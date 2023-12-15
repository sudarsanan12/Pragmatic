# -*- coding: utf-8
from odoo import http
from odoo.http import request

# from odoo.addons.website_sale.controllers.main import WebsiteSale

# class MyWebsiteSale(WebsiteSale):

#     @http.route(['/shop'], type='http', auth="public", website=True)
#     def shop(self, page=0, category=None, search='', ppg=False, **post):
#         try:
#             domain = request.httprequest.environ['HTTP_X_FORWARDED_SERVER']
#         except:
#             domain = request.httprequest.environ['HTTP_HOST']

#         path = request.httprequest.environ['PATH_INFO']
#         try:
#             http = request.httprequest.environ['HTTP_REFERER']
#         except:
#             http = request.httprequest.environ['HTTP_X_FORWARDED_PROTO']

#         if 'https' in http:
#             http = 'https://'
#         else:
#             http = 'http://'

#         if not request.session.uid:
#             url = "/web/login?redirect=" + \
#             str(http) + "/" + str(domain) + "/" + str(path)
#             url = url.replace('//', '/')
#             return request.redirect(url)
#         # Your custom code here, if needed
#         return super(MyWebsiteSale, self).shop(page=page, category=category, search=search, ppg=ppg, **post)





class StudentRegistration(http.Controller):
    @http.route(['/register'], type='http', auth="public",website=True)
    def website_menu(self):
        # request.env['hostel.student'].sudo().create()
        
        return request.render("hostel_management.register_form")
    
    @http.route(['/register_submit'], type='http', auth="public", website=True)
    def website_menu_student(self, **post):
        request.env['hostel.student'].create(post)
        return request.render('hostel_management.registration_success_template1')
       






class ServiceRequest(http.Controller):

    @http.route(['/complaint'], type='http', auth="public",website=True)
    def complaint_form(self):   
        return request.render("hostel_management.complaint_registration_form")

    @http.route(['/complaint_submit'], type='http', auth="public",website=True,csrf=False)
    def complaint_submission(self,**post):
        name=post.get('student_id')
        complaint=post.get('complaint_description')
        if request.env['hostel.student'].search([('sequence','=',name)]):
            student_id = request.env['hostel.student'].search([('sequence','=',name)])
            request.env['hostel.helpdesk'].create({
            'student_id':student_id.id,'complaint_description':complaint,
            })
            return request.render('hostel_management.registration_success_template')
        else :
            return request.render('hostel_management.registration_invalid_template')


        

    
    
class Home(http.Controller):
    @http.route(['/'], type='http', auth='public', website=True)
    def home(self):
        return http.request.render('hostel_management.home',{})
                            


class ContactUs(http.Controller):
    @http.route(['/contact'], type='http', auth="public", website=True)
    def contact_menu(self):        
        return request.render("hostel_management.contact_form")
    
    @http.route(['/contact_submit'], type='http', auth="public", website=True)
    def website_success_contact(self, **post):
        request.env['hostel.contact'].create(post)
        return request.render('hostel_management.contact_success_template')
