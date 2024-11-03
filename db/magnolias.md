# Proyecto para desarrollo de aplicación magnolias

### Datos

- Tamaño de pantalla: 2340x1080
- 
scram-sha-256


    <!-- <a href="{% url 'registrar_visita_inventario' %}" class="btn btn-primary btn-block my-2">Agregar Visita de Inventario</a> -->

# GPT

Hay que hacerle modificaciones a esta parte de la logica:


- Vista

{% extends "base.html" %}

{% block title %}Registrar Visita de Inventario{% endblock %}
{% block content %}
<h2>Registro de Visita de Inventario para Tienda {{ tienda.id }}</h2>

<div>
    <p><strong>Fecha entrega anterior:</strong> {{ fecha_entrega_anterior }}</p>
    <p><strong>Fecha actual:</strong> {{ fecha_actual }}</p>
    <p><strong>Días transcurridos:</strong> {{ dias_transcurridos }}</p>
    <p><strong>Días de cobertura:</strong> {{ dias_de_cobertura }}</p>
</div>

<form method="post">
    {% csrf_token %}
    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Productos</th>
                <th>Cantidad entregada</th>
                <th>Conteo físico</th>
                <th>Por vencer</th>
                <th>Devolución ND</th>
                <th>Canje directo</th>
                <!-- Agrega más columnas según sea necesario -->
            </tr>
        </thead>
        <tbody>
            {% for producto in productos %}
            <tr>
                <td>{{ producto.codigo_producto }}</td>
                <td><input type="number" name="cantidad_entregada_{{ producto.id }}" class="form-control" value="0"></td>
                <td><input type="number" name="conteo_fisico_{{ producto.id }}" class="form-control" value="0"></td>
                <td><input type="number" name="por_vencer_{{ producto.id }}" class="form-control" value="0"></td>
                <td><input type="number" name="devolucion_{{ producto.id }}" class="form-control" value="0"></td>
                <td><input type="number" name="canje_directo_{{ producto.id }}" class="form-control" value="0"></td>
                <!-- Agrega más campos según los valores a ingresar -->
            </tr>
            {% endfor %}
        </tbody>
    </table>
    <button type="submit" class="btn btn-primary">Guardar Visita de Inventario</button>
</form>
{% endblock %}



- backend

def registrar_visita_inventario(request, tienda_id):
    # Intentar obtener la tienda por el código de tienda (cadena de caracteres)
    try:
        tienda = TiendaDetalle.objects.get(codigo_tienda=tienda_id)
    except TiendaDetalle.DoesNotExist:
        raise Http404("Tienda no encontrada")

    productos = ProductoDetalle.objects.all()

    if request.method == 'POST':
        for producto in productos:
            conteo_fisico = int(request.POST.get(f'conteo_fisico_{producto.id}', 0))
            por_vencer = int(request.POST.get(f'por_vencer_{producto.id}', 0))
            devolucion = int(request.POST.get(f'devolucion_{producto.id}', 0))
            canje_directo = int(request.POST.get(f'canje_directo_{producto.id}', 0))
            cantidad_entregada = int(request.POST.get(f'cantidad_entregada_{producto.id}', 0))

            # Crear o actualizar el registro de visita de inventario para el producto específico
            visita = VisitaInventario(
                semana="2024-XX-YY",  # Define esto según el formato que necesitas
                ruta_secuencial="A-01",  # Modificar según sea necesario
                codigo_tienda=tienda,
                codigo_producto=producto,
                fecha_visita_anterior=timezone.now() - timedelta(days=13),  # Ejemplo de días previos
                fecha_visita_actual=timezone.now(),
                conteo_fisico=conteo_fisico,
                cantidad_por_vencer=por_vencer,
                devolucion=devolucion,
                canje=canje_directo,
                cantidad_entregada=cantidad_entregada,
                inventario_sistema_ampm=10,  # Puedes ajustar esto según tu lógica
                sugerido_sistema_ampm=5,  # Puedes ajustar esto según tu lógica
                minimo_display=5,  # Puedes ajustar esto según tu lógica
                entregado_real=cantidad_entregada
            )
            visita.save()

        return redirect('index')  # Redirige al índice después de guardar
    
    return render(request, 'registrar_visita_inventario.html', {
        'tienda': tienda,
        'productos': productos,
        'fecha_entrega_anterior': "07/Oct/2024",  # Ejemplo, se puede modificar para extraer la fecha anterior
        'fecha_actual': timezone.now().strftime("%d/%b/%Y"),
        'dias_transcurridos': 13,  # Calculado
        'dias_de_cobertura': 21  # Establecido como ejemplo
    })

- modelo

class VisitaInventario(models.Model):
    semana = models.CharField(max_length=9)
    ruta_secuencial = models.CharField(max_length=3)
    codigo_tienda = models.ForeignKey(TiendaDetalle, on_delete=models.CASCADE)
    codigo_producto = models.ForeignKey(ProductoDetalle, on_delete=models.CASCADE)
    fecha_visita_anterior = models.DateField(null=True, blank=True)
    fecha_visita_actual = models.DateField()
    dias_entre_visitas = models.PositiveIntegerField(null=True, blank=True)
    existencia_informe_ampm = models.PositiveIntegerField()
    conteo_fisico = models.PositiveIntegerField()
    cantidad_por_vencer = models.PositiveIntegerField()
    devolucion = models.PositiveIntegerField()
    canje = models.PositiveIntegerField()
    inventario_sistema_ampm = models.PositiveIntegerField()
    sugerido_sistema_ampm = models.PositiveIntegerField()
    minimo_display = models.PositiveIntegerField()
    entregado_real = models.PositiveIntegerField()
    por_vencer_50_porciento = models.models.IntegerField()
    diferencia = models.IntegerField(null=True, blank=True)
    promedio_diario_venta = models.DecimalField(max_digits=8, decimal_places=6, null=True, blank=True)
    suma_conteo_canje_venta = models.PositiveIntegerField(null=True, blank=True)
    cantidad_entregar = models.PositiveIntegerField(null=True, blank=True)
    inventario_final = models.PositiveIntegerField(null=True, blank=True)
    registro_bloqueado = models.CharField(max_length=1, choices=[('S', 'Sí'), ('N', 'No')], default='N')

    def save(self, *args, **kwargs):
        # Calcula días entre visitas si la fecha anterior existe
        if self.fecha_visita_anterior:
            self.dias_entre_visitas = (self.fecha_visita_actual - self.fecha_visita_anterior).days
        # Calcula diferencia
        self.diferencia = self.existencia_informe_ampm - self.conteo_fisico
        # Calcula promedio diario de venta
        if self.dias_entre_visitas > 0:
            self.promedio_diario_venta = self.diferencia / self.dias_entre_visitas
        # Suma de conteo, canje y venta estimada
        self.suma_conteo_canje_venta = self.conteo_fisico + self.canje + self.sugerido_sistema_ampm
        # Cantidad a entregar
        self.cantidad_entregar = max(self.minimo_display - self.conteo_fisico, 0)
        # Inventario final
        self.inventario_final = self.inventario_sistema_ampm + self.entregado_real - self.devolucion

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Semana: {self.semana}, Tienda: {self.codigo_tienda}, Producto: {self.codigo_producto}"

    class Meta:
        db_table = 'visita_inventario'
        managed = True
        verbose_name = "Visita de Inventario"
        verbose_name_plural = "Visitas de Inventario"


- modelo producto:

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

- modelo CadenaInformacion

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



la nueva logica debe cubrir una lista de puntos:

Nota que algunos campos como la fecha de

* Si es la primera vez que se hace el inventario, se debe ingresar todos los datos por primera vez, (nota que algunos campos como la temporada vienen del producto)
  

* Si es la segunda en adelante entonces se sigue la siguiente logica:

* Se debe solo modificar los campos 

Cantidad entregada: viene del historico de lo quedo la entrega pasada (de la variable inventario_final)

Conteo fisico, Por vencer, Devolucion ND, Canje son campos digitados por el usuario

Total: Es la suma de el conteo + por vencer + devolucion + canje + Ajuste

Ajuste: puede ser positivo o negativo y se calcula: como conteo + por vencer + devolucion + canje - inventario am pm

Venta: El inventario inicial (Cantidad entregada) - La existencia - Por vencer - Canje - Devolucion - Ajuste

Promedio diario de venta: Cantidad vendida / dias transcurridos, donde dias transcurridos es la resta de las fechas: Fecha entrega anterior:	07/Oct/2024, Fecha actual:	20/Oct/2024

Venta estimada: Promedio diario de venta * dias de covertura ( de la tabla CadenaInformacion)

Venta+conteo = Conteo fisico + Por vencer + Venta estimada

Entrega final: si la venta estimada es mayor que el minimo display entonces: Entrega final = Venta estimada - conteo fisico - por vencer, sino entonces Entrega final = minimo display - conteo fisico - por vencer

Por_vencer_50_porciento: se rige por esta formula =ROUND(por vencer*0.5,0) 

Minimo display : digitado por el usuario

cantidad_a_entregar: Si la entrega final es mayor que 0 entonces es: Entrega final + Por_vencer_50_porciento si no  entonces es solo igual a Por_vencer_50_porciento

Temporada: =ROUND(cantidad_a_entregar*0,0) se modifica la temporada del producto

entregado_final: 

inventario_final: Es la suma de: Conteo fisico + Por vencer + Canje directo + cantidad_a_entregar + Temporada

Fecha entrega anterior: Se retroalimenta de la fecha actual

Fecha actual es la fecha actual

Dias transcurridos: la cantidad de dias entre la fecha actual y la ultima visita

Dias de covertura: Viene de la tabla CadenaInformacion


* Como punto final nota que las variables: Cantidad entregada, Conteo fisico, Por vencer, Devolucion ND	,Canje directo,	Ajuste,	Total,	Venta,		Promedio diario de venta,		Venta estimada,suma_conteo_canje_venta,	Inventario final,	Por_vencer_50_porciento,	Minimo display,cantidad_a_entregar,Temporada (viene de los productos ),inventario_final

todos estos daatos son almacenados en listas, ya que deben almacenar esos datos por cada producto

Dime si entiendes lo que debes hacer y preguntame cualquier duda que tengas sobre la aplicacion de esta nueva logica, se bastante claro y ve paso por paso ya que es una logica algo compleja
