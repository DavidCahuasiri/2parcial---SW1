from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Estudiante(models.Model):
    _name = 'academico.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre', required=True)
    Apaterno = fields.Char(string='Apellido Paterno', required=True)
    Amaterno = fields.Char(string='Apellido Materno', required=True)
    edad = fields.Integer(string='Edad', required=True)
    curso_id = fields.Many2one('academico.curso', string='Curso', required=True)
    nivel_id = fields.Many2one('academico.nivel', string='Nivel', required=True)
    horario_ids = fields.Many2many('academico.horario', string='Horarios', compute='_compute_horario_ids', store=True)
    
    @api.depends('curso_id', 'nivel_id')
    def _compute_horario_ids(self):
        for estudiante in self:
            if estudiante.curso_id and estudiante.nivel_id:
                estudiante.horario_ids = self.env['academico.horario'].search([
                    ('name', '=', estudiante.curso_id.id),
                    ('nivel', '=', estudiante.nivel_id.id)
                ])
            else:
                estudiante.horario_ids = False

    @api.constrains('curso_id', 'nivel_id')
    def _check_class_capacity(self):
        for estudiante in self:
            if estudiante.curso_id and estudiante.nivel_id:
                horarios = self.env['academico.horario'].search([
                    ('name', '=', estudiante.curso_id.id),
                    ('nivel', '=', estudiante.nivel_id.id)
                ])
                for horario in horarios:
                    estudiantes_en_aula = self.search_count([
                        ('curso_id', '=', estudiante.curso_id.id),
                        ('nivel_id', '=', estudiante.nivel_id.id)
                    ])
                    if estudiantes_en_aula > horario.capacidad_aula:
                        raise ValidationError(
                            f"El aula {horario.aula_id.name} para el curso {horario.name.name} y nivel {horario.nivel.name} ha alcanzado su capacidad máxima de {horario.capacidad_aula} estudiantes."
                        )
