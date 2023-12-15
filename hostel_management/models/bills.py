from odoo import models, fields, api, _


class Bill(models.Model):
    _name = 'hostel.management'
    _description = 'bill_hostel'

    student_id = fields.Many2one('hostel.student', string='Student')
    name = fields.Char(string='Name', related='student_id.name')
    email = fields.Char(string='Email', related='student_id.email')
    date = fields.Date(string='Date')
    address = fields.Char(string='Permanent Address', related='student_id.permanent_address')
    contact_no = fields.Char(string='Contact Number', related='student_id.contact')
    gender = fields.Selection (string='Gender', related='student_id.gender' )    
    sequence = fields.Char(string = 'Sequence')
    room_id = fields.Many2one('hostel.room',compute ='_compute_room_id', string='Room', store=True)
    room_type = fields.Char(compute='_compute_room_id1',store=True)
    room_ac = fields.Boolean(store=True)
    bath_attached = fields.Boolean(store=True)
    room_price = fields.Float(string='Room Bill',store=True)
    mess_price = fields.Float(string='Mess Bill',Store = True)  
    bill_lines=fields.One2many('hostel.management.line','room_line_id',string='Bill Lines')
    total_price = fields.Float(String="Total",compute="calculate_total")

    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
    ], string='status', default='draft')

    def draft(self):
        self.status = "draft"

    def paid(self):
        self.status = "paid"

    @api.depends('total_price','bill_lines.price')
    def calculate_total(self):
        for total in self:
            total.total_price+= sum((line.rate) for line in total.bill_lines)



            
    @api.depends('student_id')
    def _compute_room_id(self):
        for rec in self:
            room_allocation = self.env['hostel.roomallocation'].search([('student_ids', 'in', rec.student_id.ids)], limit=1)
            rec.room_id = room_allocation.room_id if room_allocation else False
    
    
    @api.depends('room_id')
    def _compute_room_id1(self):
        for rec in self: 
            room = rec.room_id      
            if room:        #if room is truthy, the method assigns the values of various fields from the room record to the corresponding fields in the current record (rec). This includes room_type, room_ac, bath_attached, and room_price.               
                rec.room_type = room.room_type
                rec.room_ac = room.room_ac
                rec.bath_attached = room.bath_attached
                rec.room_price = room.room_rate
                rec.mess_price = room.mess_rate


            else:
                rec.room_type = False
                rec.room_ac = False
                rec.bath_attached = False
                rec.room_price = False
                rec.mess_price = False

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hostel.management')
        return super(Bill, self).create(vals)   
    

class BillLine(models.Model):
    _name = 'hostel.management.line'
    _description = 'bill_hostel_line'

    product_id=fields.Many2one('hostel.room', string="Room No")
    fee_type=fields.Selection([('room','Room Rent'),('mess','Mess Fee')])
    room_line_id=fields.Many2one('hostel.management',string='Room Bill', store=True)
    types = fields.Char('room_line_id.room_price')
    price = fields.Float(string='Price')
    rate = fields.Float(string="Price")

    

    
    @api.onchange('fee_type')
    def onchange_fee_type(self):
        if self.fee_type == 'room':
            self.product_id = self.room_line_id.room_id
            self.rate = self.room_line_id.room_price
        
        elif self.fee_type == 'mess':
            self.product_id = self.room_line_id.room_id
            self.rate = self.room_line_id.mess_price
