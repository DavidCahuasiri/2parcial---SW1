from odoo import models, fields, api, exceptions

class Aula(models.Model):
    _name = 'academico.aula'
    _description = 'Aula'

    name = fields.Char(string='Aula', required=True)
    capacity = fields.Integer(string='Capacidad')

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Ya existe un aula con ese numero, asigne otro numero para el aula.'),
        ('capacity_positive', 'CHECK(capacity > 0)', 'La capacidad del aula debe ser un número positivo.')
    ]

    @api.constrains('capacity')
    def _check_capacity(self):
        for aula in self:
            if aula.capacity <= 0:
                raise exceptions.ValidationError("La capacidad del aula debe ser un número positivo.")
