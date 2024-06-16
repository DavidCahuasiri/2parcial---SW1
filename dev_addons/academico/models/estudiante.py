from odoo import models, fields, api, exceptions

class Estudiante(models.Model):
    _name = 'academico.estudiante'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre completo', required=True)
    ci = fields.Char(string='Cedula de identidad', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Teléfono')
    gestion = fields.Date(string = 'Año', required=True)
    curso_id = fields.Many2one('academico.curso', string='Curso', required=True)
    nivel_id = fields.Selection(related='curso_id.nivel',string="Nivel")
    tutor_id=fields.Char(string='Nombre del tutor', required=True)
    ci_tutor=fields.Char(string='Cedula de identidad tutor', required=True)
    horario_ids = fields.One2many(related='curso_id.horario_ids', string='Horarios', readonly=True)
    @api.constrains('curso_id')
    def _check_classroom_capacity(self):
        for student in self:
            if student.curso_id:
                total_students = len(student.curso_id.estudiante_ids)
                if total_students > student.curso_id.aula_id.capacity:
                    raise exceptions.ValidationError("La capacidad del aula no es suficiente para el número de estudiantes.")

    _sql_constraints = [
        ('ci_unique', 'UNIQUE(ci)', 'La cédula de identidad debe ser única.')
    ]
