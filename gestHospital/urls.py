from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.bienvenida, name='gestHospital-bienvenida'),
    path('historia/', views.getHistoria, name='gestHospital-historia'),
    path('noticias/', views.getNoticias, name='gestHospital-noticias'),
    path('pacientes/', views.mostrarPacientes, name='gestHospital-pacientes'),
    path('pacientes/formularios/registrar-paciente/', views.formRegPaciente, name='gestHospital-r-f-paciente'),
    path('pacientes/formularios/seleccionar-paciente/', views.formSelecPaciente, name='gestHospital-s-f-paciente'),
    path('pacientes/borrar/<str:numID>/', views.borrarPaciente, name='gestHospital-e-paciente'),
    path('pacientes/mostrar/<str:numID>/', views.mostrarPaciente, name='gestHospital-v-paciente'),
    path('ingresos/', views.mostrarIngresos, name='gestHospital-ingresos'),
    path('ingresos/formularios/registrar-ingreso/', views.formRegIngreso, name='gestHospital-r-f-ingreso'),
    path('ingresos/formularios/editar/<str:id>/', views.editarIngreso, name='gestHospital-m-f-ingreso'),
    path('ingresos/borrar/<str:id>/', views.borrarIngreso, name='gestHospital-e-ingreso'),
    path('medicos/', views.mostrarMedicos, name='gestHospital-medicos'),
    path('medicos/formularios/reservar/<str:numColegiado>/', views.reservarMedico, name='gestHospital-b-f-medico'),
    path('medicos/borrar/<str:numColegiado>/', views.borrarMedico, name='gestHospital-e-medico'),
    path('medicos/formularios/registrar-medico/', views.formRegMedico, name='gestHospital-r-f-medico'),
    path('logout/', views.logOut, name='gestHospital-logout'),
    path('login/', views.logIn, name='gestHospital-login'),
]
