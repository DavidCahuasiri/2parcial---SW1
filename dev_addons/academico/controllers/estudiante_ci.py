from odoo import http
from odoo.http import request

class EstudianteController(http.Controller):

    @http.route('/api/estudiantes/<string:ci>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_estudiante_por_ci(self, ci, **kwargs):
        if not ci:
            return {'status': 400, 'message': 'Cédula es requerida'}

        estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)])
        if not estudiante:
            return {'status': 404, 'message': 'Estudiante no encontrado'}

        estudiante_data = {
            'id': estudiante.id,
            'nombre': estudiante.name,
            'ci': estudiante.ci,
            'email': estudiante.email,
            'telefono': estudiante.phone,
            'curso': estudiante.curso_id.name if estudiante.curso_id else '',
        }
        return {'status': 200, 'data': estudiante_data}
