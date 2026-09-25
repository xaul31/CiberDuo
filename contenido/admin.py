from django import forms
from django.contrib import admin

from .models import Opcion, Perfil, Pregunta, TipoAmenaza


class OpcionInlineFormSet(forms.BaseInlineFormSet):
    """Valida que la pregunta tenga al menos 2 opciones y exactamente 1 correcta."""

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

        correctas = sum(1 for d in activas if d.get('es_correcta'))
        if correctas != 1:
            raise forms.ValidationError('Debe haber exactamente 1 opción correcta.')


class OpcionInline(admin.TabularInline):
    model = Opcion
    formset = OpcionInlineFormSet
    extra = 3


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug', 'orden', 'activo')
    list_editable = ('orden', 'activo')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(TipoAmenaza)
class TipoAmenazaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('enunciado_corto', 'perfil', 'tipo_amenaza', 'medio', 'puntos', 'orden', 'activa')
    list_filter = ('perfil', 'tipo_amenaza', 'medio', 'activa')
    search_fields = ('enunciado',)
    list_editable = ('orden', 'activa')
    inlines = [OpcionInline]

    @admin.display(description='Enunciado')
    def enunciado_corto(self, obj):
        return obj.enunciado[:70]