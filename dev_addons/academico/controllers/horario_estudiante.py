from odoo import http, _
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class GestionAcademicaController(http.Controller):

    @http.route('/api/horario/estudiante/<string:ci>', type='json', auth='public', methods=['GET', 'OPTIONS'], csrf=False)
    def get_horario(self, ci, **kwargs):
        try:
            if request.httprequest.method == 'OPTIONS':
                headers = {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type',
                }
                return Response(status=200, headers=headers)

            if not ci:
                return Response(
                    json.dumps({'status': 400, 'message': 'Cédula es requerida'}),
                    status=400,
                    headers={'Content-Type': 'application/json'}
                )

            estudiante = request.env['academico.estudiante'].sudo().search([('ci', '=', ci)], limit=1)
            if not estudiante:
                return Response(
                    json.dumps({'status': 404, 'message': 'Estudiante no encontrado'}),
                    status=404,
                    headers={'Content-Type': 'application/json'}
                )

            horario_data = []
            horarios = request.env['academico.horario'].sudo().search([('curso_id', '=', estudiante.curso_id.id)])
            for horario in horarios:
                horario_data.append({
                    'curso': horario.curso_id.name,
                    'nivel': horario.nivel_id.name if horario.nivel_id else None,
                    'materia': horario.materia_id.name,
                    'aula': horario.aula_id.name,
                    'start_time': horario.start_time,
                    'end_time': horario.end_time,
                })

            return Response(
                json.dumps({'status': 200, 'data': horario_data}),
                status=200,
                headers={'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
            )
        except Exception as e:
            # Registrar el error en los logs de Odoo
            request.env.cr.rollback()
            _logger.exception("Error al obtener el horario del estudiante: %s", e)
            return Response(
                json.dumps({'status': 500, 'message': 'Internal Server Error'}),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
