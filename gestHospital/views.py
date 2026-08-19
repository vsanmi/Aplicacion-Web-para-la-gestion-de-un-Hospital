from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from .forms import RegPaciente, RegIngreso, BuscarPaciente, ModificarIngreso, RegMedico, LogInUsuarios
from .Hosp import GestorPacientes, GestorIngresos, GestorMedicos
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from .models import Ingreso, Paciente
from django.db.models import Sum

NEXT_FIELD_LABEL = 'next'

BIENVENIDA = 'gestHospital/base.html'
HISTORIA   = 'gestHospital/historia.html'
NOTICIAS   = 'gestHospital/noticias.html'
REG_PACIENTE = 'gestHospital/regPaciente.html'
REG_INGRESO = 'gestHospital/regIngreso.html'
REG_MEDICO = 'gestHospital/regMedico.html'
LISTA_PACIENTES = 'gestHospital/listaPacientes.html'
LISTA_MEDICOS = 'gestHospital/listaMedicos.html'
MOSTRAR_PACIENTE = 'gestHospital/mostrarPaciente.html'
LISTA_INGRESOS = 'gestHospital/listaIngresos.html'
MOD_INGRESO = 'gestHospital/modIngreso.html'
MOSTRAR_INGRESO = 'gestHospital/mostrarIngreso.html'
RESERVAR_MEDICO = 'gestHospital/reservarMedico.html'
RESULTADO = 'gestHospital/res.html'
LOGIN = 'gestHospital/login.html'

def bienvenida( request: HttpRequest )  -> HttpResponse:
    return render (request, BIENVENIDA)

def getHistoria( request : HttpRequest ) -> HttpResponse:
    return render( request, HISTORIA )

def getNoticias( request : HttpRequest ) -> HttpResponse:
    return render( request, NOTICIAS )


def logIn( request : HttpRequest) -> HttpResponse:
    if ( request.method == 'POST'):
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            error='Por favor, habilite las cookies para continuar'
            return render(request, LOGIN, {'formulario':form, 'errorMsg':error })
        form = LogInUsuarios(request.POST)
        if ( form.is_valid()):
            nombreUsuario = form.cleaned_data['username']
            contrasenya = form.cleaned_data['password']
            usuario = authenticate(request, username=nombreUsuario, password=contrasenya)
            if ( usuario ):
                if ( request.user.is_authenticated ):
                    logout(request)
                login(request, usuario)
                if (request.user.groups.filter(name='medicos').exists()):
                    nextPage = reverse('gestHospital-b-f-medico', args=[request.user.username])
                    return redirect(nextPage)
                nextPage=request.GET.get(NEXT_FIELD_LABEL)
                if ( nextPage is None ):
                    nextPage = reverse('gestHospital-bienvenida')
                return redirect (nextPage)
            else:
                error='Nombre de usuario o contraseña incorrectos'
                return render(request, LOGIN, {'formulario':form, 'errorMsg':error })
        else:
            error="Los datos de algún campo del formulario son incorrectos"
            return render(request, LOGIN, {'formulario':form, 'errorMsg':error })
    else:
        form = LogInUsuarios()
        if ( request.GET.get('error403') is None):
            error=None
        else:
            error='Operación no permitida. Use una cuenta con permisos suficientes'
        request.session.set_test_cookie()
        return render(request, LOGIN, {'formulario':form, 'errorMsg': error })

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
def logOut( request : HttpRequest) -> HttpResponse:
    logout( request )
    return redirect ('gestHospital-bienvenida')

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.add_paciente', 'auth.add_user'], raise_exception=True)
def formRegPaciente(request : HttpRequest) -> HttpResponse:

    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Registro de un nuevo paciente"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    if (request.method == 'GET'):
        form = RegPaciente()
        return render(request, REG_PACIENTE, {'formulario': form})
        pass

    if (request.method == 'POST'):
        form = RegPaciente(request.POST)
        if (form.is_valid()):
            nombre = form.cleaned_data['nombre']
            apellidos = form.cleaned_data['apellidos']
            numID = form.cleaned_data['numID']
            sexo = form.cleaned_data['sexo']
            res = GestorPacientes.registrarPaciente(nombre, apellidos, numID, sexo)
            if (res['code'] == 0):
                texto = "Paciente con identificador "+numID+" añadida correctamente"
                op = "Registro de un nuevo paciente"
                return render(request, REG_PACIENTE, {'texto': texto, "texto_op" : op })
                pass
            else:
                error = "Error"
                if (res['code'] == 2):
                    error = 'Ya existe el paciente con identificador: '+numID
                    pass
                return render(request, REG_PACIENTE, {'formulario': form, 'errorMsg': error})
                pass
            pass
        else:
            error="Error en el formulario"
            return render(request, REG_PACIENTE, {'formulario': form, 'errorMsg': error})
            pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.add_ingreso', 'auth.add_user'], raise_exception=True)
def formRegIngreso(request : HttpRequest) -> HttpResponse:
    
    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Registro de un nuevo ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    if (request.method == 'GET'):
        form = RegIngreso()
        return render(request, REG_INGRESO, {'formulario': form})
        pass

    if (request.method == 'POST'):
        form = RegIngreso(request.POST)
        if (form.is_valid()):
            id = form.cleaned_data['id']
            paciente = form.cleaned_data['paciente']
            edad = form.cleaned_data['edad']
            fechaIngreso = form.cleaned_data['fechaIngreso']
            fechaAlta = form.cleaned_data['fechaAlta']
            descripcion = form.cleaned_data['descripcion']
            res = GestorIngresos.registrarIngreso(id, paciente, edad, fechaIngreso, fechaAlta, descripcion)
            if (res['code'] == 0):
                texto = "Ingreso con identificador "+id+" añadido correctamente"
                op = "Registro de un nuevo ingreso"
                return render(request, REG_INGRESO, {'texto': texto, "texto_op" : op })
                pass
            else:
                error = "Error"
                return render(request, REG_INGRESO, {'formulario': form, 'errorMsg': error})
                pass
            pass
        else:
            error="Error en el formulario"
            return render(request, REG_INGRESO, {'formulario': form, 'errorMsg': error})
            pass
    pass
    
@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente', 'auth.add_user'], raise_exception=True)
def formSelecPaciente(request :HttpRequest) -> HttpResponse:
    if (request.method != 'POST'):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Búsqueda de pacientes"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    form = BuscarPaciente(request.POST)
    if (form.is_valid()):
        texto = form.cleaned_data['texto']
        lista = GestorPacientes.buscar(texto)
        return render(request, LISTA_PACIENTES, {'lista': lista})
        pass
    else:
        error = "No se ha podido completar la búsqueda"
        op = "Búsqueda de pacientes"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.delete_paciente', 'auth.add_user'], raise_exception=True)
def borrarPaciente(request : HttpRequest, numID: str) -> HttpResponse:
    res = GestorPacientes.borrarPaciente(numID)
    if ( res is None):
        error = "No existe el paciente con identificador " + numID
        op = "Eliminar paciente"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        texto = "Paciente con identificador " + numID + " ha sido borrado"
        op = "Eliminar paciente"
        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente', 'auth.add_user'], raise_exception=True)
def mostrarPaciente(request : HttpRequest, numID: str) -> HttpResponse:
    res = GestorPacientes.buscarPaciente(numID)
    if ( res is None):
        error = "No existe el paciente con identificador " + numID
        op = "Buscar paciente"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        return render(request, MOSTRAR_PACIENTE, {'paciente': res })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_paciente', 'auth.add_user'], raise_exception=True)
def mostrarPacientes(request: HttpRequest) -> HttpResponse:
    if (request.method == 'GET'):
        lista = GestorPacientes.buscarPaciente()
        return render(request, LISTA_PACIENTES, {'lista': lista})
        pass

    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    op = "Búsqueda de pacientes"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
def editarIngreso(request: HttpRequest, id: str) -> HttpResponse:
    op = "Modificar un ingreso"
    if request.method == 'POST':
        form = ModificarIngreso(request.POST)
        if form.is_valid():
            fechaAlta = form.cleaned_data['fechaAlta']
            descripcion = form.cleaned_data['descripcion']
            res = GestorIngresos.modificarIngreso(id, fechaAlta, descripcion)
            if res == 0:
                texto = "El ingreso " + id + " ha sido modificado"
                return render(request, RESULTADO, {'texto': texto, "texto_op": op})
            if res == 1:
                error = "El ingreso " + id + " no existe."
                return render(request, RESULTADO, {'errorMsg': error, "texto_op": op})
            if res == 2:
                error = "Los datos no son consistentes."
                return render(request, RESULTADO, {'errorMsg': error, "texto_op": op})
        else:
            error = "Error en el formulario"
            return render(request, MOD_INGRESO, {'formulario': form, 'errorMsg': error})
    elif request.method == 'GET':
        ingreso = GestorIngresos.buscarIngreso(id)
        if ingreso is None:
            error = "El ingreso " + id + " no existe"
            return render(request, RESULTADO, {'errorMsg': error, "texto_op": op})
        inicial = {'fechaAlta': None, 'descripcion': None}
        if ingreso.fechaAlta is not None:
            inicial['fechaAlta'] = ingreso.fechaAlta
        if ingreso.descripcion is not None:
            inicial['descripcion'] = ingreso.descripcion
        form = ModificarIngreso(inicial)
        return render(request, MOD_INGRESO, {'formulario': form, 'ingreso': ingreso})
    else:
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op": op}, status=405)

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.delete_ingreso', 'auth.add_user'], raise_exception=True)
def borrarIngreso(request : HttpRequest, id:str) -> HttpResponse:
    res = GestorIngresos.borrarIngreso(id)
    if ( res is None):
        error = "No existe el ingreso del paciente " + id
        op = "Eliminar ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        texto = "El ingreso del paciente " + id + " ha sido borrado"
        op = "Eliminar ingreso"
        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_ingreso', 'auth.add_user'], raise_exception=True)
def mostrarIngresos(request: HttpRequest) -> HttpResponse:
    if (request.method == 'GET'):
        lista = GestorIngresos.buscarIngreso()
        return render(request, LISTA_INGRESOS, {'lista': lista})
        pass

    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    op = "Visualizar ingresos"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_ingreso', 'auth.add_user'], raise_exception=True)
def mostrarIngreso(request: HttpRequest, id:str) -> HttpResponse:
    res = GestorIngresos.buscarIngreso(id)
    if ( res is None):
        error = "No existe el ingreso del paciente " + id
        op = "Buscar ingreso"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        return render(request, MOSTRAR_INGRESO, {'ingreso': res })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.add_medico', 'auth.add_user'], raise_exception=True)
def formRegMedico(request: HttpRequest) -> HttpResponse:

    if ((request.method != 'GET') and (request.method != 'POST')):
        error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
        op = "Registro de un nuevo médico"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
        pass

    if (request.method == 'GET'):
        form = RegMedico()
        return render(request, REG_MEDICO, {'formulario': form})
        pass

    if (request.method == 'POST'):
        form = RegMedico(request.POST)
        if (form.is_valid()):
            numColegiado = form.cleaned_data['numColegiado']
            especialidad = form.cleaned_data['especialidad']
            password = form.cleaned_data['password']
            res = GestorMedicos.registrarMedico(numColegiado, especialidad, password)
            if (res == 0):
                texto = "Médico con número de colegiado "+numColegiado+" añadido correctamente"
                op = "Registro de un nuevo médico"
                return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
                pass
            else:
                error = "Error"
                if (res == 2):
                    error = 'Ya existe el médico con número de colegiado: '+numColegiado
                    pass
                return render(request, REG_MEDICO, {'formulario': form, 'errorMsg': error})
                pass
            pass
        else:
            error="Error en el formulario"
            return render(request, REG_MEDICO, {'formulario': form, 'errorMsg': error})
            pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.view_medico', 'auth.add_user'], raise_exception=True)
def mostrarMedicos(request: HttpRequest) -> HttpResponse:
    if (request.method == 'GET'):
        lista = GestorMedicos.buscarMedico()
        return render(request, LISTA_MEDICOS, {'lista': lista})
        pass

    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    op = "Visualizar médicos"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
@permission_required( ['gestHospital.delete_medico', 'auth.add_user'], raise_exception=True)
def borrarMedico(request:HttpRequest, numColegiado:str) -> HttpResponse:
    res = GestorMedicos.borrarMedico(numColegiado)
    if ( res is None):
        error = "No existe el médico con número de colegiado " + numColegiado
        op = "Eliminar médico"
        return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
        pass
    else:
        texto = "El médico con número de colegiado " + numColegiado + " ha sido borrado"
        op = "Eliminar médico"
        return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
        pass
    pass

@login_required(login_url=reverse_lazy('gestHospital-login'), redirect_field_name=NEXT_FIELD_LABEL)
def reservarMedico( request: HttpRequest, numColegiado:str) -> HttpResponse:
    if ( request.method == 'GET'):
        ingresos=GestorIngresos.buscarIngreso()
        ingresosReservados=GestorMedicos.obtenerReservas(numColegiado)
        numHombres = 0
        numMujeres = 0
        edadHombres = 0
        edadMujeres = 0
        for ingreso in ingresosReservados:
            if ingreso.paciente.sexo == 'H':
                edadHombres += ingreso.edad
                numHombres += 1
            elif ingreso.paciente.sexo == 'M':
                edadMujeres += ingreso.edad
                numMujeres += 1
        edadMediaHombre = edadHombres / numHombres if numHombres else 0
        edadMediaMujer = edadMujeres / numMujeres if numMujeres else 0
        for ingreso in ingresosReservados:
            ingresos.remove(ingreso)
        return render( request, RESERVAR_MEDICO, {'numColegiado':numColegiado, 'ingresos':ingresos, 'reservados':ingresosReservados, 'edadMediaMujer':edadMediaMujer, 'edadMediaHombre':edadMediaHombre})
        pass
    if (request.method == 'POST'):
        op = "Reserva de un medico"
        try:
            op = request.POST['op']
            id = request.POST['ingreso']
            pass
        except KeyError:
            error = "Formulario incorrecto. Fallo en el navegador"
            return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)
            pass
        if ( id == 'Ninguno'):
            texto = 'No se ha modificado el médico '+numColegiado
            return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
            pass
        if ( op == 'reservar'):
            res = GestorMedicos.reservarMedico(numColegiado, id)
            pass
        else:
            res = GestorMedicos.anularReservaMedico(numColegiado, id)
            pass
        if ( res == 0 ):
            texto = 'Operación completada'
            return render(request, RESULTADO, {'texto': texto, "texto_op" : op })
            pass
        else:
            if ( res == 1 ):
                error = "El médico "+numColegiado+" no existe"
                return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
                pass
            if ( res == 2):
                error = "El ingreso "+id+" no se encuentra"
                return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
                pass
            if ( res == 3 ):
                error = "El ingreso "+id+" ya tiene reservado el médico "+numColegiado
                return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op })
                pass
            pass
        pass
    error = "Operación de protocolo empleada incorrecta. Fallo en el navegador"
    return render(request, RESULTADO, {'errorMsg': error, "texto_op" : op }, status=405)

