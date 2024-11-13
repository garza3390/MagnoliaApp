import os
from django.utils import timezone
from datetime import datetime

from inventario_app.models import TiendaDetalle, VisitaInventario,CadenaInformacion

def cargar_inventarios():

    cadena = None
    cadena_semana = ""
    f_actual = timezone.now()
    try:
        cadena = CadenaInformacion.objects.first()
        cadena_semana = cadena.semana_proceso
    except:
        print("Aun no hay cadena de informacion")
    f_path = os.path.join(os.getcwd(),"inventario_app","data","inv_final.txt")
    # Leer los datos del archivo inv_final.txt y dividirlos en grupos de 5
    with open(f_path, 'r') as file:
        data = file.read().splitlines()

    # Verifica si el número de datos es múltiplo de 5
    if len(data) % 5 != 0:
        raise ValueError("El archivo de inventario no tiene un número de datos divisible por 5.")

    # Dividir los datos en grupos de 5
    datos_por_grupo = [data[i:i + 5] for i in range(0, len(data), 5)]

    # Obtener todas las tiendas de la base de datos
    tiendas = TiendaDetalle.objects.all()

    # Verifica si el número de grupos de datos coincide con el número de tiendas
    if len(tiendas) != len(datos_por_grupo):
        raise ValueError("El número de tiendas no coincide con el número de grupos de datos.")

    # Crear inventarios para cada tienda
    for idx, tienda in enumerate(tiendas):
        inventario_inicial = datos_por_grupo[idx]
        inventario_inicial_str = f"[{','.join(inventario_inicial)}]"


        f_anterior = datetime.combine(tienda.fecha_ultima_visita, datetime.min.time())

        d_e_visitas = (f_actual.date() - f_anterior.date()).days if f_anterior else None

        nuevo_inventario = VisitaInventario.objects.create(

            semana=cadena_semana,  # Campo por defecto
            codigo_tienda=tienda,
            co_tienda=tienda.codigo_tienda,
            fecha_visita_anterior = f_anterior,
            fecha_visita_actual=f_actual,  # Puedes modificar esto si necesitas la fecha actual
            dias_entre_visitas=d_e_visitas,
            inventario_inicial=inventario_inicial_str,
            existencia_informe_ampm="[]",
            conteo_fisico="[]",
            cantidad_por_vencer="[]",
            devolucion="[]",
            canje="[]",
            inventario_sistema_ampm="[]",
            ajuste="[]",
            venta_real = "[]",
            promedio_diario_venta="[]",
            sugerido_sistema_ampm="[]",
            venta_estimada="[]",
            minimo_display="[]",
            suma_conteo_vencer_venta_estimada="[]",
            cantidad_entregar="[]",
            por_vencer_50_porciento="[]",
            entregado_real="[]",
            temporada="[]",
            inventario_final="[]",
            registro_bloqueado='N'
        )

    print("Inventarios creados correctamente para cada tienda.")


dir = os.path.join(os.getcwd(),"inventario_app","data")
print(dir)
