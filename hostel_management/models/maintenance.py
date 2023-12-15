from odoo import models, fields, api ,_


class HostelMaintenance(models.Model):
    _name = 'hostel.maintenance'
    _description = 'maintenance'
    _rec_name='sequence'


    assigned_person = fields.Char(string='Assigned Person')
    profession = fields.Selection([
        ('electronician', 'Electronician'),
        ('carpenter', 'Carpenter'),
        ('plumber', 'Plumber'),
        ('painter', 'Painter'),
        ('intercom', 'Intercom')
    ], string = 'Profession')

    status = fields.Selection([
        ('pending', 'Pending'),
        ('assigned', 'Assigned'),
        ('done', 'Done')
    ], string = 'Status', default = 'pending')

    sequence = fields.Char(string = 'Sequence')
    helpdesk_id = fields.Many2one('hostel.helpdesk')
    room_no = fields.Char(string = 'Room No')
    complaint_description = fields.Char(string = 'Complaint Description')
    complaint_time = fields.Datetime(string = 'Complaint Time')
    price = fields.Char(string = 'Total Price')

    def assigned(self):
        self.status = "assigned"

    def done(self):
        self.status = "done"

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hostel.maintenance')
        return super(HostelMaintenance, self).create(vals)
