from odoo import models, fields, api
from odoo.exceptions import ValidationError

class horario(models.Model):
    _name = 'academico.horario'
    _description = 'academico.horario'

    materia_id = fields.Many2one('academico.materia', string='Materia', required=True)
    aula_id = fields.Many2one('academico.aula', string='Aula', required=True)
    name = fields.Many2one('academico.curso', string='Curso', related='aula_id.curso_id', readonly=True)
    nivel = fields.Many2one('academico.nivel', string='Nivel', related='aula_id.nivel_id', readonly=True)
    turno = fields.Selection([
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ], string='Turno', required=True)
    dia_semana = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
        ('sabado', 'Sábado'),
    ], string='Día de la Semana', required=True)
    hora_inicio = fields.Selection(
        [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 15)],
        string='Hora de Inicio',
        required=True
    )
    hora_fin = fields.Selection(
        [(f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}') for h in range(24) for m in range(0, 60, 15)],
        string='Hora de Fin',
        required=True
    )
    capacidad_aula = fields.Integer(string='Capacidad del Aula', related='aula_id.capacidad', store=True)

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_hora_inicio_fin(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError("La hora de inicio debe ser menor que la hora de fin.")
                
    @api.constrains('aula_id', 'dia_semana', 'hora_inicio', 'hora_fin')
    def _check_horario_conflictivo_aula(self):
        for record in self:
            conflicto_aula = self.search([
                ('id', '!=', record.id),
                ('aula_id', '=', record.aula_id.id),
                ('dia_semana', '=', record.dia_semana),
                ('hora_inicio', '<', record.hora_fin),
                ('hora_fin', '>', record.hora_inicio),
            ])
            if conflicto_aula:
                raise ValidationError("Conflicto de horarios: ya existe un horario en la misma aula en el mismo horario.")
    
    @api.constrains('dia_semana', 'hora_inicio', 'hora_fin', 'name', 'nivel')
    def _check_horario_conflictivo_curso_nivel(self):
        for record in self:
            conflicto_curso_nivel = self.search([
                ('id', '!=', record.id),
                ('dia_semana', '=', record.dia_semana),
                ('name', '=', record.name.id),
                ('nivel', '=', record.nivel.id),
                ('hora_inicio', '<', record.hora_fin),
                ('hora_fin', '>', record.hora_inicio),
            ])
            if conflicto_curso_nivel:
                raise ValidationError("Conflicto de horarios: ya existe un horario para el mismo curso y nivel en el mismo horario.")

    @api.constrains('aula_id', 'name', 'nivel')
    def _check_aula_curso_nivel(self):
        for record in self:
            if record.aula_id and record.name and record.nivel:
                conflicto_aula_curso_nivel = self.search([
                    ('id', '!=', record.id),
                    ('aula_id', '=', record.aula_id.id),
                    ('name', '!=', record.name.id),
                    ('nivel', '!=', record.nivel.id),
                ])
                if conflicto_aula_curso_nivel:
                    raise ValidationError("No se puede registrar un horario en la misma aula si el curso y el nivel son distintos.")
    
