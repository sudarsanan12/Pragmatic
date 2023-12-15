from odoo import models,fields,api, _
from odoo.exceptions import ValidationError


class HostelStockLine(models.Model):
    _name ='hostel.stock.line'
    _description = 'hostel Stockline'
    _rec_name = 'inventory_id'

    inventory_id = fields.Many2one('hostel.inventory',string='product')
    qty = fields.Float(string='qty')
    uom = fields.Selection(related='inventory_id.uom')
    stock_id = fields.Many2one('hostel.stock')
    
    
#  ======================================================================================================================================   


class StockManagement(models.Model):
    _name = 'hostel.stock'
    _description = 'hostel.stock'
    _rec_name = 'sequence'


    inventory_type = fields.Selection([ ('Incom', 'Incoming'),  ('Outgo', 'Outgoing')],string='Inventory Type' ,required = True)
    date = fields.Datetime(string='Date', required=True)
    sequence = fields.Char(string = 'Sequence', required = True, copy=False, readonly=True, default=lambda self: _('New'))
    line_ids = fields.One2many('hostel.stock.line','stock_id', required = True)
    status = fields.Selection([ ('pending', 'Pending'),  ('updated', 'Updated')], string='Status', default='pending', required = True)



    def pending(self):
        self.status = "pending"


    def updated(self):

        self.status = "updated"

    def update_stock(self):
        if self.inventory_type =='Incom':
            for line in self.line_ids:
                line.inventory_id.count+=line.qty

        elif self.inventory_type =='Outgo':
            for line in self.line_ids:
                if line.inventory_id.count < line.qty:
                    raise ValidationError("There is no stock in inventory. Please purchase first")
                else:
                    line.inventory_id.count-=line.qty
    
        self.status = "updated"





@api.model
def create(self, vals):
    if vals.get('sequence', _('New')) == _('New'):

        vals['sequence'] = self.env['ir.sequence'].next_by_code('hostel.stock') or _('New')
    return super(StockManagement, self).create(vals)

