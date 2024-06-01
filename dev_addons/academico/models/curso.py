
            
from odoo import models,fields,api
from odoo.exceptions import ValidationError

class nivel(models.Model):
    _name = 'academico.curso'
    _description = 'academico.curso'

    name = fields.Char(string='Nombre', required=True)
    #aula_id=fields.Many2one('academico.aula')
    
    @api.constrains('name')
    def check_unique_nivel(self):
        for curso in self:
            domain = [
            ('id', '!=', curso.id),
            ('name', '=', curso.name),
            ]
            existing_curso = self.search(domain, limit=1)
            if existing_curso:
                raise ValidationError(f"Ya existe el nivel {curso.name}.")

