# -*- coding: utf-8 -*-
from odoo import http

# class Kidzplay(http.Controller):
#     @http.route('/kidzplay/kidzplay/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kidzplay/kidzplay/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kidzplay.listing', {
#             'root': '/kidzplay/kidzplay',
#             'objects': http.request.env['kidzplay.kidzplay'].search([]),
#         })

#     @http.route('/kidzplay/kidzplay/objects/<model("kidzplay.kidzplay"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kidzplay.object', {
#             'object': obj
#         })