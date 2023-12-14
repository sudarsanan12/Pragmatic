# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.addons.website_sale.controllers.main import WebsiteSale
import base64


class ComplaintPage(http.Controller):
    @http.route('/laundry/complaint/page', type='http', auth='public', website=True)
    def custom_complaint_page(self, order=False, **post):
        values = {}
        orders = request.env['sale.order'].sudo().search([('id', "=", int(order))])
        values.update({
            'orders': orders
        })
        return request.render('pragmatic_laundry_management.complaint_page_template', values)

    @http.route(['/laundry/complaint-submit'], type='http', auth="user", website=True)
    def checkout(self, **post):
        sale_id = post.get('order_id_id')
        complaint = request.env['laundry_management.complaint'].search([('order_id_id.id', '=', sale_id)])
        sale = request.env['sale.order'].search([('id', '=', sale_id)])
        if not complaint.id:
            sale.sudo().write({'is_complaint' : True})
            request.env['laundry_management.complaint'].create(post)
        return request.render('pragmatic_laundry_management.complaint_return_page_template')


class Website(http.Controller):
    @http.route('/', type='http', auth='public', website=True)
    def web(self):
        services = request.env['laundry_management.service'].search([])

        values = {}
        active_company = request.env.user.company_id.id
        data = request.env['res.company'].browse([active_company])
        values.update({
            'data': data,
            'services': services,
        })
        return request.render('pragmatic_laundry_management.website_template', values)

class CustomWebsiteSale(WebsiteSale):

    @http.route(['/shop/checkout'], type='http', auth="user", website=True)
    def checkout(self, order=False, **post):
        # Check if the user is logged incomplaint
        if request.env.user and request.env.user != request.website.user_id:
            return super(CustomWebsiteSale, self).checkout(**post)
        else:
            return request.redirect('/web/login?redirect=/shop/checkout')


class ReviewPage(http.Controller):
    @http.route('/laundry/reviews/page', type='http', auth='public', website=True)
    def custom_review_page(self, rev=False, **post):
        values = {}
        revs = request.env['sale.order'].sudo().search([('id', "=", int(rev))])
        values.update({
            'revs': revs
        })
        return request.render('pragmatic_laundry_management.review_page_template',values)
    
    @http.route(['/laundry/reivew-submit'], type='http', auth="user", website=True)
    def checkout(self, **post):
        sale_id = post.get('sale_id')
        review = request.env['laundry_management.review'].search([('sale_id.id', '=', sale_id)])
        sale = request.env['sale.order'].search([('id', '=', sale_id)])
        if not review.id:
            sale.sudo().write({'is_reviewed' : True})
            request.env['laundry_management.review'].create(post)
        return request.render('pragmatic_laundry_management.review_return_page_template')