from odoo import models, fields, api



class DriverDeliveryWizard(models.TransientModel):
    _name = 'laundry_management.driver.delivery.wizard'
    _description = 'Delivery Driver'

    sale_id = fields.Many2one('sale.order', string='Order id', default= lambda self: self.get_order(), readonly=1)
    driver_id = fields.Many2one('res.users')

    def get_order(self):
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        return docs
    
    def action_assgin_driver(self):
        res = self.env['stock.picking'].search([('origin','=',self.sale_id.name),('picking_type_code', '=', 'outgoing')])
        res.laundry_order_id = self.sale_id.id
        res.delivery_driver_id = self.driver_id.id
        template = self.env.ref('pragmatic_laundry_management.laundry_email_template_driver')
        template.send_mail(self.sale_id.id, force_send=True)