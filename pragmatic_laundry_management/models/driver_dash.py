from odoo import models, fields, api, _
from odoo.exceptions import MissingError


class Driver_dash(models.Model):
    _inherit = 'stock.picking'

    is_picked = fields.Boolean(string="Picked",default = False)
    laundry_order_id=fields.Many2one('sale.order',string='Laundry Order Id')
    driver_id = fields.Many2one('res.users',string="Pickup driver")
    delivery_driver_id = fields.Many2one('res.users',string="Delivery driver")
 

    def button_validate(self):
        if self.laundry_order_id.state == 'out_for_delivery':
            for products in self.move_ids_without_package:
                if products.quantity_done <= 0:
                    raise MissingError('Please update the done quantity')
            self.laundry_order_id.state = 'delivered'
            template = self.env.ref('pragmatic_laundry_management.laundry_email_template_delivery')
            template.send_mail(self.laundry_order_id.id, force_send=True)
        elif self.laundry_order_id.state == 'assign_to_pick_up':
            self.laundry_order_id.state = 'picked'
            self.is_picked = True
        return super(Driver_dash, self).button_validate()
    
    def action_reached_store(self):
        self.laundry_order_id.state = 'reached_store'
        self.is_picked = False
    
    def action_delivered_laundry(self):
        if self.laundry_order_id.state == 'out_for_delivery':
            self.laundry_order_id.state = 'delivered'