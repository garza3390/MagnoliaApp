from datetime import timedelta
from django.http import Http404
from django.shortcuts import render, redirect
from .models import CadenaInformacion, TiendaDetalle, ProductoDetalle, VisitaInventario
from .forms import CadenaInformacionForm, TiendaDetalleForm, ProductoDetalleForm, VisitaInventarioForm
from django.utils import timezone

def crear_visita_inventario(request):
    if request.method == 'POST':
        form = VisitaInventarioForm(request.POST)
        if form.is_valid():
            visita = form.save(commit=False)
            visita.save()  # Calcula campos automáticos al guardar
            return redirect('edit')
    else:
        form = VisitaInventarioForm()
    return render(request, 'crear_visita_inventario.html', {'form': form})

# Vista para agregar una tienda
def agregar_tienda(request):
    if request.method == 'POST':
        form = TiendaDetalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('edit')
    else:
        form = TiendaDetalleForm()
    return render(request, 'agregar_tienda.html', {'form': form})

# Vista para agregar un producto
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoDetalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('edit')
    else:
        form = ProductoDetalleForm()
    return render(request, 'agregar_producto.html', {'form': form})

# Vista de inicio para listar opciones
def edit(request):
    return render(request, 'edit.html')

# Vista para editar CadenaInformacion
def editar_cadena_informacion(request):
    # Intentar obtener el único registro de CadenaInformacion o crearlo si no existe
    cadena_info, created = CadenaInformacion.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = CadenaInformacionForm(request.POST, instance=cadena_info)
        if form.is_valid():
            form.save()
            return redirect('edit')
    else:
        form = CadenaInformacionForm(instance=cadena_info)

    return render(request, 'editar_cadena_informacion.html', {'form': form})

def seleccionar_tienda(request):
    if request.method == 'POST':
        tienda_id = request.POST.get('tienda_id')
        return redirect('registrar_visita_inventario', tienda_id=tienda_id)
    return render(request, 'seleccionar_tienda.html')


# inventario_app/views.py

import json
from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import Http404
from django.utils import timezone
from .models import TiendaDetalle, ProductoDetalle, VisitaInventario, CadenaInformacion

def registrar_visita_inventario(request, tienda_id):
    # Datos de la tienda y semana
    semana_actual = "2024-XX-YY"  # Este es un ejemplo; puedes ajustar el formato según tu lógica.
    fecha_actual = timezone.now()

    try:
        tienda = TiendaDetalle.objects.get(codigo_tienda=tienda_id)
    except TiendaDetalle.DoesNotExist:
        raise Http404("Tienda no encontrada")

    # Datos de CadenaInformacion (por ejemplo, días de cobertura)
    cadena_info = CadenaInformacion.objects.first()
    dias_de_cobertura = cadena_info.dias_de_covertura if cadena_info else 21

    # Verificar si ya existe un registro para esta tienda y semana
    try:
        visita_existente = VisitaInventario.objects.get(codigo_tienda=tienda, semana=semana_actual)
        primera_vez = False
        inventario_anterior = json.loads(visita_existente.inventario_final)
    except VisitaInventario.DoesNotExist:
        primera_vez = True
        inventario_anterior = []

    # Obtener productos
    productos = ProductoDetalle.objects.all()

    # Inicializar listas para almacenar los resultados de cada producto
    cantidad_entregada, conteo_fisico, por_vencer, devolucion, canje_directo = [], [], [], [], []
    ajuste, total, venta, promedio_diario_venta, venta_estimada = [], [], [], [], []
    venta_conteo, inventario_final, por_vencer_50, minimo_display = [], [], [], []

    if request.method == 'POST':
        for idx, producto in enumerate(productos):
            # Obtener datos del formulario
            conteo = int(request.POST.get(f'conteo_fisico_{producto.id}', 0))
            vencer = int(request.POST.get(f'por_vencer_{producto.id}', 0))
            devolucion_nd = int(request.POST.get(f'devolucion_{producto.id}', 0))
            canje = int(request.POST.get(f'canje_directo_{producto.id}', 0))
            minimo_disp = int(request.POST.get(f'minimo_display_{producto.id}', 0))

            # Cantidad entregada depende de si es la primera vez o si existe un registro anterior
            cantidad = inventario_anterior[idx] if not primera_vez and len(inventario_anterior) > idx else 0

            # Cálculos basados en tu lógica
            ajuste_val = conteo + vencer + devolucion_nd + canje - cantidad
            total_val = conteo + vencer + devolucion_nd + canje + ajuste_val
            venta_val = cantidad - conteo - vencer - canje - devolucion_nd - ajuste_val
            dias_transcurridos = (fecha_actual - timedelta(days=13)).days  # Ejemplo; usa el cálculo correcto aquí
            promedio_venta = venta_val / dias_transcurridos if dias_transcurridos > 0 else 0
            venta_estimada_val = promedio_venta * dias_de_cobertura
            venta_conteo_val = conteo + vencer + venta_estimada_val
            entrega_final = max(venta_estimada_val, minimo_disp) - conteo - vencer
            por_vencer_50_val = round(vencer * 0.5)
            cantidad_entregar = max(entrega_final + por_vencer_50_val, por_vencer_50_val)

            # Almacenar resultados en listas
            cantidad_entregada.append(cantidad)
            conteo_fisico.append(conteo)
            por_vencer.append(vencer)
            devolucion.append(devolucion_nd)
            canje_directo.append(canje)
            ajuste.append(ajuste_val)
            total.append(total_val)
            venta.append(venta_val)
            promedio_diario_venta.append(promedio_venta)
            venta_estimada.append(venta_estimada_val)
            venta_conteo.append(venta_conteo_val)
            inventario_final.append(total_val + cantidad_entregar)
            por_vencer_50.append(por_vencer_50_val)
            minimo_display.append(minimo_disp)

        # Guardar las listas comprimidas como strings JSON en la base de datos
        visita = VisitaInventario(
            semana=semana_actual,
            ruta_secuencial="A-01",  # Define según tu formato
            codigo_tienda=tienda,
            fecha_visita_anterior=fecha_actual - timedelta(days=dias_transcurridos),
            fecha_visita_actual=fecha_actual,
            cantidad_entregada=json.dumps(cantidad_entregada),
            conteo_fisico=json.dumps(conteo_fisico),
            por_vencer=json.dumps(por_vencer),
            devolucion=json.dumps(devolucion),
            canje_directo=json.dumps(canje_directo),
            ajuste=json.dumps(ajuste),
            total=json.dumps(total),
            venta=json.dumps(venta),
            promedio_diario_venta=json.dumps(promedio_diario_venta),
            venta_estimada=json.dumps(venta_estimada),
            venta_conteo=json.dumps(venta_conteo),
            inventario_final=json.dumps(inventario_final),
            por_vencer_50_porciento=json.dumps(por_vencer_50),
            minimo_display=json.dumps(minimo_display)
        )
        visita.save()

        return redirect('index')  # Redirigir tras guardar

    return render(request, 'inventario_app/registrar_visita_inventario.html', {
        'tienda': tienda,
        'productos': productos,
        'fecha_entrega_anterior': "07/Oct/2024",  # Ejemplo, se puede extraer de la base de datos
        'fecha_actual': fecha_actual.strftime("%d/%b/%Y"),
        'dias_transcurridos': dias_transcurridos,
        'dias_de_cobertura': dias_de_cobertura
    })
