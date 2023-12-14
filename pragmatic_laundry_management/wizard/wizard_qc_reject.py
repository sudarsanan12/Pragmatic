from odoo import models, fields, api
from odoo.http import request


class RejectWizard(models.TransientModel):
    _name = 'laundry_management.qc.wizard'
    _description = 'Reject Reason'

    sale_id = fields.Many2one('sale.order')
    reason_to_reject = fields.Text(string='Describe The Reason')


    
    def quality_issue(self):
        sale_id = self.env['sale.order'].browse(self.env.context.get('sale_id'))
        qc_id = self.env['laundry_management.qc'].browse(self.env.context.get('qc_id'))
        qc_id.sale_id.state = 'qc_rejected'
        qc_id.state = "rejected"
        cleaner = self.env['laundry_management.cleaner'].search([('sale_id', '=', sale_id.id)])
        cleaner.state = 'pending'
        if sale_id:
            self.sale_id = sale_id.id
        qc_id.reason_to_reject = self.reason_to_reject
        qc_id.message_post(body=f' <b>Qc Rejected</b> <br> Reject Reason is : {self.reason_to_reject}')
        self.sale_id.message_post(body=f' <b>Qc Rejected</b> <br> Reject Reason is : {self.reason_to_reject}')
        service=self.env['laundry_management.cleaner'].search([('sale_id','=',self.sale_id.id)])  
        if service:
            service.message_post(body=f' <b>Qc Rejected</b> <br> Reject Reason is : {self.reason_to_reject}')
        return qc_id.sale_id

