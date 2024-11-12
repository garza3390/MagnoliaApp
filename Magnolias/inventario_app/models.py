import json
from django.db import models
from datetime import timedelta
from django.utils import timezone

class CadenaInformacion(models.Model):
    nombre_cadena = models.CharField(max_length=50, default='Inversiones AMPM S.A.')
    cedula_juridica = models.CharField(max_length=12, default='3-102-811609')
    semana_proceso = models.CharField(max_length=9,default='2000-43')
    dia_proxima_visita = models.DateField(null=True, blank=True,default='2000-10-10')
    rango_fecha_inicio = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    rango_fecha_fin = models.DateField(default=timezone.now().strftime('%Y-%m-%d'))
    dias_de_covertura = models.IntegerField(null=True, default=21)

    def __str__(self):
        return f"{self.nombre_cadena} - Semana: {self.semana_proceso}"

    class Meta:
        db_table = 'cadena_informacion'
        managed = True
        verbose_name = "Información de Cadena"
        verbose_name_plural = "Informaciones de Cadenas"


class TiendaDetalle(models.Model):
    codigo_tienda = models.CharField(max_length=3) #
    nombre_tienda = models.CharField(max_length=30) #
    grupo_tienda = models.CharField(max_length=4, choices=[('AMPM', 'AMPM'), ('FM', 'FM')]) #
    ruta_secuencial_temp = models.CharField(max_length=3) #
    ruta_secuencial_fija = models.CharField(max_length=3) #
    horario_cierre_bodega = models.CharField(choices=[('11-12', '11-12'), ('12-13', '12-13')]) #
    fecha_ultima_visita = models.DateField(null=True, blank=True) #
    telefono = models.CharField(max_length=9, default="")
    correo = models.EmailField(max_length=50, default="")
    direccion = models.CharField(max_length=600,default="")

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



# class VisitaInventario(models.Model):

#     semana = models.CharField(max_length=9) #  Se mantiene: se obtiene de la tabla CadenaInformacion
#     codigo_tienda = models.ForeignKey(TiendaDetalle, on_delete=models.CASCADE) # se mantiene: Se ingresa por el usuario
#     fecha_visita_anterior = models.DateField(null=True, blank=True) # se mantiene: Se retroalimenta de la actual en la segunda pasada, en la primera esta en blanco
#     fecha_visita_actual = models.DateField(null=True, blank=True) # se mantiene: Se obtiene de la fecha actual
#     dias_entre_visitas = models.IntegerField(null=True, blank=True) # se mantiene: Se obtiene de la diferencia de dias  entre la fecha actual y la visita anterior
#     inventario_inicial = models.IntegerField() # Se retroalimenta de inventario_final, esta se convierte en textfield para almacenar la lista
#     existencia_informe_ampm = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     conteo_fisico = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     cantidad_por_vencer = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     devolucion = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     canje = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     inventario_sistema_ampm = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     ajuste = models.IntegerField() #  se calcula como conteo_fisico + cantidad_por_vencer + devolucion + canje - inventario_sistema_ampm, se convierte en textfield para almacenar la lista
#     promedio_diario_venta = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True) # Cantidad vendida / dias transcurridos se convierte en textfield para almacenar la lista
#     sugerido_sistema_ampm = models.IntegerField() # se convierte en textfield para almacenar la lista
#     venta_real = inventario_inicial - conteo - por_vencer - canje - devolucion
#     venta_estimada = models.DecimalField() # se calcula como: Promedio diario de venta * dias de covertura ( de la tabla CadenaInformacion),se convierte en textfield para almacenar la lista
#     minimo_display = models.IntegerField() # Ingresada por el usuario, esta se convierte en textfield para almacenar la lista
#     suma_conteo_vencer_venta_estimada = models.IntegerField(null=True, blank=True) # se calcula como Conteo fisico + Por vencer + Venta estimada, se convierte en textfield para almacenar la lista
#     cantidad_entregar = models.IntegerField(null=True, blank=True) # if venta_estimada > minimo_display: venta_estimada - conteo_fisico - por_vencer else:  minimo_display - conteo_fisico - por_vencer, esta se convierte en textfield para almacenar la lista
#     por_vencer_50_porciento = models.models.IntegerField() # se rige por esta formula =ROUND(cantidad_por_vencer*0.5 sino 0), esta se convierte en textfield para almacenar la lista
#     entregado_real = models.IntegerField() # if cantidad_entregar > 0: cantidad_entregar + por_vencer_50_porciento else: por_vencer_50_porciento, esta se convierte en textfield para almacenar la lista
#     temporada = models.IntegerField() # Proviene de los porcentaje_temporada de productos, se convierte en textfield para almacenar la lista
#     inventario_final = models.IntegerField(null=True, blank=True) # Es la suma de: Conteo fisico + Por vencer + Canje directo + cantidad_a_entregar + porcentaje_temporada , esta se convierte en textfield para almacenar la lista
#     registro_bloqueado = models.CharField(max_length=1, choices=[('S', 'Sí'), ('N', 'No')], default='N') # Ingresado por el usuario

#     def save(self, *args, **kwargs):

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"Semana: {self.semana}, Tienda: {self.codigo_tienda}, Producto: {self.codigo_producto}"

#     class Meta:
#         db_table = 'visita_inventario'
#         managed = True
#         verbose_name = "Visita de Inventario"
#         verbose_name_plural = "Visitas de Inventario"


class VisitaInventario(models.Model):
    semana = models.CharField(max_length=9)  # m Se obtiene de CadenaInformacion
    codigo_tienda = models.ForeignKey(TiendaDetalle, on_delete=models.CASCADE)  # u Ingresado por el usuario
    co_tienda = models.CharField(max_length=3,default="000")
    fecha_visita_anterior = models.DateField(null=True, blank=True)  # r Retroalimentado de la visita actual previa
    fecha_visita_actual = models.DateField(null=True, blank=True,default=timezone.now().strftime('%Y-%m-%d'))  # c Fecha actual
    dias_entre_visitas = models.IntegerField(null=True, blank=True)  # c Diferencia de días entre visitas
    inventario_inicial = models.TextField(null=True, blank=True)  # r Retroalimentado del inventario final
    existencia_informe_ampm = models.TextField()  # u Lista: Ingresada por el usuario
    conteo_fisico = models.TextField()  # u Lista: Ingresada por el usuario
    cantidad_por_vencer = models.TextField()  # u Lista: Ingresada por el usuario
    devolucion = models.TextField()  # u Lista: Ingresada por el usuario
    canje = models.TextField()  # u Lista: Ingresada por el usuario
    inventario_sistema_ampm = models.TextField()  # u Lista: Ingresada por el usuario
    ajuste = models.TextField()  # c Lista: Calculado
    venta_real = models.TextField(default="[0,0,0,0,0]") # venta_real = inventario_inicial - conteo - por_vencer - canje - devolucion
    promedio_diario_venta = models.TextField(null=True, blank=True)  # c Lista: Calculado
    sugerido_sistema_ampm = models.TextField()  # u Lista: Calculado o ingresado
    venta_estimada = models.TextField()  # c Lista: Calculado
    minimo_display = models.TextField()  # u Lista: Ingresado por el usuario
    suma_conteo_vencer_venta_estimada = models.TextField(null=True, blank=True)  # c Lista: Calculado
    cantidad_entregar = models.TextField(null=True, blank=True)  # c Lista: Calculado
    por_vencer_50_porciento = models.TextField()  # c Lista: Calculado
    entregado_real = models.TextField()  # c Lista: Calculado
    temporada = models.TextField(null=True, blank=True)  # m Calculado: basado en porcentaje_temporada de productos
    inventario_final = models.TextField(null=True, blank=True)  # c Lista: Calculado
    registro_bloqueado = models.CharField(max_length=1, choices=[('S', 'Sí'), ('N', 'No')], default='N')  # u Ingresado por el usuario

    # ajuste
    # promedio_diario_venta
    # venta_estimada
    # suma_conteo_vencer_venta_estimada
    # cantidad_entregar * mostrar en la vista con js
    # por_vencer_50_porciento
    # entregado_real
    # inventario_final * mostrar en la vista con js

    def save(self, *args, **kwargs):

        if isinstance(self.codigo_tienda,TiendaDetalle):
            self.co_tienda = self.codigo_tienda.codigo_tienda
            print("codigo tienda" + str(self.co_tienda))


        # Extraer el valor de días de cobertura desde la tabla CadenaInformacion
        cadena_info = CadenaInformacion.objects.first()
        dias_de_cobertura = int(cadena_info.dias_de_covertura) if cadena_info else 21  # Usa 21 si no hay valor

        # Realizar cálculos para cada lista de valores por product
        inv_in = json.loads(self.inventario_inicial)
        existencia_informe = json.loads(self.existencia_informe_ampm)
        conteo = json.loads(self.conteo_fisico)
        por_vencer = json.loads(self.cantidad_por_vencer)
        devolucion_nd = json.loads(self.devolucion)
        canje = json.loads(self.canje)
        inventario_sistema = json.loads(self.inventario_sistema_ampm)
        minimo_disp = json.loads(self.minimo_display)

        # Inicializar listas para almacenar resultados
        ajuste = []
        total = []
        venta = []
        promedio_venta = []
        venta_estimada = []
        suma_conteo_venta = []
        cantidad_entregar = []
        por_vencer_50 = []
        entregado_real = []
        inventario_final = []


        if self.dias_entre_visitas == None:
            self.dias_entre_visitas = 0

        # Calcular cada valor para cada producto
        for idx in range(len(existencia_informe)):

            #  Se calcula como conteo_fisico + cantidad_por_vencer + devolucion + canje - inventario_sistema_ampm

            ajuste_val = int(conteo[idx]) + int(por_vencer[idx]) + int(devolucion_nd[idx]) + int(canje[idx]) - int(inventario_sistema[idx])
            ajuste.append(ajuste_val)

            # TODO: fix the calculus of total selled

            total_val = int(conteo[idx]) + int(por_vencer[idx]) + int(devolucion_nd[idx]) + int(canje[idx]) + int(ajuste_val)
            total.append(total_val)

            # inventario_inicial - conteo - por_vencer - canje - devolucion
            venta_val =  int(inv_in[idx]) - int(conteo[idx]) - int(por_vencer[idx]) - int(canje[idx]) - int(devolucion_nd[idx])
            venta.append(venta_val)

            promedio_diario = float(venta_val) / float(self.dias_entre_visitas) if int(self.dias_entre_visitas) > 0 else 0
            promedio_venta.append(promedio_diario)

            venta_estim = round(promedio_diario * dias_de_cobertura)
            venta_estimada.append(venta_estim)

            suma_conteo_venta_val = round(int(conteo[idx]) + int(por_vencer[idx]) + venta_estim)
            suma_conteo_venta.append(suma_conteo_venta_val)


            cantidad_entregar_val = 0

            if venta_estim > int(minimo_disp[idx]):
                cantidad_entregar_val = venta_estim - int(conteo[idx]) - int(por_vencer[idx])
            else:
                cantidad_entregar_val = int(minimo_disp[idx]) - int(conteo[idx]) - int(por_vencer[idx])

            cantidad_entregar.append(cantidad_entregar_val)

            pv_50 = round(int(por_vencer[idx]) * 0.5)
            if int(por_vencer[idx]) == 1:
                pv_50 = 1
            por_vencer_50.append(pv_50)

            entregado_real_val = 0
            if cantidad_entregar_val > pv_50:
                entregado_real_val = cantidad_entregar_val + pv_50
            else:
                entregado_real_val = pv_50

            entregado_real.append(entregado_real_val)

            inventario_final_val = int(conteo[idx]) + int(por_vencer[idx]) + int(canje[idx]) + int(entregado_real_val) + float(json.loads(self.temporada)[idx])
            inventario_final.append(int(inventario_final_val))

        # Almacenar resultados comprimidos en JSON
        self.ajuste = json.dumps(ajuste)
        self.promedio_diario_venta = json.dumps(promedio_venta)
        self.venta_estimada = json.dumps(venta_estimada)
        self.suma_conteo_vencer_venta_estimada = json.dumps(suma_conteo_venta)
        self.cantidad_entregar = json.dumps(cantidad_entregar)
        self.por_vencer_50_porciento = json.dumps(por_vencer_50)
        self.entregado_real = json.dumps(entregado_real)
        self.inventario_final = json.dumps(inventario_final)
        self.venta_real = json.dumps(venta)


        # Llamar al método save original
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Semana: {self.semana}, Tienda: {self.codigo_tienda}"

    class Meta:
        db_table = 'visita_inventario'
        managed = True
        verbose_name = "Visita de Inventario"
        verbose_name_plural = "Visitas de Inventario"
