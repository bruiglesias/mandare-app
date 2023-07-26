from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models
from . import forms


# Register your models here.
@admin.register(models.Profissional)
class ProfissionalAdmin(UserAdmin):
    add_form = forms.CustomProfissionalCreateForm
    list_display = [
        'nome',
        'email',
        'especialidade',
        'celular',
        'estado',
        'cidade'
    ]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {
         'fields': ('nome', 'foto_perfil', 'especialidade', 'data_nascimento', 'celular')}),
        ('Localização', {'fields': ('pais', 'estado', 'cidade')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'foto_perfil',
        'data_nascimento',
        'especialidade',
        'data_cadastro',
        'profissional',
        'diagnostico'
    ]


@admin.register(models.Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'profissional',
        'numero_sessoes',
        'numero_tentativas',
    ]

    def get_profissional(self, obj):
        return obj.programa.profissional.username

    get_profissional.short_description = 'profissional'


@admin.register(models.ProgramaPaciente)
class ProgramaPacienteAdmin(admin.ModelAdmin):

    list_display = [
        'programa',
        'paciente',
        'numero_sessoes',
        'numero_tentativas'
    ]

    def numero_sessoes(self, obj):
        return obj.programa.numero_sessoes

    def numero_tentativas(self, obj):
        return obj.programa.numero_tentativas

    numero_sessoes.short_description = 'numero_sessoes'
    numero_tentativas.short_description = 'numero_tentativas'


@admin.register(models.Sessao)
class SessaoAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'programa',
        'paciente'
    ]

    def paciente(self, obj):
        return obj.programa.paciente.nome

    paciente.short_description = 'paciente'


@admin.register(models.Tentativa)
class TentativaAdmin(admin.ModelAdmin):
    list_display = [
        'nome',
        'programa',
        'sessao',
        'situacao',
        'paciente'
    ]

    def paciente(self, obj):
        return obj.sessao.programa.paciente.nome

    def programa(self, obj):
        return obj.sessao.programa.programa.nome

    programa.short_description = 'programa'
    paciente.short_description = 'paciente'


admin.site.site_header = 'Administração Somare'
