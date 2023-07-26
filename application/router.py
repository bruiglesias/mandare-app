from django.urls import path

from . import views as app_views

app_name = 'application'

urlpatterns = [
    path('', app_views.login_page, name='index'),
    path('autenticar', app_views.login_redirect_page, name='autenticar'),
    path('cadastro', app_views.signup_page, name='cadastro'),
    path('redirect', app_views.signup_redirect, name='redirect'),
    path('principal', app_views.main_page, name='principal'),
    path('cadastrar-programa', app_views.add_program_page,
         name='cadastrar-programa'),
    path('programa-redirect', app_views.add_program_redirect,
         name='programa-redirect'),
    path('cadastrar-paciente', app_views.add_paciente_page,
         name='cadastrar-paciente'),
    path('paciente-redirect', app_views.add_paciente_redirect,
         name='paciente-redirect'),
    path('search-paciente', app_views.search_main_page,
         name='search-paciente'),

    path('paciente/<int:paciente>', app_views.paciente_page,
         name='paciente'),

    path('paciente/<int:id>/editar', app_views.edit_paciente_page,
         name='editar-paciente'),

    path('paciente/<int:id>/redirect', app_views.edit_paciente_redirect,
         name='editar-paciente-redirect'),

    path('paciente/<int:id>/programa-cadastrar',
         app_views.add_programa_paciente, name='paciente-programa-cadastrar'),

    path('paciente/<int:id_paciente>/programa/<int:id_programa>',
         app_views.programa_paciente, name='programa-paciente'),

    path('paciente/programa/resumo',
         app_views.programa_paciente_resumo, name='paciente-programa-resumo'),

    path('paciente/programa/redirect',
         app_views.programa_paciente_redirect, name='paciente-programa-redirect'),  # noqa

     path('paciente/<int:id>/historico', app_views.historico_page, name='paciente-historico'),  # noqa

     path('historico-programa-redirect', app_views.historico_programa_redirect, name='paciente-programa-historico-redirect'),  # noqa
     path('historico-programa/<int:paciente_id>/programa/<int:programa_id>',
          app_views.resultado_historico_page, name='paciente-programa-historico'),  # noqa

     path('historico-programa/<int:paciente_id>/programa/<int:programa_id>/relatorio', app_views.resultado_historico_relatorio, name='paciente-programa-relatorio'),  # noqa

    path('sair', app_views.logout_view, name='sair'),

]
