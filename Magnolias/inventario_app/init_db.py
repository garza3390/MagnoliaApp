import psycopg2
from datetime import datetime

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='Magnolias_inv',
    user='postgres',
    password='password',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

# Lista completa de datos a insertar (sin valores para campos con defaults)
datos_tiendas = [
    ('024', 'AM CURRIDABAT JMZ', 'AMPM', 'A05', 'A05', '11-12', '2024-10-21'),
    ('019', 'AM CURRIDABAT FRESES', 'AMPM', 'A10', 'A10', '11-12', '2024-10-21'),
    ('029', 'FM SABANILLA EL CRISTO', 'FM', 'A15', 'A15', '12-13', '2024-10-21'),
    ('089', 'FM SABANILLA ALTOS', 'FM', 'A20', 'A20', '11-12', '2024-10-21'),
    ('085', 'FM CURRIDABAT GRANADILLA', 'FM', 'A25', 'A25', '12-13', '2024-10-21'),
    ('093', 'AM CURRIDABAT GUAYABOS', 'AMPM', 'A30', 'A30', '12-13', '2024-10-21'),
    ('012', 'FM CURRIDABAT GUAYABOS', 'FM', 'A35', 'A35', '11-12', '2024-10-21'),
    ('006', 'AM CURRIDABAT CURRI', 'AMPM', 'A40', 'A40', '12-13', '2024-10-21'),
    ('014', 'AM SJ ASAMBLEA', 'AMPM', 'A65', 'A65', '11-12', '2024-10-21'),
    ('041', 'AM SJ BARRIO DENT', 'AMPM', 'A45', 'A45', '11-12', '2024-10-21'),
    ('053', 'FM SJ YOSES', 'FM', 'A50', 'A50', '11-12', '2024-10-21'),
    ('091', 'AM SJ YOSES', 'AMPM', 'A55', 'A55', '12-13', '2024-10-21'),
    ('049', 'FM SJ ESCALANTE', 'FM', 'A60', 'A60', '12-13', '2024-10-21'),
    ('087', 'FM SJ LUJAN', 'FM', 'A70', 'A70', '12-13', '2024-10-21'),
    ('004', 'AM S.FRANCISCO FARO', 'AMPM', 'A75', 'A75', '12-13', '2024-10-21'),
    ('038', 'AM S.FRANCISCO EL BOSQUE', 'AMPM', 'A80', 'A80', '11-12', '2024-10-21'),
    ('129', 'AM SJ DESAMPARADOS', 'AMPM', 'A85', 'A85', '12-13', '2024-10-21'),
    ('037', 'AM S.PEDRO OUTLET MALL', 'AMPM', 'A90', 'A90', '11-12', '2024-10-21'),
    ('013', 'AM S.PEDRO CENTRO', 'AMPM', 'A95', 'A95', '12-13', '2024-10-28'),
    ('152', 'AM S.PEDRO LA GRANJA', 'AMPM', 'A97', 'A97', '12-13', '2024-10-21'),
    ('084', 'AM CARTAGO BAILEY', 'AMPM', 'B45', 'B45', '12-13', '2024-10-22'),
    ('071', 'AM CARTAGO CORIS', 'AMPM', 'B05', 'B05', '11-12', '2024-10-22'),
    ('148', 'FM CARTAGO TOBOSI', 'FM', 'B07', 'B07', '12-13', '2024-10-22'),
    ('079', 'AM CARTAGO GUARCO', 'AMPM', 'B10', 'B10', '12-13', '2024-10-22'),
    ('140', 'AM CARTAGO PITAHAYA', 'AMPM', 'B15', 'B15', '12-13', '2024-10-22'),
    ('143', 'AM CARTAGO GUADALUPE', 'AMPM', 'B17', 'B17', '12-13', '2024-10-22'),
    ('059', 'FM CARTAGO MOLINO', 'FM', 'B20', 'B20', '11-12', '2024-10-22'),
    ('056', 'FM CARTAGO TEC', 'FM', 'B25', 'B25', '12-13', '2024-10-22'),
    ('081', 'AM CARTAGO BASILICA', 'AMPM', 'B30', 'B30', '11-12', '2024-10-22'),
    ('035', 'AM CARTAGO CENTRO', 'AMPM', 'B35', 'B35', '11-12', '2024-10-22'),
    ('121', 'AM CARTAGO OCCIDENTE', 'AMPM', 'B40', 'B40', '12-13', '2024-10-22'),
    ('075', 'AM CARTAGO TRES RIOS', 'AMPM', 'B50', 'B50', '12-13', '2024-10-28'),
    ('080', 'FM CURRIDABAT LOMAS', 'FM', 'B55', 'B55', '11-12', '2024-10-22'),
    ('142', 'FM CARTAGO AYARCO SUR', 'FM', 'B58', 'B58', '11-12', '2024-10-22'),
    ('139', 'AM CARTAGO VILLAS DE AYARCO', 'AMPM', 'B60', 'B60', '12-13', '2024-10-22'),
    ('068', 'FM CURRIDABAT PINARES O2', 'FM', 'B65', 'B65', '11-12', '2024-10-22'),
    ('015', 'FM CURRIDABAT PINARES', 'FM', 'B70', 'B70', '12-13', '2024-10-28'),
    ('126', 'AM SJ HOSPITAL', 'AMPM', 'C05', 'C05', '11-12', '2024-10-23'),
    ('016', 'AM SJ PASEO COLON', 'AMPM', 'C10', 'C10', '12-13', '2024-10-23'),
    ('034', 'AM SJ SABANA NORTE', 'AMPM', 'C15', 'C15', '11-12', '2024-10-23'),
    ('022', 'FM SJ ROHRMOSER', 'FM', 'C20', 'C20', '12-13', '2024-10-23'),
    ('009', 'AM SJ SABANA SUR', 'AMPM', 'C25', 'C25', '11-12', '2024-10-23'),
    ('131', 'FM ESCAZU BELLO HORIZONTE', 'FM', 'C30', 'C30', '12-13', '2024-10-23'),
    ('067', 'FM ESCAZU TREJOS', 'FM', 'C35', 'C35', '11-12', '2024-10-23'),
    ('130', 'AM ESCAZU PLAZA JUSO', 'AMPM', 'C40', 'C40', '11-12', '2024-10-23'),
    ('030', 'FM ESCAZU MONTE', 'FM', 'C45', 'C45', '12-13', '2024-10-23'),
    ('076', 'FM ESCAZU CENTRO', 'FM', 'C50', 'C50', '11-12', '2024-10-23'),
    ('017', 'FM ESCAZU PACO', 'FM', 'C55', 'C55', '12-13', '2024-10-23'),
    ('036', 'AM ESCAZU NATURA', 'AMPM', 'C60', 'C60', '11-12', '2024-10-23'),
    ('007', 'AM ESCAZU GUACHIPELIN', 'AMPM', 'C65', 'C65', '12-13', '2024-10-23'),
    ('063', 'FM ESCAZU METROPLAZA', 'FM', 'C70', 'C70', '11-12', '2024-10-23'),
    ('027', 'FM ESCAZU MULTIPARK', 'FM', 'C75', 'C75', '12-13', '2024-10-23'),
    ('145', 'FM ESCAZU GUACHIPELIN', 'FM', 'C80', 'C80', '12-13', '2024-10-23'),
    ('033', 'AM HEREDIA UNA', 'AMPM', 'D05', 'D05', '11-12', '2024-10-25'),
    ('045', 'AM HEREDIA SANTA LUCIA', 'AMPM', 'D10', 'D10', '11-12', '2024-10-25'),
    ('055', 'AM HEREDIA MERCEDES NORTE', 'AMPM', 'D15', 'D15', '12-13', '2024-10-25'),
    ('060', 'AM HEREDIA VEROLIS', 'AMPM', 'D20', 'D20', '12-13', '2024-10-25'),
    ('039', 'FM HEREDIA MULTIFLORES', 'FM', 'D25', 'D25', '11-12', '2024-10-25'),
    ('021', 'AM HEREDIA SAN FRANCISCO', 'AMPM', 'D30', 'D30', '12-13', '2024-10-25'),
    ('132', 'FM HEREDIA PLAZA VIZCAYA', 'FM', 'D32', 'D32', '12-13', '2024-10-25'),
    ('058', 'AM HEREDIA AURORA', 'AMPM', 'D35', 'D35', '11-12', '2024-10-25'),
    ('008', 'FM BELEN CARIARI', 'FM', 'D40', 'D40', '11-12', '2024-10-25'),
    ('020', 'AM HEREDIA CENADA', 'AMPM', 'D45', 'D45', '12-13', '2024-10-25'),
    ('043', 'AM HEREDIA LAGUNILLA', 'AMPM', 'D50', 'D50', '11-12', '2024-10-25'),
    ('010', 'AM URUCA REPRETEL', 'AMPM', 'D55', 'D55', '12-13', '2024-10-25'),
    ('028', 'FM SJ ROHRMOSER OESTE', 'FM', 'D60', 'D60', '11-12', '2024-10-25'),
    ('086', 'AM ROHRMOSER TRIANGULO', 'AMPM', 'D65', 'D65', '12-13', '2024-10-25'),
    ('144', 'FM SJ LORETO', 'FM', 'D70', 'D70', '12-13', '2024-10-25'),
    ('064', 'AM PAVAS AYA', 'AMPM', 'D75', 'D75', '11-12', '2024-10-18'),
    ('002', 'AM SABANILLA PAULINA', 'AMPM', 'E10', 'E10', '12-13', '2024-10-26'),
    ('061', 'FM S.PEDRO SABANILLA', 'FM', 'E15', 'E15', '11-12', '2024-10-26'),
    ('090', 'FM GUADALUPE EL CARMEN', 'FM', 'E20', 'E20', '11-12', '2024-10-26'),
    ('051', 'AM SJ CORONADO', 'AMPM', 'E25', 'E25', '12-13', '2024-10-26'),
    ('123', 'FM MORAVIA SYKES', 'FM', 'E30', 'E30', '12-13', '2024-10-26'),
    ('003', 'AM MORAVIA COLEGIOS', 'AMPM', 'E35', 'E35', '11-12', '2024-10-26'),
    ('062', 'AM GUADALUPE MONTELIMAR', 'AMPM', 'E40', 'E40', '11-12', '2024-10-26'),
    ('042', 'AM SJ CALLE BLANCOS', 'AMPM', 'E45', 'E45', '12-13', '2024-10-26'),
    ('072', 'AM URUCA AUTO STAR', 'AMPM', 'E50', 'E50', '12-13', '2024-10-15'),
    ('082', 'FM TIBAS VIVE', 'FM', 'E52', 'E52', '11-12', '2024-10-26'),
    ('032', 'AM SJ TIBAS', 'AMPM', 'E55', 'E55', '12-13', '2024-10-18'),
    ('066', 'AM HEREDIA SANTO DOMINGO', 'AMPM', 'E60', 'E60', '12-13', '2024-10-26'),
    ('120', 'AM HEREDIA S.ISIDRO', 'AMPM', 'E65', 'E65', '11-12', '2024-10-26'),
    ('088', 'FM HEREDIA S.RAFAEL', 'FM', 'E70', 'E70', '11-12', '2024-10-26'),
    ('040', 'FM HEREDIA S.PABLO', 'FM', 'E75', 'E75', '12-13', '2024-10-26'),
    ('047', 'AM HEREDIA RINCON DE FLORES', 'AMPM', 'E80', 'E80', '12-13', '2024-10-26'),
    ('122', 'FM S.ANA ECO PLAZA', 'FM', 'F05', 'F05', '11-12', '2024-10-28'),
    ('048', 'FM S.ANA POZOS', 'FM', 'F10', 'F10', '12-13', '2024-10-28'),
    ('018', 'FM S.ANA CRUZ ROJA', 'FM', 'F15', 'F15', '11-12', '2024-10-28'),
    ('031', 'AM S.ANA RIO ORO', 'AMPM', 'F20', 'F20', '11-12', '2024-10-28'),
    ('074', 'FM S.ANA PIEDADES', 'FM', 'F25', 'F25', '12-13', '2024-10-28'),
    ('057', 'FM SJ CIUDAD COLON', 'FM', 'F30', 'F30', '12-13', '2024-10-28'),
    ('054', 'FM S.ANA LINDORA', 'FM', 'F32', 'F32', '11-12', '2024-10-28'),
    ('078', 'AM ALAJUELA LOGICPARK', 'AMPM', 'F35', 'F35', '12-13', '2024-10-29'),
    ('065', 'FM BELEN LA RIBERA', 'FM', 'F40', 'F40', '11-12', '2024-10-29'),
    ('069', 'AM BELEN CAFETAL', 'AMPM', 'F45', 'F45', '12-13', '2024-10-29'),
    ('138', 'FM ALAJUELA PLAZA REAL', 'FM', 'F50', 'F50', '12-13', '2024-10-29'),
    ('073', 'AM ALAJUELA ESTADIO', 'AMPM', 'F55', 'F55', '11-12', '2024-10-29'),
    ('124', 'FM ALAJUELA LA TRINIDAD', 'FM', 'F57', 'F57', '12-13', '2024-10-29'),
    ('025', 'AM SJ BANCO CENTRAL', 'AMPM', 'F60', 'F60', '12-13', '2024-10-28')
]

# Insertar datos en la tabla
for tienda in datos_tiendas:
    cursor.execute('''
        INSERT INTO tienda_detalle (
            codigo_tienda, nombre_tienda, grupo_tienda, ruta_secuencial_temp,
            ruta_secuencial_fija, horario_cierre_bodega, fecha_ultima_visita,telefono,
                   correo,direccion
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s,'','','')
    ''', (
        tienda[0], tienda[1], tienda[2], tienda[3], tienda[4],
        tienda[5], datetime.strptime(tienda[6], '%Y-%m-%d')
    ))
# Lista completa de productos a insertar
datos_productos = [
    ('007-9', 'GALLETA PARA COLOREAR', '7443023470079', 1008.85, 131.15, 1140, 10.00, 0.00),
    ('014-7', 'CAJA CON GALLETAS', '7443023470147', 1579.65, 205.35, 1785, 10.00, 0.00),
    ('021-5', 'KIT CON CALLETAS PARA DECORAR', '7443023470215', 2221.24, 288.76, 2510, 10.00, 0.00),
    ('022-2', 'GALLETA DECORADA', '7443023470222', 646.02, 83.98, 730, 10.00, 0.00),
    ('032-1', 'BROWNIES CAJA 2 UNIDADES', '7443023470321', 1146.02, 148.98, 1295, 10.00, 0.00)
]

# Insertar datos en la tabla producto_detalle
for producto in datos_productos:
    cursor.execute('''
        INSERT INTO producto_detalle (
            codigo_producto, nombre_producto, codigo_barras, valor_sin_iva, iva, valor_con_iva,
            porcentaje_merma, porcentaje_temporada
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', producto)


# Confirmar la transacción
conn.commit()

# Cerrar la conexión
cursor.close()
conn.close()

print("Datos insertados correctamente.")
