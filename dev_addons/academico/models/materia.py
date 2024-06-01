from odoo import models, fields, api
from odoo.exceptions import ValidationError



class materia(models.Model):
    _name = 'academico.materia'
    _description = 'academico.materia'

    name = fields.Char(string='Nombre', required=True)
    
    profesor_id = fields.Many2many('academico.profesor', string='Profesor')
    estudiante_ids = fields.Many2many('academico.estudiante', string='Estudiantes')
    
    @api.constrains('name')
    def check_unique_materia(self):
        for materia in self:
            domain = [
            ('id', '!=', materia.id),
            ('name', '=', materia.name),
            ]
            existing_materia = self.search(domain, limit=1)
            if existing_materia:
                raise ValidationError(f"Ya existe la materia {materia.name}.")