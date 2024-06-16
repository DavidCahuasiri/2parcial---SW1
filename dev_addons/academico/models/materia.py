
from odoo import models, fields, api
class Materia(models.Model):
    _name = 'academico.materia'
    _description = 'Materia'

    name = fields.Char(string='Materia', required=True)
    profesor_id = fields.Many2one('academico.profesor', string='Profesor')
    _sql_constraints = [
        ('name_profesor_unique', 'UNIQUE(name, profesor_id)', 'La combinación de nombre de materia y profesor debe ser única.')
    ]