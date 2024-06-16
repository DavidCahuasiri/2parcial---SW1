from odoo import http
from odoo.http import request

class ProfesorController(http.Controller):

    @http.route('/api/horario/profesor/<string:ci>', type='http', auth='public', methods=['GET'], csrf=False)
    def get_horario_por_ci(self, ci, **kwargs):
        if not ci:
            return {'status': 400, 'message': 'Cédula es requerida'}

        # Buscar al profesor por su cédula
        profesor = request.env['academico.profesor'].sudo().search([('ci', '=', ci)], limit=1)
        if not profesor:
            return {'status': 404, 'message': 'Profesor no encontrado'}

        horario_data = []
        # Buscar todas las materias asociadas al profesor
        materias = request.env['academico.materia'].sudo().search([('profesor_id', '=', profesor.id)])
        for materia in materias:
            # Buscar los horarios asociados a la materia
            horarios = request.env['academico.horario'].sudo().search([('materia_id', '=', materia.id)])
            for horario in horarios:
                horario_data.append({
                    'curso': horario.curso_id.name,
                    'nivel': horario.nivel_id,
                    'materia': horario.materia_id.name,
                    'aula': horario.aula_id.name,
                    'start_time': horario.start_time.strftime('%Y-%m-%d %H:%M:%S') if horario.start_time else None,
                    'end_time': horario.end_time.strftime('%Y-%m-%d %H:%M:%S') if horario.end_time else None,
                })

        return {'status': 200, 'data': horario_data}
