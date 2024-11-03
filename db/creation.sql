CREATE TABLE cadena_informacion (
    nombre_cadena VARCHAR(50) NOT NULL DEFAULT 'Inversiones AMPM S.A.',
    cedula_juridica CHAR(12) NOT NULL DEFAULT '3-102-811609',
    semana_proceso CHAR(9) NOT NULL,
    dia_proxima_visita DATE,
    rango_fecha_inicio DATE NOT NULL DEFAULT '2024-11-03',
    rango_fecha_fin DATE NOT NULL DEFAULT '2024-11-09'
);

CREATE TABLE tienda_detalle (
    codigo_tienda CHAR(3) NOT NULL,
    nombre_tienda VARCHAR(30) NOT NULL,
    grupo_tienda VARCHAR(4) CHECK (grupo_tienda IN ('AMPM', 'FM')),
    ruta_secuencial_temp CHAR(3),
    ruta_secuencial_fija CHAR(3),
    horario_cierre_bodega TIME CHECK (horario_cierre_bodega IN ('11:00', '12:00', '12:00', '13:00')),
    fecha_ultima_visita DATE,
    telefono CHAR(9),
    correo VARCHAR(30),
    direccion VARCHAR(60)
);


CREATE TABLE producto_detalle (
    codigo_producto CHAR(5) NOT NULL,
    nombre_producto VARCHAR(30) NOT NULL,
    codigo_barras CHAR(13) UNIQUE,
    valor_sin_iva NUMERIC(12, 6),
    iva NUMERIC(5, 6),
    valor_con_iva NUMERIC(12, 2),
    porcentaje_merma NUMERIC(5, 2),
    porcentaje_temporada NUMERIC(5, 2)
);

CREATE TABLE visita_inventario (
    semana CHAR(9) NOT NULL,
    ruta_secuencial CHAR(3) NOT NULL,
    codigo_tienda CHAR(3) NOT NULL,
    codigo_producto CHAR(5) NOT NULL,
    fecha_visita_anterior DATE,
    fecha_visita_actual DATE,
    dias_entre_visitas SMALLINT,
    inventario_inicial SMALLINT,
    existencia_informe_ampm SMALLINT,
    conteo_fisico SMALLINT,
    cantidad_por_vencer SMALLINT,
    devolucion SMALLINT,
    canje SMALLINT,
    inventario_sistema_ampm SMALLINT,
    diferencia SMALLINT CHECK (diferencia BETWEEN -999 AND 999),
    promedio_diario_venta NUMERIC(8, 6),
    sugerido_sistema_ampm SMALLINT,
    venta_estimada_magnolias SMALLINT,
    minimo_display SMALLINT,
    suma_conteo_canje_venta SMALLINT,
    cantidad_entregar SMALLINT,
    entregado_real SMALLINT,
    inventario_final SMALLINT,
    registro_bloqueado CHAR(1) CHECK (registro_bloqueado IN ('S', 'N')),
    PRIMARY KEY (semana, ruta_secuencial, codigo_tienda, codigo_producto)
);
