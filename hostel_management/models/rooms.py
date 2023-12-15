from odoo import models,fields,api
from odoo.exceptions import ValidationError


class HostelRooms(models.Model):
    _name = 'hostel.room'
    _description = 'hostel.room'
    _rec_name = 'room_no'
    
    room_no = fields.Char(string="Room number") 
    sequence_number = fields.Char(string = "id")
    room_type = fields.Selection([('2share', '2 share'), ('3share', '3 share'), ('4share', '4 share')],string='Type of room',required=True)
    room_ac = fields.Boolean(string='Ac room', default=True)
    count = fields.Integer(string="Count of people")
    bath_attached = fields.Boolean(string='Bathroom attached', default=True)
    availability = fields.Boolean(string='Room availability', default=True)
    room_rate = fields.Float( string='Room Price', store=True)
    mess_rate = fields.Float( string='Mess Price', store=True) #++++
    student_id = fields.Many2one('hostel.student')
    



    @api.onchange('room_type', 'count')
    def _check_count_with_room_type(self):
        for record in self:
            if record.room_type == '2share' and record.count > 2:
                raise ValidationError('count of people must be 2 or below 2')
            elif record.room_type == '3share' and record.count > 3:
                raise ValidationError('count of people must be 3 or below 3')
            elif record.room_type == '4share' and record.count > 4:
                raise ValidationError('count of people must be 4 or below 4')

    @api.constrains('room_no')
    def _check_unique_field(self):
        for record in self:
            existing_records = self.search([('room_no', '=', record.room_no)])
            if len(existing_records) > 1:
                raise ValidationError('room number must be unique!')


    @api.model
    def create(self, vals):
        vals['sequence_number'] = self.env['ir.sequence'].next_by_code('hostel.room')
        return super(HostelRooms, self).create(vals)
        