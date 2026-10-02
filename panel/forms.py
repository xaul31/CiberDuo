from django import forms
from django.forms import inlineformset_factory

from contenido.models import Opcion, Perfil, Pregunta, TipoAmenaza
from usuarios.models import Usuario


class PanelLoginForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput())


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label='Contraseña',
        required=False,
        widget=forms.PasswordInput(render_value=False),
        help_text='Al editar, déjala en blanco para mantener la actual.',
    )

    class Meta:
        model = Usuario
        # 'password' NO va aquí: se maneja a mano en save() para no pisar el hash con un valor vacío
        fields = ['nombre', 'email', 'perfil', 'activo']

    field_order = ['nombre', 'email', 'password', 'perfil', 'activo']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.instance.pk and not password:
            raise forms.ValidationError('La contraseña es obligatoria.')
        return password

    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            usuario.set_password(password)
        if commit:
            usuario.save()
        return usuario


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['nombre', 'slug', 'descripcion', 'orden', 'activo']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class TipoAmenazaForm(forms.ModelForm):
    class Meta:
        model = TipoAmenaza
        fields = ['nombre', 'descripcion']
        widgets = {'descripcion': forms.Textarea(attrs={'rows': 3})}


class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = [
            'perfil', 'tipo_amenaza', 'enunciado', 'medio',
            'mensaje_simulado', 'explicacion', 'puntos', 'orden', 'activa',
        ]
        widgets = {
            'enunciado': forms.Textarea(attrs={'rows': 3}),
            'mensaje_simulado': forms.Textarea(attrs={'rows': 3}),
            'explicacion': forms.Textarea(attrs={'rows': 3}),
        }


class OpcionBaseFormSet(forms.BaseInlineFormSet):
    """Mínimo 2 opciones y exactamente 1 correcta."""

    def clean(self):
        super().clean()
        if any(self.errors):
            return
        activas = [
            f.cleaned_data
            for f in self.forms
            if f.cleaned_data and not f.cleaned_data.get('DELETE', False)
        ]
        if len(activas) < 2:
            raise forms.ValidationError('Agrega al menos 2 opciones.')
        if sum(1 for d in activas if d.get('es_correcta')) != 1:
            raise forms.ValidationError('Debe haber exactamente 1 opción correcta.')


OpcionFormSet = inlineformset_factory(
    Pregunta,
    Opcion,
    formset=OpcionBaseFormSet,
    fields=['texto', 'es_correcta', 'retroalimentacion', 'orden'],
    extra=3,
    can_delete=True,
    widgets={'retroalimentacion': forms.TextInput()},
)