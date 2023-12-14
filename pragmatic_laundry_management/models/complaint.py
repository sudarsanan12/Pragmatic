from odoo import _, api, fields, models, tools

class Complaint(models.Model):

    _name = 'laundry_management.complaint'
    _description = 'complaint_laundry_management'
    _rec_name = 'sequence'

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default='New')
    status = fields.Selection([('canceled', 'Canceled'),('recieved', 'Recieved')])
    customer_name_id = fields.Many2one('res.partner',string='Customer',related="order_id_id.partner_id")
    contact_number = fields.Char(related='customer_name_id.phone',string='Phone')
    order_id_id = fields.Many2one('sale.order',string='Order')
    complaint_description  = fields.Text(string="Complaints")


    @api.model
    def create(self, vals):
        data_to_pass = self.env.context.get('default_data_to_pass', {})
        vals.update(data_to_pass)
        seq = self.env['ir.sequence'].sudo().next_by_code('laundry_management.review') or _('New')
        res =  super().create(vals)
        res.sequence = seq
        return res

    def cancel_action(self):
        self.status = 'canceled'

    def aprove_action(self):
        self.status = 'recieved'
    
    def resolve_action(self):
        self.status = 'resolved'


