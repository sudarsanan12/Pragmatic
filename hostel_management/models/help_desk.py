from odoo import models,fields,api



class HelpDesk(models.Model):
    _name = 'hostel.helpdesk'
    _description = 'helpdesk'
    _rec_name = 'seq'
    
    seq = fields.Char(string = 'Sequence',required = True,readonly = True,copy = False,default = 'New')
    student_id = fields.Many2one('hostel.student',required = True)
    room_no = fields.Char(string = 'Room No',compute = '_compute_room_id',store = True)
    complaint_description = fields.Char(string = 'Complaint Description',required = True)
    complaint_time = fields.Datetime(string = 'Complaint Time',default = lambda self: fields.Datetime.now())
    complaint_status = fields.Selection([
        ('pending','pending'),
        ('recieved','recieved')
    ],string = 'Complaint Status',default = 'pending',readonly = True)


    @api.depends('student_id')
    def _compute_room_id(self):
        for rec in self:
            room_allocation = self.env['hostel.roomallocation'].search([('student_ids', 'in', rec.student_id.ids)], limit = 1)
            rec.room_no = room_allocation.room_id.room_no if room_allocation else False
    

    def create_maintenance(self):
        self.env['hostel.maintenance'].create({
            'room_no':self.room_no,
            'complaint_description':self.complaint_description,
            'complaint_time':self.complaint_time,
            'helpdesk_id':self.id,
            })
        records = self.search([('complaint_status','=', 'pending')])
        values = {
            'complaint_status': 'recieved',
        }
        records.write(values)
        
    
    def action_open(self):
        return{
            'type':'ir.actions.act_window',
            'name':'Maintenance',
            'res_model':'hostel.maintenance',
            'domain':[('helpdesk_id','=',self.id)],
            'view_mode':'tree,form',
            'target':'current',
            }
    
    
    @api.model
    def create(self, vals):
        if vals.get('seq',('New')) == ('New'):
            vals['seq'] = self.env['ir.sequence'].next_by_code('hostel.helpdesk.seq') or ('New')
        res = super(HelpDesk, self).create(vals)
        return res