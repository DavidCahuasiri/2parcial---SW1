from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Profesor(models.Model):
    _name = 'academico.profesor'
    _description = 'Profesor'

    name = fields.Char(string='Nombre', required=True)
    email = fields.Char(string='Email')
    telefono = fields.Char(string='Teléfono')
    materia_ids = fields.Many2many('academico.materia', string='Materias')
    nivel_id = fields.Many2one('academico.nivel', string='Nivel', required=True)
    curso_id = fields.Many2one('academico.curso', string='Curso', required=True)
    horario_ids = fields.Many2many('academico.horario', string='Horarios', compute='_compute_horario_ids', store=True)

    @api.depends('curso_id', 'nivel_id')
    def _compute_horario_ids(self):
        for profesor in self:
            if profesor.curso_id and profesor.nivel_id:
                profesor.horario_ids = self.env['academico.horario'].search([
                    ('name', '=', profesor.curso_id.id),
                    ('nivel', '=', profesor.nivel_id.id)
                ])
            else:
                profesor.horario_ids = False

    @api.constrains('curso_id', 'nivel_id')
    def _check_class_capacity(self):
        for profesor in self:
            if profesor.curso_id and profesor.nivel_id:
                horarios = self.env['academico.horario'].search([
                    ('name', '=', profesor.curso_id.id),
                    ('nivel', '=', profesor.nivel_id.id)
                ])
                for horario in horarios:
                    profesores_en_aula = self.search_count([
                        ('curso_id', '=', profesor.curso_id.id),
                        ('nivel_id', '=', profesor.nivel_id.id)
                    ])
                    if profesores_en_aula > horario.capacidad_aula:
                        raise ValidationError(
                            f"El aula {horario.aula_id.name} para el curso {horario.name.name} y nivel {horario.nivel.name} ha alcanzado su capacidad máxima de {horario.capacidad_aula} personas."
                        )
