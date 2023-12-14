
from odoo import models, fields, api


class Service(models.Model):
    _name = 'laundry_management.service'
    _description = 'Service Page'

    name = fields.Char(string="Service Name" ,required=True)
    description = fields.Text(string="Service Description" ,required=True)
    image = fields.Binary(string="Image" ,required=True)