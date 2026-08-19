from django import forms

from gestHospital.models import SEXO_OPCIONES, Paciente, ESPECIALIDADES, Ingreso

class RegPaciente( forms.Form ):
    nombre = forms.CharField( label='Nombre paciente', max_length=50)
    apellidos = forms.CharField( label='Apellidos paciente', max_length=50)
    numID = forms.CharField(label = 'Identificador único del paciente', max_length=20)
    sexo = forms.ChoiceField(choices=SEXO_OPCIONES)
    pass

class BuscarPaciente( forms.Form ):
    texto = forms.CharField(label = 'Texto a buscar', max_length=50)
    pass

class RegIngreso( forms.Form ):
    id = forms.CharField(label='Identificador único del ingreso', max_length=20)
    paciente = forms.ModelChoiceField( label='Paciente ingresado', queryset=Paciente.objects.all())
    edad= forms.IntegerField(label = 'Edad paciente',max_value=120)
    fechaIngreso = forms.DateField(label='Fecha de ingreso',widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    fechaAlta = forms.DateField(label='Fecha de alta',widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    descripcion = forms.CharField(label='Descripcion enfermedad', max_length=2000, required=False)
    pass

    def clean(self):
        cleaned_data = super().clean()
        descripcion = cleaned_data.get('descripcion')
        fecha_alta = cleaned_data.get('fechaAlta')

        if not descripcion and fecha_alta:
            raise forms.ValidationError('No se puede introducir una fecha de alta si la descripción está vacía.')
    
class ModificarIngreso( forms.Form ):
    fechaAlta = forms.DateField(
        label='Fecha de alta',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    descripcion = forms.CharField(label='Descripcion enfermedad', max_length=2000, required=False)
    pass

class RegMedico( forms.Form ):
    numColegiado = forms.CharField( label='Número de colegiado', max_length=100 )
    especialidad= forms.ChoiceField(choices=ESPECIALIDADES)
    password = forms.CharField( label='Contraseña', max_length=100, widget=forms.PasswordInput)
    pass

class LogInUsuarios( forms.Form):
    username = forms.CharField( label='Nombre de usuario', max_length=10, widget=forms.TextInput(attrs={'placeholder':'nombre de usuario'}))
    password = forms.CharField( label='Contraseña', max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'contraseña'}))
    pass