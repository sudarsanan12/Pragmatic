from odoo import http
from odoo.addons.portal.controllers.portal import CustomerPortal

class YourCustomCustomerPortal(CustomerPortal):

    def _prepare_orders_domain(self, partner):
        super(YourCustomCustomerPortal, self)._prepare_orders_domain(partner)
        domain = [
            ('message_partner_ids', 'child_of', [partner.commercial_partner_id.id]),
            ('state', '!=', 'draft'),
        ]
        return domain