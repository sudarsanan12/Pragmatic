from odoo import models,fields




class Hostelcontact(models.Model):
    _name = 'hostel.contact'
    _description = 'hostel.contact'
    
    name = fields.Char(required=True) 
    phone = fields.Char(required=True)
    email= fields.Char (required = True)
    subject = fields.Char()
    question = fields.Char(required=True)