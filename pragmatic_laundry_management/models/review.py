# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class Review(models.Model):
    _name = 'laundry_management.review'
    _description = 'laundry_management.review'
    _rec_name = 'sequence'

    review = fields.Char()
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default=lambda self: _('New')) 
    customer_id =fields.Many2one('res.partner',related="sale_id.partner_id")
    rating = fields.Float(string='Rating')
    sale_id = fields.Many2one('sale.order',string='Order Id')


    @api.model
    def create(self, vals):
        seq = self.env['ir.sequence'].sudo().next_by_code('laundry_management.review') or _('New')
        res =  super().create(vals)
        res.sequence = seq
        return res

    