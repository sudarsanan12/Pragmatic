from odoo import models,fields,api
from odoo.exceptions import ValidationError


class HostelRoomsAllocation(models.Model):
    _name = 'hostel.roomallocation'
    _description = 'hostel.roomallocation '
    _rec_name = 'room_id'



    room_id = fields.Many2one('hostel.room',required=True,string="Room no")
    student_ids = fields.Many2many('hostel.student',domain="[('states', '=', 'confirmed')]",required=True)
    name = fields.Char('student_ids.name')
    sequence_number = fields.Char(string="sequence")
    start_date = fields.Date(string='from')
    end_date = fields.Date(string='To')
    room_type = fields.Selection(related='room_id.room_type')
    room_ac = fields.Boolean(related='room_id.room_ac')
    bath_attached = fields.Boolean(related='room_id.bath_attached')
    room_price = fields.Float(related='room_id.room_rate')
    mess_price = fields.Float(related='room_id.mess_rate')
    count = fields.Integer(compute='_compute_student_count', string='Number of Students')
    states = fields.Selection([('pending','Pending'),('confirmed','Confirmed'),('rejected','Rejected')],string='Status',default='pending')

    def confirm(self):
        self.states = "confirmed"

    def reject(self):
        self.states = "rejected"

    @api.onchange('room_type', 'student_ids')
    def _check_count_with_room_type(self):
        student_count = len(self.student_ids)
        for record in self:
            if record.room_type == '2share' and student_count > 2:
                raise ValidationError('count of people must be 2 or below 2')
            elif record.room_type == '3share' and student_count > 3:
                raise ValidationError('count of people must be 3 or below 3')
            elif record.room_type == '4share' and student_count > 4:
                raise ValidationError('count of people must be 4 or below 4')


    @api.depends('student_ids')
    def _compute_student_count(self):
        for rec in self:
            rec.count = len(rec.student_ids)
            
            
    @api.model
    def create(self, vals):
        vals['sequence_number'] = self.env['ir.sequence'].next_by_code('hostel.roomallocation')
        return super(HostelRoomsAllocation, self).create(vals)
        