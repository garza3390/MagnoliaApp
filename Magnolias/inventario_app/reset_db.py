import psycopg2

ANYWHERE = True
# Conexión a la base de datos PostgreSQL

if not ANYWHERE:
    conn = psycopg2.connect(
        dbname='Magnolias_inv',
        user='postgres',
        password='password',
        host='localhost',
        port='5432'
    )
else:
    conn = psycopg2.connect(
        dbname='magnolias_inv',
        user='super',
        password='MagnoliasANYwhere1029',
        host='garza-4162.postgres.pythonanywhere-services.com',
        port='14162'
    )
cursor = conn.cursor()

# Lista de tablas a vaciar en el orden correcto para evitar errores de dependencia
tablas = [
    'visita_inventario',
    'producto_detalle',
    'tienda_detalle',
    'cadena_informacion'
]

# Iterar y vaciar cada tabla
for tabla in tablas:
    cursor.execute(f'TRUNCATE TABLE {tabla} RESTART IDENTITY CASCADE')
    print(f'Tabla {tabla} vaciada.')

# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Todas las tablas han sido reseteadas.")
