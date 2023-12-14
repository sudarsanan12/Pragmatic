
from odoo import models, fields, api

class CompanyDetail(models.Model):

    _inherit = 'res.company'
    

    experiences = fields.Text()
    experiences_image = fields.Binary(attachment=True)
    company_history = fields.Text()
    history_image = fields.Binary(attachment=True)
   