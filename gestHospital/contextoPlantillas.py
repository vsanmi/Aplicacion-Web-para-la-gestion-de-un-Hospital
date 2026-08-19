from django.http import HttpRequest

def contextoGestHospital(request: HttpRequest) -> dict:
    return {
        'gestHospital_base_html': 'gestHospital/base.html',
        'gestHospital_css':'gestHospital/gestHospital.css',
        'gestHospital_imagen_hospital' : 'gestHospital/hospital.png',
        'gestHospital_favicon' : 'gestHospital/cor.png',
        'gestHospital_icono_borrar' : 'gestHospital/trash-bin.png',
        'gestHospital_icono_mas' : 'gestHospital/ojo.png',
        'gestHospital_icono_desplegar' : 'gestHospital/conectar.png',
        'gestHospital_icono_editar' : 'gestHospital/editar.png',
        'gestHospital_icono_reservar' : 'gestHospital/reserva.png',
        'gestHospital_tabla_paciente' : 'gestHospital/tablaPacientes.html',
        'gestHospital_tabla_medico' : 'gestHospital/tablaMedicos.html',
        'gestHospital_tabla_ingreso' : 'gestHospital/tablaIngresos.html',
        'gestHospital_volver' : 'gestHospital/volver.html',
        'gestHospital_icono_ordenar' : 'gestHospital/ordenar.png',
        'gestHospital_icono_ordenar1' : 'gestHospital/sort.png',
        }
