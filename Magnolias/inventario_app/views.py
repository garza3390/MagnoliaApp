import json
from django.http import Http404
from django.shortcuts import render, redirect
from .models import CadenaInformacion, TiendaDetalle, ProductoDetalle, VisitaInventario
from .forms import CadenaInformacionForm, TiendaDetalleForm, ProductoDetalleForm, VisitaInventarioForm
from django.utils import timezone
from django.contrib import messages
from datetime import datetime


def comprobate(request):
    print("Comprobando que todas las tiendas estén bien...")
    visitas = VisitaInventario.objects.all()
    productos = ProductoDetalle.objects.all()
    obj = json.dumps([0 for p in productos])
    proceed = True
    not_visited = []

    if len(visitas) == 0:
        messages.warning(request, f'La lista de visitas se encuentra vacía.')
        proceed = False
    
    for v in visitas:

        if v.registro_bloqueado != "S":
            not_visited.append(f'{v.co_tienda}:{v.codigo_tienda.nombre_tienda}\n')
            proceed = False
            
    
    if proceed:
        messages.success(request, 'Todos los registros estan bloqueados.')
        messages.info(request, 'Procediendo con el restablecimiento de los datos de las visitas.')
        try:
            for v in visitas:
                v.fecha_visita_anterior = v.fecha_visita_actual
                v.inventario_inicial = v.inventario_final
                v.existencia_informe_ampm = obj
                v.conteo_fisico = obj
                v.cantidad_por_vencer = obj
                v.devolucion = obj
                v.canje = obj
                v.inventario_sistema_ampm = obj
                v.ajuste = obj
                v.promedio_diario_venta = obj
                v.sugerido_sistema_ampm = obj
                v.venta_estimada = obj
                v.minimo_display = obj
                v.suma_conteo_vencer_venta_estimada = obj
                v.cantidad_entregar = obj
                v.por_vencer_50_porciento = obj
                v.entregado_real = obj
                v.temporada = obj
                v.inventario_final = obj
                v.registro_bloqueado = 'N'
                v.save()

        except:
            messages.error(request, f'Hubo un error tratando de restablecer los datos.')
    else:
        messages.info(request, f'No todas las tiendas han sido visitadas.')
        all_tiendas_message = "Tiedas que no han sido visitadas:\n"
        for m in not_visited:
            all_tiendas_message += m
        messages.warning(request, all_tiendas_message)
        
        return redirect("seleccionar_tienda")

    return redirect("seleccionar_tienda")

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

    contexto = {
        'fecha_actual': timezone.now(),
    }
    
    if request.method == 'POST':
        tienda_id = request.POST.get('tienda_id')
        return redirect('registrar_visita_inventario', tienda_id=tienda_id)
    return render(request, 'seleccionar_tienda.html',contexto)

def registrar_visita_inventario(request, tienda_id):
    cadena_info = CadenaInformacion.objects.first()
    semana_actual = cadena_info.semana_proceso
    fecha_actual = timezone.now()

    try:
        tienda = TiendaDetalle.objects.get(codigo_tienda=tienda_id)
    except TiendaDetalle.DoesNotExist:
        messages.info(request, f'Tienda no encontrada')
        raise Http404("Tienda no encontrada")
    
    productos = ProductoDetalle.objects.all()
    dias_de_cobertura = cadena_info.dias_de_covertura if cadena_info else 21

    # Comprobar si ya existe una visita de inventario para esta tienda y semana
    try:
        visita_existente = VisitaInventario.objects.get(co_tienda=tienda_id, semana=semana_actual)
        primera_vez = False

       
        
        fecha_visita_anterior = datetime.combine(visita_existente.fecha_visita_anterior, datetime.min.time())

        inv_inicial = visita_existente.inventario_inicial

        dias_entre_visitas = (fecha_actual.date() - fecha_visita_anterior.date()).days if fecha_visita_anterior else None


    except VisitaInventario.DoesNotExist:

        primera_vez = True
        fecha_visita_anterior = None
        inv_inicial = [0 for p in productos]
        dias_entre_visitas = None

    # Datos iniciales

    
    messages.info(request, f'Primera vez: {primera_vez}')

    if request.method == 'POST':
        # Obtener datos comunes (primer registro y subsecuentes)
        inv_i = []
        existencia_ampm = []
        conteo = []
        por_vencer = []
        devolucion = []
        canje = []  
        inventario_ampm = []
        sugerido_ampm = []
        minimo_disp = []

        for producto in productos:
            inv_i.append(int(request.POST.get(f'inventario_inicial_{producto.id}', 0)))
            existencia_ampm.append(int(request.POST.get(f'existencia_ampm_{producto.id}', 0)))
            conteo.append(int(request.POST.get(f'conteo_fisico_{producto.id}', 0)))
            por_vencer.append(int(request.POST.get(f'por_vencer_{producto.id}', 0)))
            devolucion.append(int(request.POST.get(f'devolucion_{producto.id}', 0)))
            canje.append(int(request.POST.get(f'canje_{producto.id}', 0)))
            inventario_ampm.append(int(request.POST.get(f'inventario_ampm_{producto.id}', 0)))
            sugerido_ampm.append(int(request.POST.get(f'sugerido_ampm_{producto.id}', 0)))
            minimo_disp.append(int(request.POST.get(f'minimo_display_{producto.id}', 0)))

        # Para la primera vez, capturamos todos los campos iniciales
        if primera_vez:
            
            

            # Crear un nuevo registro de inventario
            visita = VisitaInventario(
                semana=semana_actual,
                codigo_tienda=tienda,
                fecha_visita_anterior=tienda.fecha_ultima_visita,
                fecha_visita_actual=fecha_actual,
                dias_entre_visitas=dias_entre_visitas,
                inventario_inicial=json.dumps(inv_i),
                existencia_informe_ampm=json.dumps(existencia_ampm),
                conteo_fisico=json.dumps(conteo),
                cantidad_por_vencer=json.dumps(por_vencer),
                devolucion=json.dumps(devolucion),
                canje=json.dumps(canje),
                inventario_sistema_ampm=json.dumps(inventario_ampm),
                sugerido_sistema_ampm = json.dumps(sugerido_ampm),
                minimo_display=json.dumps(minimo_disp),
                temporada=json.dumps([float(p.porcentaje_temporada) for p in productos]),
                registro_bloqueado = 'S' if request.POST.get('registro_bloqueado') else 'N'
            )
            visita.save()
            return redirect('seleccionar_tienda')  # Redirigimos tras guardar

        else:
            # Actualizar datos de una visita subsecuente
            visita_existente.semana = semana_actual
            visita_existente.fecha_visita_actual = fecha_actual
            visita_existente.dias_entre_visitas = dias_entre_visitas

            visita_existente.conteo_fisico = json.dumps(conteo)
            visita_existente.existencia_informe_ampm=json.dumps(existencia_ampm)
            visita_existente.cantidad_por_vencer = json.dumps(por_vencer)
            visita_existente.devolucion = json.dumps(devolucion)
            visita_existente.canje = json.dumps(canje)
            visita_existente.inventario_sistema_ampm=json.dumps(inventario_ampm)
            visita_existente.sugerido_sistema_ampm = json.dumps(sugerido_ampm)
            visita_existente.minimo_display = json.dumps(minimo_disp)
            visita_existente.temporada=json.dumps([float(p.porcentaje_temporada) for p in productos])
    
            visita_existente.registro_bloqueado = 'S' if request.POST.get('registro_bloqueado') else 'N'
            
            visita_existente.save()
            return redirect('seleccionar_tienda')  # Redirigimos tras guardar
        
    
        
    context  = {
        'tienda': tienda,
        'productos': productos,
        'fecha_actual': fecha_actual,
        'dias_de_cobertura': dias_de_cobertura,
        'semana_actual': semana_actual,
        'primera_vez': primera_vez,
        'fecha_visita_anterior': fecha_visita_anterior,
        'inventario_inicial': inv_inicial,
        'dias_entre_visitas': dias_entre_visitas,
        'precios_productos' : [p.valor_con_iva for p in productos]
    }
    rb = False
    if not primera_vez:
        if visita_existente.registro_bloqueado == "S":
            rb = True
    context["rb"] = rb


    if not primera_vez:
        all_data = zip(productos,
                    json.loads(visita_existente.inventario_inicial),
                    json.loads(visita_existente.existencia_informe_ampm),
                    json.loads(visita_existente.conteo_fisico),
                    json.loads(visita_existente.cantidad_por_vencer),
                    json.loads(visita_existente.devolucion),
                    json.loads(visita_existente.canje),
                    json.loads(visita_existente.ajuste),
                    json.loads(visita_existente.inventario_sistema_ampm),
                    json.loads(visita_existente.sugerido_sistema_ampm),
                    json.loads(visita_existente.minimo_display),
                    json.loads(visita_existente.cantidad_entregar),
                    json.loads(visita_existente.entregado_real)
                                )
        context['all_data'] = all_data
        context['final_d'] = json.loads(visita_existente.devolucion)
        context['final_e'] = json.loads(visita_existente.entregado_real)
        
        




    # Renderizar el formulario adecuado según sea la primera vez o no
    return render(request, 'registrar_visita_inventario.html', context)
