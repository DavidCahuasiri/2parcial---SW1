from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Horario(models.Model):
    _name = 'academico.horario'
    _description = 'Horario de Clases'

    name = fields.Many2one('academico.curso', string='Curso', required=True)
    materia_id = fields.Many2one('academico.materia', string='Materia', required=True)
    aula_id = fields.Many2one(related='name.aula_id', string='Aula', required=True)
    start_time = fields.Datetime(string='Hora de Inicio', required=True)
    end_time = fields.Datetime(string='Hora de Fin', required=True)
    estudiante_ids = fields.One2many(related='name.estudiante_ids', string='Estudiantes', readonly=True)
    nivel_id = fields.Selection(related='name.nivel', string='Nivel', readonly=True)
    
    @api.constrains('start_time', 'end_time')
    def _check_time_validity(self):
        for record in self:
            if record.start_time >= record.end_time:
                raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

    @api.constrains('start_time', 'end_time', 'aula_id')
    def _check_overlap_aula(self):
        for record in self:
            overlapping_classes = self.env['academico.horario'].search([
                ('aula_id', '=', record.aula_id.id),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if overlapping_classes:
                raise ValidationError("Existe un solapamiento de horarios para el aula seleccionada.")

    @api.constrains('start_time', 'end_time', 'name')
    def _check_overlap_curso(self):
        for record in self:
            overlapping_classes = self.env['academico.horario'].search([
                ('name', '=', record.name.id),
                ('id', '!=', record.id),
                ('start_time', '<', record.end_time),
                ('end_time', '>', record.start_time),
            ])
            if overlapping_classes:
                raise ValidationError("Existe un solapamiento de horarios para el curso seleccionado.")
