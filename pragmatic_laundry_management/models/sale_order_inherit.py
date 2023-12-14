from odoo import models, fields, api, _
from odoo.exceptions import MissingError



class SalesInheritance(models.Model):
    _inherit = "sale.order"
    _description = 'Office Employee'


    driver_id = fields.Many2one('res.users',string="Pickup driver")
    qc_id = fields.Many2one('res.users')
    cleaner_id = fields.Many2one('res.users', string="Service Person")
    is_out_of_delivery = fields.Boolean(string='Is out of delivery',default=False)
    is_reviewed = fields.Boolean(default=False, copy=False)
    is_complaint = fields.Boolean(default=False, copy=False)
    state = fields.Selection(selection_add=[('assign_to_pick_up', 'Assign to pick up'), ('picked', 'Picked'),
                                            ('reached_store', 'Reached Store'), ('in_service', 'In Service'),
                                            ('service_completed', 'Service Completed'), ('qc', 'QC'),('qc_approved','QC Approved'),('qc_rejected','QC Rejected'),
                                            ('out_for_delivery', 'Out For Delivery'), ('delivered', 'Delivered')])


    def action_assign(self):   
        if not self.driver_id:
            raise MissingError("Driver must not be empty")
        self.state = 'assign_to_pick_up'
        template = self.env.ref('pragmatic_laundry_management.laundry_email_template_driver')
        template.send_mail(self.id, force_send=True)
        order_id = self.env['stock.picking'].search([('laundry_order_id', '=', self.id)])
        order_id.is_picked = True
        stock_picking_obj = self.env['stock.picking']
        for order in self:
            # Create a stock picking record
            picking_vals = {
            'partner_id': order.partner_id.id,
            'location_dest_id': order.warehouse_id.lot_stock_id.id,
            'location_id': order.partner_id.property_stock_customer.id,
            'picking_type_id': order.warehouse_id.in_type_id.id,
            'laundry_order_id':order.id,
            'driver_id':order.driver_id.id,
            'move_type': 'direct',
            'origin': order.name,
                }
 
            # Add products from sale order lines to the picking
            lis = []
            for line in order.order_line:
                move_vals = {
                'name': line.product_id.name,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'quantity_done' : line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'location_id': order.partner_id.property_stock_customer.id,
                'location_dest_id': order.warehouse_id.lot_stock_id.id,
                }
                lis.append((0,0,move_vals))
            
            picking_vals['move_ids_without_package'] = lis
    # Create the picking
            stock_picking = stock_picking_obj.create(picking_vals)
            stock_picking.action_confirm()
            stock_picking.action_assign()
        return True    
    
   
    # def action_pick_up(self):
    #     self.state = 'picked'
    #     order_id = self.env['stock.picking'].search([('laundry_order_id', '=', self.id)])
    #     order_id.button_validate()
    #     order_id.is_picked = True
        

    def action_reach_store(self):
        self.state = 'reached_store'
        order_id = self.env['stock.picking'].search([('laundry_order_id', '=', self.id)])
        order_id.is_picked = False


    def action_service_order(self):
        cleaner = self.env['laundry_management.cleaner'].search([('sale_id', '=', self.id)])
        return{
                'type': 'ir.actions.act_window',
                'name': 'Service order',
                'res_id' : cleaner.id,
                'res_model': 'laundry_management.cleaner',
                'view_mode': 'form',
                'target': 'current',
                'view_id' : self.env.ref('pragmatic_laundry_management.view_cleaner_dashboard_form').id
            }        

    def action_service_test(self):
        if not self.cleaner_id:
            raise MissingError("Please assign a Cleaner")
        else :
            template = self.env.ref('pragmatic_laundry_management.laundry_email_template_cleaner')
            template.send_mail(self.id, force_send=True)
            self.env['laundry_management.cleaner'].create({
            'sale_id' : self.id,
            'cleaner_id' : self.cleaner_id.id
        })
        self.state = 'in_service'
        cleaner = self.env['laundry_management.cleaner'].search([('sale_id', '=', self.id)])
        cleaner.state = 'pending'
        

    def action_service_complete(self):
        self.state = 'service_completed'
        cleaner = self.env['laundry_management.cleaner'].search([('sale_id', '=', self.id)])
        cleaner.state = 'service_completed'

    def action_quality(self):
        self.state = 'qc'
        if not self.qc_id:
            raise MissingError("Please assign a QC")
        template = self.env.ref('pragmatic_laundry_management.laundry_email_template_qc')
        template.send_mail(self.id, force_send=True)
        qc_order = self.env['laundry_management.qc'].search([('sale_id', '=', self.id)])
        if qc_order.id == False :
            self.env['laundry_management.qc'].create({
                'sale_id' : self.id,
                'qc_id' : self.qc_id.id
            })
        qc_order.state = 'pending'
    def action_quality_approved(self):
        qc_order = self.env['laundry_management.qc'].search([('sale_id', '=', self.id)])
        qc_order.state = 'approved'
        self.state = 'qc_approved'
    
    
    def action_quality_rejected(self):
        qc_order = self.env['laundry_management.qc'].search([('sale_id', '=', self.id)])
        qc_order.state = 'rejected'
        self.state = 'qc_rejected'
    
    def action_reservice(self):
        self.state = 'in_service'
        cleaner = self.env['laundry_management.cleaner'].search([('sale_id', '=', self.id)])
        cleaner.state = 'in_service'
        

    def action_out_for_delivery(self):
        self.state = 'out_for_delivery'
        self.is_out_of_delivery = True
        action = {
        'name': "Delivery Driver",
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'laundry_management.driver.delivery.wizard',
        'view_id': self.env.ref('pragmatic_laundry_management.driver_delivery_wizard_form').id,
        'target': 'new',
            }
        return action


    def action_deliver(self):
        self.state = 'delivered'
        template = self.env.ref('pragmatic_laundry_management.laundry_email_template_delivery')
        template.send_mail(self.id, force_send=True)

    def action_transaction_order(self):
            order_id = self.env['stock.picking'].search([('laundry_order_id', '=', self.id),('picking_type_id.code','=','incoming')])
            return{
                'type': 'ir.actions.act_window',
                'name': 'Picking',
                'res_id' : order_id.id,
                'res_model': 'stock.picking',
                'view_mode': 'form',
                'target': 'current',
                'view_id' : self.env.ref('stock.view_picking_form').id              
            }
    

    def action_qc_order(self):
            order_id = self.env['laundry_management.qc'].search([('sale_id', '=', self.id)])
            return{
                'type': 'ir.actions.act_window',
                'name': 'QC',
                'res_id' : order_id.id,
                'res_model': 'laundry_management.qc',
                'view_mode': 'form',
                'target': 'current',
                'view_id' : self.env.ref('pragmatic_laundry_management.qc_form').id
            }
    
    def action_confirm(self):
        res=super(SalesInheritance, self).action_confirm()
        picking = self.env['stock.picking'].search([('origin','=',self.name)])
        if picking:
            picking.laundry_order_id = self.id
            picking.state = 'assigned'
        return res
