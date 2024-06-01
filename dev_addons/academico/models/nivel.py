

from odoo import models,fields,api
from odoo.exceptions import ValidationError

class nivel(models.Model):
    _name = 'academico.nivel'
    _description = 'academico.nivel'

    name = fields.Char(string='Nombre', required=True)
    #aula_id=fields.Many2one('academico.aula')
    
    @api.constrains('name')
    def check_unique_nivel(self):
        for nivel in self:
            domain = [
            ('id', '!=', nivel.id),
            ('name', '=', nivel.name),
            ]
            existing_nivel = self.search(domain, limit=1)
            if existing_nivel:
                raise ValidationError(f"Ya existe el nivel {nivel.name}.")