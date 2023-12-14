from odoo import models, fields, api


class Customer(models.Model):
    _inherit = 'res.partner'


    is_admin = fields.Boolean(string="Admin",default=False)
    is_driver = fields.Boolean(string="Driver",default=False)
    is_qc = fields.Boolean(string="QC",default=False)
    is_cleaner = fields.Boolean(string="Cleaner",default=False)
