# Generated by Django 5.1.2 on 2024-11-03 22:24

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CadenaInformacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cadena', models.CharField(default='Inversiones AMPM S.A.', max_length=50)),
                ('cedula_juridica', models.CharField(default='3-102-811609', max_length=12)),
                ('semana_proceso', models.CharField(max_length=9)),
                ('dia_proxima_visita', models.DateField(blank=True, null=True)),
                ('rango_fecha_inicio', models.DateField(default=datetime.date.today)),
                ('rango_fecha_fin', models.DateField(default=datetime.date.today)),
                ('dias_de_covertura', models.IntegerField(default=21, null=True)),
            ],
            options={
                'verbose_name': 'Información de Cadena',
                'verbose_name_plural': 'Informaciones de Cadenas',
                'db_table': 'cadena_informacion',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='ProductoDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_producto', models.CharField(max_length=5)),
                ('nombre_producto', models.CharField(max_length=30)),
                ('codigo_barras', models.CharField(max_length=13, unique=True)),
                ('valor_sin_iva', models.FloatField()),
                ('iva', models.FloatField()),
                ('valor_con_iva', models.FloatField()),
                ('porcentaje_merma', models.DecimalField(decimal_places=2, max_digits=5)),
                ('porcentaje_temporada', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                'verbose_name': 'Detalle de Producto',
                'verbose_name_plural': 'Detalles de Productos',
                'db_table': 'producto_detalle',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='TiendaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_tienda', models.CharField(max_length=3)),
                ('nombre_tienda', models.CharField(max_length=30)),
                ('grupo_tienda', models.CharField(choices=[('AMPM', 'AMPM'), ('FM', 'FM')], max_length=4)),
                ('ruta_secuencial_temp', models.CharField(max_length=3)),
                ('ruta_secuencial_fija', models.CharField(max_length=3)),
                ('horario_cierre_bodega', models.CharField(choices=[('11-12', '11-12'), ('12-13', '12-13')])),
                ('fecha_ultima_visita', models.DateField(blank=True, null=True)),
                ('telefono', models.CharField(max_length=9)),
                ('correo', models.EmailField(max_length=30)),
                ('direccion', models.CharField(max_length=60)),
            ],
            options={
                'verbose_name': 'Detalle de Tienda',
                'verbose_name_plural': 'Detalles de Tiendas',
                'db_table': 'tienda_detalle',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VisitaInventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semana', models.CharField(max_length=9)),
                ('fecha_visita_anterior', models.DateField(blank=True, null=True)),
                ('fecha_visita_actual', models.DateField(blank=True, null=True)),
                ('dias_entre_visitas', models.IntegerField(blank=True, null=True)),
                ('inventario_inicial', models.IntegerField()),
                ('existencia_informe_ampm', models.TextField()),
                ('conteo_fisico', models.TextField()),
                ('cantidad_por_vencer', models.TextField()),
                ('devolucion', models.TextField()),
                ('canje', models.TextField()),
                ('inventario_sistema_ampm', models.TextField()),
                ('ajuste', models.TextField()),
                ('promedio_diario_venta', models.TextField(blank=True, null=True)),
                ('sugerido_sistema_ampm', models.TextField()),
                ('venta_estimada', models.TextField()),
                ('minimo_display', models.TextField()),
                ('suma_conteo_vencer_venta_estimada', models.TextField(blank=True, null=True)),
                ('cantidad_entregar', models.TextField(blank=True, null=True)),
                ('por_vencer_50_porciento', models.TextField()),
                ('entregado_real', models.TextField()),
                ('temporada', models.IntegerField()),
                ('inventario_final', models.TextField(blank=True, null=True)),
                ('registro_bloqueado', models.CharField(choices=[('S', 'Sí'), ('N', 'No')], default='N', max_length=1)),
                ('codigo_tienda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario_app.tiendadetalle')),
            ],
            options={
                'verbose_name': 'Visita de Inventario',
                'verbose_name_plural': 'Visitas de Inventario',
                'db_table': 'visita_inventario',
                'managed': True,
            },
        ),
    ]
