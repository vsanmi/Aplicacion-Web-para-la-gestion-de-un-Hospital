from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

from django.contrib.auth.models import User
from .models import Paciente, Ingreso, Medico

GRUPO_MEDICOS = 'medicos'
GRUPO_ADMINISTRADORES = 'administradores'


class Usuario:

    nombre_usuario : str = ''
    es_administrador : bool = False
    es_medico : bool = False

    def __init__(self, nombre_usuario : str) -> None:
        try:
            usuario = User.objects.get(username=nombre_usuario)
            pass
        except ObjectDoesNotExist:
            return
            pass
        self.nombre_usuario = usuario.username
        self.es_administrador = usuario.groups.all().filter(name__iexact=GRUPO_ADMINISTRADORES).count() == 1 or usuario.is_superuser
        self.es_medico = usuario.groups.all().filter(name__iexact=GRUPO_MEDICOS).count() == 1
        pass
    
class GestorPacientes:
    
    def registrarPaciente(nombre, apellidos, numID, sexo):
        try:
            Paciente.objects.get(numID=numID)
            res = {'code': 2}
        except ObjectDoesNotExist:
            paciente = Paciente(nombre=nombre, apellidos=apellidos, numID=numID, sexo=sexo)
            try:                
                paciente.save()
                res = {'code': 0}
            except IntegrityError:
                res = {'code': 1}
        return res
    
    def buscarPaciente( numID=None ):
        if ( numID is None ):
            pacientes = list( Paciente.objects.all())
            return pacientes
            pass
        else:
            try:
                paciente = Paciente.objects.get(numID = numID)
                return paciente
                pass
            except ObjectDoesNotExist:
                return None
                pass
            pass
        pass
    
    def buscar( texto ):
        if ( texto is None):
            return None
            pass
        lista = list(Paciente.objects.filter(numID__contains=texto) | Paciente.objects.filter( nombre__contains=texto) | Paciente.objects.filter( apellidos__contains=texto) | Paciente.objects.filter( sexo__contains=texto))
        return lista        
        pass

    def borrarPaciente( numID):
        if ( numID is None ):
            return None
        
        try:
            paciente = Paciente.objects.get( numID = numID)
            paciente.delete()
            return paciente
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass
    pass
pass
    
class GestorMedicos:
    def registrarMedico(numColegiado, especialidad, password):
        try:
            Medico.objects.get(numColegiado=numColegiado)
            res = 2
        except ObjectDoesNotExist:
            medico = Medico(numColegiado=numColegiado, especialidad=especialidad)
            try:                
                medico.save()
                res = 0
            except IntegrityError:
                res = 1
        return res
        pass
    def buscarMedico( numColegiado = None ):
        if ( numColegiado is None ):
            medicos = list( Medico.objects.all())
            return medicos
            pass
        else:
            try:
                medico = Medico.objects.get(numColegiado = numColegiado)
                return medico
                pass
            except ObjectDoesNotExist:
                return None
                pass
            pass
        pass
    
    def borrarMedico( numColegiado):
        if ( numColegiado is None ):
            return None
        try:
            medico = Medico.objects.get( numColegiado = numColegiado)
            medico.delete()
            return medico
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass    
    
    def obtenerReservas( numColegiado ):
        try:
            medico = Medico.objects.get(numColegiado=numColegiado)
            return list(medico.ingresos.all())
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass

    def anularReservaMedico( numColegiado, id ):
        try:
            medico = Medico.objects.get( numColegiado=numColegiado)
            try:
                ingreso = Ingreso.objects.get( id = id)
                medico.ingresos.remove(ingreso)
                medico.save()
                pass
            except ObjectDoesNotExist:
                return 2
                pass
            pass
        except ObjectDoesNotExist:
            return 1
            pass
        return 0
        pass

        pass

    def reservarMedico( numColegiado, id ):
        try:
            medico = Medico.objects.get( numColegiado=numColegiado)
            try:
                try:
                    medico.ingresos.get(id=id)
                    return 3
                    pass
                except ObjectDoesNotExist:
                    pass
                ingreso = Ingreso.objects.get( id = id)
                medico.ingresos.add(ingreso)
                medico.save()
                pass
            except ObjectDoesNotExist:
                return 2
                pass
            pass
        except ObjectDoesNotExist:
            return 1
            pass
        return 0
        pass

    
class GestorIngresos:
    def registrarIngreso(id, paciente, edad, fechaIngreso, fechaAlta, descripcion):
        try:
            Ingreso.objects.get(id=id)
            res = {'code': 2}
        except ObjectDoesNotExist:
            ingreso = Ingreso(id=id, paciente=paciente, edad=edad, fechaIngreso=fechaIngreso, fechaAlta=fechaAlta, descripcion=descripcion)
            try:                
                ingreso.save()
                res = {'code': 0}
            except IntegrityError:
                res = {'code': 1}
        return res

    def borrarIngreso( id):
        if ( id is None ):
            return None
        
        try:
            ingreso = Ingreso.objects.get( id = id)
            ingreso.delete()
            return ingreso
            pass
        except ObjectDoesNotExist:
            return None
            pass
        pass

    def modificarIngreso(id, fechaAlta, descripcion):
        try:
            ingreso=Ingreso.objects.get( id = id)
            ingreso.fechaAlta = fechaAlta
            ingreso.descripcion = descripcion
            ingreso.save()
            return 0
            pass
        except ObjectDoesNotExist:
            return 1
            pass
        except IntegrityError:
            return 2
            pass
        pass
    
    def buscarIngreso( id=None ):
        if ( id is None ):
            ingresos = list( Ingreso.objects.all())
            return ingresos
            pass
        else:
            try:
                ingreso = Ingreso.objects.get(id = id)
                return ingreso
                pass
            except ObjectDoesNotExist:
                return None
                pass
            pass
        pass

pass

