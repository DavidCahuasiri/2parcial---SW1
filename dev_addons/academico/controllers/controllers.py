# -*- coding: utf-8 -*-
# from odoo import http


# class Academico(http.Controller):
#     @http.route('/academico/academico', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/academico/academico/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('academico.listing', {
#             'root': '/academico/academico',
#             'objects': http.request.env['academico.academico'].search([]),
#         })

#     @http.route('/academico/academico/objects/<model("academico.academico"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('academico.object', {
#             'object': obj
#         })

