from django.db import models
from datetime import timedelta
from datetime import date

class CadenaInformacion(models.Model):
    nombre_cadena = models.CharField(max_length=50, default='Inversiones AMPM S.A.')
    cedula_juridica = models.CharField(max_length=12, default='3-102-811609')
    semana_proceso = models.CharField(max_length=9)
    dia_proxima_visita = models.DateField(null=True, blank=True)
    rango_fecha_inicio = models.DateField(default=date.today)
    rango_fecha_fin = models.DateField(default=date.today)
    dias_de_covertura = models.DecimalField(max_digits=2, decimal_places=2)

    def __str__(self):
        return f"{self.nombre_cadena} - Semana: {self.semana_proceso}"

    class Meta:
        db_table = 'cadena_informacion'
        managed = True
        verbose_name = "Información de Cadena"
        verbose_name_plural = "Informaciones de Cadenas"


class TiendaDetalle(models.Model):
    codigo_tienda = models.CharField(max_length=3)
    nombre_tienda = models.CharField(max_length=30)
    grupo_tienda = models.CharField(max_length=4, choices=[('AMPM', 'AMPM'), ('FM', 'FM')])
    ruta_secuencial_temp = models.CharField(max_length=3)
    ruta_secuencial_fija = models.CharField(max_length=3)
    horario_cierre_bodega = models.CharField(choices=[('11-12', '11-12'), ('12-13', '12-13')])
    fecha_ultima_visita = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=9)
    correo = models.EmailField(max_length=30)
    direccion = models.CharField(max_length=60)

    def __str__(self):
        return f"{self.nombre_tienda} ({self.codigo_tienda})"

    class Meta:
        db_table = 'tienda_detalle'
        managed = True
        verbose_name = "Detalle de Tienda"
        verbose_name_plural = "Detalles de Tiendas"


# inventario_app/models.py

from django.db import models

class ProductoDetalle(models.Model):
    codigo_producto = models.CharField(max_length=5)
    nombre_producto = models.CharField(max_length=30)
    codigo_barras = models.CharField(max_length=13, unique=True)
    valor_sin_iva = models.FloatField()
    iva = models.FloatField()  # El valor se enviará desde el formulario o se puede calcular aquí
    valor_con_iva = models.FloatField()  # Se calculará y redondeará automáticamente en el método save()
    porcentaje_merma = models.DecimalField(max_digits=5, decimal_places=2)
    porcentaje_temporada = models.DecimalField(max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        # Calcula el IVA si no ha sido proporcionado por el formulario
        self.iva = self.valor_sin_iva * 0.13
        
        # Calcula el valor con IVA y redondea al entero más cercano
        self.valor_con_iva = round(self.valor_sin_iva + self.iva)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre_producto} ({self.codigo_producto})"

    class Meta:
        db_table = 'producto_detalle'
        managed = True
        verbose_name = "Detalle de Producto"
        verbose_name_plural = "Detalles de Productos"



class VisitaInventario(models.Model):
    
    semana = models.CharField(max_length=9) #  Se mantiene: se obtiene de la tabla CadenaInformacion
    codigo_tienda = models.ForeignKey(TiendaDetalle, on_delete=models.CASCADE) # se mantiene: Se ingresa por el usuario
    fecha_visita_anterior = models.DateField(null=True, blank=True) # se mantiene: Se retroalimenta de la actual en la segunda pasada, en la primera esta en blanco
    fecha_visita_actual = models.DateField(null=True, blank=True) # se mantiene: Se obtiene de la fecha actual
    dias_entre_visitas = models.IntegerField(null=True, blank=True) # se mantiene: Se obtiene de la diferencia de dias  entre la fecha actual y la visita anterior
    inventario_inicial = models.IntegerField() # Se mantiene: se retroalimenta de inventario_final
    existencia_informe_ampm = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    conteo_fisico = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    cantidad_por_vencer = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    devolucion = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    canje = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    inventario_sistema_ampm = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    ajuste = models.IntegerField() #  se calcula como conteo_fisico + cantidad_por_vencer + devolucion + canje - inventario_sistema_ampm, se convierte en textfield para almacenar la lista
    promedio_diario_venta = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True) # Cantidad vendida / dias transcurridos se convierte en textfield para almacenar la lista
    sugerido_sistema_ampm = models.IntegerField() # se convierte en textfield para almacenar la lista
    venta_estimada = models.DecimalField() # se calcula como: Promedio diario de venta * dias de covertura ( de la tabla CadenaInformacion),se convierte en textfield para almacenar la lista
    minimo_display = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
    suma_conteo_vencer_venta_estimada = models.IntegerField(null=True, blank=True) # se calcula como Conteo fisico + Por vencer + Venta estimada, se convierte en textfield para almacenar la lista
    cantidad_entregar = models.IntegerField(null=True, blank=True) # if venta_estimada > minimo_display: venta_estimada - conteo_fisico - por_vencer else:  minimo_display - conteo_fisico - por_vencer, esta se convierte en textfield para almacenar la lista
    por_vencer_50_porciento = models.models.IntegerField() # se rige por esta formula =ROUND(cantidad_por_vencer*0.5 sino 0), esta se convierte en textfield para almacenar la lista
    entregado_real = models.IntegerField() # if cantidad_entregar > 0: cantidad_entregar + por_vencer_50_porciento else: por_vencer_50_porciento, esta se convierte en textfield para almacenar la lista
    temporada = models.IntegerField() # Proviene de los porcentaje_temporada de productos 
    inventario_final = models.IntegerField(null=True, blank=True) # Es la suma de: Conteo fisico + Por vencer + Canje directo + cantidad_a_entregar + porcentaje_temporada , esta se convierte en textfield para almacenar la lista
    registro_bloqueado = models.CharField(max_length=1, choices=[('S', 'Sí'), ('N', 'No')], default='N') # Ingresado por el usuario 

    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Semana: {self.semana}, Tienda: {self.codigo_tienda}, Producto: {self.codigo_producto}"

    class Meta:
        db_table = 'visita_inventario'
        managed = True
        verbose_name = "Visita de Inventario"
        verbose_name_plural = "Visitas de Inventario"
