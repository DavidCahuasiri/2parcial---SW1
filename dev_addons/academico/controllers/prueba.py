from odoo import http # type: ignore
from odoo.http import request # type: ignore
import json

class HelloApi(http.Controller):
    @http.route('/api/estudiantes', auth='public', website=False, csrf=False, type='json', methods=['GET', 'OPTIONS'], cors='*')
    def hello(self, **kw):
        if request.httprequest.method == 'OPTIONS':
            headers = [
                ('Access-Control-Allow-Origin', '*'),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
            ]
            return request.make_response('OK', headers=headers)
        
        estudiantes = request.env['academico.estudiante'].sudo().search([])
        est_list = []
        for est in estudiantes:
            est_list.append({
                'name': est.name,
                'ci': est.ci,
                'email': est.email,
                'phone': est.phone,
                'curso_id': est.curso_id.name
            })
        
        headers = [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*')
        ]
        
        return est_list
