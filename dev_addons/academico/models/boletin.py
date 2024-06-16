 
from odoo import models, fields, api


class Boletin(models.Model):
    _name = 'academico.boletin'
    _description = 'Boletín de Notas'

    estudiante_id = fields.Many2one('academico.estudiante', string='Estudiante', required=True)
    curso_id = fields.Many2one('academico.curso', string='Curso', compute='_compute_curso', store=True)
    
    nivel_id = fields.Selection(related='curso_id.nivel',string='Nivel')
    nota_ids = fields.One2many('academico.nota', 'boletin_id', string='Notas', store=True)
    estado_aprobacion = fields.Char(string='Estado de Aprobación', compute='_compute_estado_aprobacion', store=True)
    promedio = fields.Float(string='Promedio', compute='_compute_promedio', store=True)
 # Restricción para permitir solo un boletín por estudiante
    _sql_constraints = [
        ('estudiante_uniq', 'UNIQUE(estudiante_id)', 'Ya existe un boletín para este estudiante.'),
    ]
    @api.depends('promedio')
    def _compute_estado_aprobacion(self):
        for boletin in self:
            boletin.estado_aprobacion = 'Aprobado' if boletin.promedio >= 51 else 'Reprobado'
    @api.depends('estudiante_id')
    def _compute_curso(self):
        for boletin in self:
            boletin.curso_id = boletin.estudiante_id.curso_id if boletin.estudiante_id else False
    

    @api.depends('nota_ids.nota')
    def _compute_promedio(self):
        for boletin in self:
            total_notas = sum(boletin.nota_ids.mapped('nota'))
            boletin.promedio = total_notas / len(boletin.nota_ids) if boletin.nota_ids else 0.0

    @api.onchange('estudiante_id')
    def _onchange_estudiante_id(self):
        if self.estudiante_id:
            self.curso_id = self.estudiante_id.curso_id.id
        else:
            self.curso_id = False
    @api.onchange('estudiante_id')
    def _onchange_estudiante_id(self):
        if self.estudiante_id:
            notas_del_estudiante = self.env['academico.nota'].search([('estudiante_id', '=', self.estudiante_id.id)])
            self.nota_ids = [(6, 0, notas_del_estudiante.ids)]
    
    notas_materias_trimestres = fields.Text(string='Notas', compute='_compute_notas_materias_trimestres', store=True)
    notas_id= fields.Text(string='Notas', compute='_notas', store=True)
    materias_id= fields.Text(string='Materias', compute='_materias', store=True)
    trimestres_id = fields.Text(string='Trimestre', compute='_trimestre', store=True)
    @api.depends('nota_ids')
    def _compute_curso(self):
        for boletin in self:
            boletin.curso_id = boletin.estudiante_id.curso_id if boletin.estudiante_id else False

    @api.depends('nota_ids')
    def _compute_promedio(self):
        for boletin in self:
            total_notas = sum(boletin.nota_ids.mapped('nota'))
            boletin.promedio = total_notas / len(boletin.nota_ids) if boletin.nota_ids else 0.0

    # @api.depends('nota_ids')
    # def _compute_notas_materias_trimestres(self):
    #     for boletin in self:
    #         notas_materias_trimestres = []
    #         for nota in boletin.nota_ids:
    #             notas_materias_trimestres.append(f"{nota.materia_id.name}: {nota.nota} - Trimestre {nota.trimestre}")
    #         boletin.notas_materias_trimestres = '\n'.join(notas_materias_trimestres)
            
    @api.depends('nota_ids')
    def _notas(self):
        for boletin in self:
            notas_id = []
            for nota in boletin.nota_ids:
                notas_id.append(f" {nota.nota} ")
            boletin.notas_id = '\n'.join(notas_id)
            
    @api.depends('nota_ids')
    def _materias(self):
        for boletin in self:
            materias_id = []
            for nota in boletin.nota_ids:
                materias_id.append(f" {nota.materia_id.name} ")
            boletin.materias_id = '\n'.join(materias_id)
    
    @api.depends('nota_ids')
    def _trimestre(self):
        for boletin in self:
            trimestres_id = []
            for nota in boletin.nota_ids:
                trimestres_id.append(f" {nota.trimestre} Trimestre ")
            boletin.trimestres_id = '\n'.join(trimestres_id)
            
    