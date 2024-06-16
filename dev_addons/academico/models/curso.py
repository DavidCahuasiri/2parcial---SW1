from odoo import models, fields, api, exceptions

class Curso(models.Model):
    _name = 'academico.curso'
    _description = 'Curso'

    name = fields.Char(string='Curso', required=True)
    nivel = fields.Selection([
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria')
    ], string='Nivel', required=True)
    materia_ids = fields.Many2many('academico.materia', string='Materias', required=True)
    aula_id = fields.Many2one('academico.aula', string='Aula', required=True)
    estudiante_ids = fields.One2many('academico.estudiante', 'curso_id', string='Estudiantes', readonly=True)
    profesor_id = fields.One2many('academico.profesor', 'curso_id', string='Profesor', readonly=True)
    horario_ids = fields.One2many('academico.horario', 'name', string='Horarios')
    _sql_constraints = [
        ('aula_curso_nivel_uniq', 'unique(aula_id, nivel)', 'Ya existe un curso en esta aula con el mismo nivel.'),
    ]

    @api.constrains('aula_id', 'nivel')
    def _check_aula_nivel(self):
        for curso in self:
            if curso.aula_id and curso.nivel:
                cursos_otra_aula_nivel = self.search([
                    ('aula_id', '!=', curso.aula_id.id),
                    ('nivel', '=', curso.nivel),
                    ('id', '!=', curso.id),
                ])
                if cursos_otra_aula_nivel:
                    raise exceptions.ValidationError(
                        "Ya existe un curso con el mismo nivel en otra aula."
                    )

    @api.constrains('materia_ids')
    def _check_materias(self):
        for curso in self:
            if not curso.materia_ids:
                raise exceptions.ValidationError("Debe asignar al menos una materia al curso.")
