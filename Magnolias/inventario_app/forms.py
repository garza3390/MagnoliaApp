from django import forms
from .models import CadenaInformacion, TiendaDetalle, ProductoDetalle, VisitaInventario

class CadenaInformacionForm(forms.ModelForm):
    class Meta:
        model = CadenaInformacion
        fields = '__all__'

class TiendaDetalleForm(forms.ModelForm):
    class Meta:
        model = TiendaDetalle
        fields = '__all__'
    def clean_codigo_tienda(self):
        codigo = self.cleaned_data['codigo_tienda']
        return codigo.zfill(3)

class ProductoDetalleForm(forms.ModelForm):
    class Meta:
        model = ProductoDetalle
        fields = ['codigo_producto', 'nombre_producto', 'codigo_barras', 'valor_sin_iva', 'porcentaje_merma', 'porcentaje_temporada']

class VisitaInventarioForm(forms.ModelForm):
    class Meta:
        model = VisitaInventario
        fields = [
            'fecha_visita_actual', 'existencia_informe_ampm', 'conteo_fisico', 'cantidad_por_vencer',
            'devolucion', 'canje', 'inventario_sistema_ampm', 'sugerido_sistema_ampm',
            'minimo_display', 'entregado_real'
        ]
class CadenaInformacionForm(forms.ModelForm):
    class Meta:
        model = CadenaInformacion
        fields = '__all__'