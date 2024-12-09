from odoo import fields, models, api

class CrmCustomerRequest(models.Model):
    _name = "crm.customer.request"
    _description = "Customer Request"
    # khai bao cac truong trong bang
    # product.template
    product_id = fields.Many2one('product.template', string="Product Template", required = True)
    # crm.lead
    opportunity_id = fields.Many2one('crm.lead', string="Associated Lead", required = True)
    # date, mac dinh today
    date = fields.Date(string = "Date", default = fields.Date.today(), required = True)
    # description
    description = fields.Char(string = "Description")
    # qty default = 1
    qty = fields.Float(string = "Quantity", default = 1)

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    #izi test them truong one2many
    request_ids = fields.One2many('crm.customer.request', 'opportunity_id', string='Customer Requests')
    requests_count = fields.Float(compute='_compute_customer_request_data', string="Expected Sales")
    #requests_total = fields.Float(compute='_compute_customer_request_data', string="Expected Revenue")

    @api.depends('request_ids.opportunity_id', 'request_ids.qty')
    def _compute_customer_request_data(self):
        for lead in self:
            lead.requests_count = sum(
                opp.qty for opp in lead.request_ids
            )