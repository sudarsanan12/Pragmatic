# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class QualityController(models.Model):
    _name = 'laundry_management.qc'
    _inherit=['mail.thread']
    _description = 'Quality controller'
    _rec_name = 'sequence'

    sequence = fields.Char(default=lambda self: _('New'))
    sale_id = fields.Many2one('sale.order', string='Order id', readonly=1)
    qc_id = fields.Many2one('res.users', string='Quality controller', readonly=1)
    reason_to_reject = fields.Text(readonly=1, default='NA')
    state = fields.Selection([('pending', 'Pending'), ('rejected', 'Rejected'),
                                ('approved', 'Approved')], string='Status', default ="pending")

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code(
                'laundry_management.qc') or _('New')
        res = super(QualityController, self).create(vals)
        return res
    
    def approve(self):
        self.sale_id.state = 'qc_approved'
        self.state = "approved"

    def reject(self):
        ctx = self.env.context.copy()
        ctx.update({
            "sale_id":self.sale_id.id,
            'qc_id' : self.id
            })
        action = {
        'name': "Reason To Reject",
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'laundry_management.qc.wizard',
        'view_id': self.env.ref('pragmatic_laundry_management.reject_reason_wizard_form').id,
        'target': 'new',
        'context': ctx
            }
        return action
    
