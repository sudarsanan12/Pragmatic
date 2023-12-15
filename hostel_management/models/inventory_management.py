from odoo import models,fields,api, _
from odoo.exceptions import ValidationError

class HostelRoomInventory(models.Model):
    _name = 'hostel.inventory'
    _description = 'hostel.inventory'
    
    

    name = fields.Char(string="Name of the product") 
    category = fields.Selection([ ('Mess', 'Mess management'),  ('Room', 'Room management')],string='Category of product',default="Mess management" ,required=True)
    uom = fields.Selection([ ('unit', 'Unit'), ('kg', 'KG'), ('grams', 'Grams'), ('dozen', 'Dozen')],string='Unit of measure',required=True)
    count = fields.Float(string='count of item',readonly=True)
    sequence = fields.Char(string = 'Sequence',required=True, copy=False, readonly=True, default=lambda self: _('New'))



    @api.constrains('name')
    def _check_unique_field(self):
        for record in self:
            existing_records = self.search([('name', '=', record.name)])
            if len(existing_records) > 1:
                raise ValidationError('Field Name must be unique!')

    @api.model
    def create(self, vals):
        if vals.get('sequence', ('New')) == ('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('hostel.inventory') or ('New')
            return super(HostelRoomInventory, self).create(vals)