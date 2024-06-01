
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class aula(models.Model):
    _name = 'academico.aula'
    _description = 'academico.aula'

    name = fields.Char(string='Nombre', required=True)
    curso_id = fields.Many2one('academico.curso')
    nivel_id = fields.Many2one('academico.nivel')
    #turno_id = fields.Many2one('academico.turno')
    capacidad = fields.Integer(string='Capacidad')
    
    @api.constrains('name')
    def check_unique_curso(self):
        for curso in self:
            domain = [
            ('id', '!=', curso.id),
            ('name', '=', curso.name),
            
            ]
            existing_curso = self.search(domain, limit=1)
            if existing_curso:
                raise ValidationError(f"Ya existe el aula {curso.name}.")