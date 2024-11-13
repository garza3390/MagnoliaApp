import os
from datetime import datetime

from inventario_app.models import VisitaInventario


def update_inventarios():
    # Leer las fechas del archivo ultima_visita.txt
    f_path = os.path.join(os.getcwd(), "inventario_app", "data", "ultima_visita.txt")
    with open(f_path, 'r') as file:
        fechas = file.read().splitlines()

    # Verifica si el número de fechas es múltiplo de 5
    if len(fechas) % 5 != 0:
        raise ValueError("El archivo de fechas no tiene un número de datos divisible por 5.")

    # Filtrar las fechas, seleccionando solo la primera de cada grupo de 5
    fechas_por_inventario = [fechas[i] for i in range(0, len(fechas), 5)]

    # Obtener todos los inventarios existentes
    inventarios = VisitaInventario.objects.all()

    # Verifica si el número de inventarios coincide con el número de fechas
    if len(inventarios) != len(fechas_por_inventario):
        raise ValueError("El número de inventarios no coincide con el número de fechas proporcionadas.")

    # Actualizar la fecha de última visita de cada inventario
    for idx, inventario in enumerate(inventarios):
        fecha_str = fechas_por_inventario[idx]
        # Obtener el año actual
        current_year = datetime.now().year
        # Convertir la fecha al formato yyyy-mm-dd
        fecha_ultima_visita = datetime.strptime(f"{current_year}-{fecha_str}", "%Y-%d-%b").date()

        # Actualizar el campo en el modelo
        inventario.fecha_visita_anterior = fecha_ultima_visita
        inventario.save()

    print("Fechas de última visita actualizadas correctamente.")


dir = os.path.join(os.getcwd(), "inventario_app", "data")
print(dir)
