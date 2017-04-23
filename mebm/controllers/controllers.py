# -*- coding: utf-8 -*-
from odoo import http

# class Mebm(http.Controller):
#     @http.route('/mebm/mebm/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mebm/mebm/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mebm.listing', {
#             'root': '/mebm/mebm',
#             'objects': http.request.env['mebm.mebm'].search([]),
#         })

#     @http.route('/mebm/mebm/objects/<model("mebm.mebm"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mebm.object', {
#             'object': obj
#         })