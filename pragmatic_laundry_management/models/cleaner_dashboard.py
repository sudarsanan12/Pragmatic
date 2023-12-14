from odoo import models, fields, api


class CleanerDashboard(models.Model):
    _name = 'laundry_management.cleaner'
    _inherit=['mail.thread']
    _description = 'Cleaner Dashboard'

    
    sequence = fields.Char(default="New")
    sale_id = fields.Many2one('sale.order', string='Order id', readonly=1)
    cleaner_id = fields.Many2one('res.users', string='Cleaner')
    state = fields.Selection([('pending', 'Pending'),('in_service', 'IN SERVICE'),('service_completed','SERVICE COMPLETED')], default='pending')


    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('laundry_management.cleaner')
        return super(CleanerDashboard, self).create(vals)
  
    def servicein(self):
        self.state = 'in_service'
        self.sale_id.state = 'in_service'
     
    def serviceout(self):
        self.state = 'service_completed'
        self.sale_id.state = 'service_completed'