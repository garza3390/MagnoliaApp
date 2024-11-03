from datetime import timedelta
import json
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



def registrar_visita_inventario(request, tienda_id):
    semana_actual = "2024-XX"  # Define esto según el formato de tu semana actual
    fecha_actual = timezone.now()

    try:
        tienda = TiendaDetalle.objects.get(codigo_tienda=tienda_id)
    except TiendaDetalle.DoesNotExist:
        return redirect("seleccionar_tienda")

    # Comprobar si ya existe una visita de inventario para esta tienda y semana
    try:
        visita_existente = VisitaInventario.objects.get(codigo_tienda=tienda, semana=semana_actual)
        primera_vez = False
        # Descomprimir los valores para mostrar datos retroalimentados en el formulario
        fecha_visita_anterior = visita_existente.fecha_visita_actual
        inventario_inicial = json.loads(visita_existente.inventario_final)
    except VisitaInventario.DoesNotExist:
        primera_vez = True
        fecha_visita_anterior = None
        inventario_inicial = 0  # Valor inicial si es la primera visita

    # Datos iniciales
    productos = ProductoDetalle.objects.all()
    cadena_info = CadenaInformacion.objects.first()
    dias_de_cobertura = cadena_info.dias_de_covertura if cadena_info else 21  # Valor predeterminado

    if request.method == 'POST':
        # Si es la primera vez, recibir todos los datos completos
        if primera_vez:
            existencia_informe = []
            conteo = []
            por_vencer = []
            devolucion = []
            canje = []
            inventario_sistema = []
            minimo_disp = []

            for producto in productos:
                existencia_informe.append(int(request.POST.get(f'existencia_informe_{producto.id}', 0)))
                conteo.append(int(request.POST.get(f'conteo_fisico_{producto.id}', 0)))
                por_vencer.append(int(request.POST.get(f'por_vencer_{producto.id}', 0)))
                devolucion.append(int(request.POST.get(f'devolucion_{producto.id}', 0)))
                canje.append(int(request.POST.get(f'canje_{producto.id}', 0)))
                inventario_sistema.append(int(request.POST.get(f'inventario_sistema_{producto.id}', 0)))
                minimo_disp.append(int(request.POST.get(f'minimo_display_{producto.id}', 0)))

            # Guardar los valores iniciales como listas comprimidas
            visita = VisitaInventario(
                semana=semana_actual,
                codigo_tienda=tienda,
                fecha_visita_anterior=None,
                fecha_visita_actual=fecha_actual,
                dias_entre_visitas=None,
                inventario_inicial=0,
                existencia_informe_ampm=json.dumps(existencia_informe),
                conteo_fisico=json.dumps(conteo),
                cantidad_por_vencer=json.dumps(por_vencer),
                devolucion=json.dumps(devolucion),
                canje=json.dumps(canje),
                inventario_sistema_ampm=json.dumps(inventario_sistema),
                minimo_display=json.dumps(minimo_disp),
                temporada=0,
                registro_bloqueado='N'
            )
        else:
            # Para visitas subsecuentes, solo se ingresan algunos valores
            conteo = []
            por_vencer = []
            devolucion = []
            canje = []
            minimo_disp = []

            for producto in productos:
                conteo.append(int(request.POST.get(f'conteo_fisico_{producto.id}', 0)))
                por_vencer.append(int(request.POST.get(f'por_vencer_{producto.id}', 0)))
                devolucion.append(int(request.POST.get(f'devolucion_{producto.id}', 0)))
                canje.append(int(request.POST.get(f'canje_{producto.id}', 0)))
                minimo_disp.append(int(request.POST.get(f'minimo_display_{producto.id}', 0)))

            # Actualizar los valores existentes en la base de datos
            visita_existente.conteo_fisico = json.dumps(conteo)
            visita_existente.cantidad_por_vencer = json.dumps(por_vencer)
            visita_existente.devolucion = json.dumps(devolucion)
            visita_existente.canje = json.dumps(canje)
            visita_existente.minimo_display = json.dumps(minimo_disp)
            visita_existente.fecha_visita_anterior = fecha_visita_anterior
            visita_existente.fecha_visita_actual = fecha_actual
            visita_existente.dias_entre_visitas = (fecha_actual - fecha_visita_anterior).days if fecha_visita_anterior else None
            
            visita_existente.save()
            return redirect('edit')  # Redirigir tras guardar

        # Guardar los datos en el modelo en el caso de la primera visita
        if primera_vez:
            visita.save()
            return redirect('edit')

    # Renderizar el formulario adecuado según sea la primera vez o no
    return render(request, 'registrar_visita_inventario.html', {
        'tienda': tienda,
        'productos': productos,
        'fecha_actual': fecha_actual.strftime("%d/%b/%Y"),
        'dias_de_cobertura': dias_de_cobertura,
        'primera_vez': primera_vez,
        'fecha_visita_anterior': fecha_visita_anterior,
        'inventario_inicial': inventario_inicial,
    })