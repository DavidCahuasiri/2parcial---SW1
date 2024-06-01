from odoo import models,fields,api

class turno(models.Model):
    _name='academico.turno'
    _description = 'academico.profesor'

    name = fields.Char(string='Nombre', required=True)