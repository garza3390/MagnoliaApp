from django.urls import path
from . import views

urlpatterns = [
    path('edit/', views.edit, name='edit'),
    path('editar_cadena_informacion/', views.editar_cadena_informacion, name='editar_cadena_informacion'),
    path('crear_visita_inventario/', views.crear_visita_inventario, name='crear_visita_inventario'),
    path('agregar_tienda/', views.agregar_tienda, name='agregar_tienda'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('registrar_visita_inventario/<str:tienda_id>/', views.registrar_visita_inventario, name='registrar_visita_inventario'),
    path('comprobate/',views.comprobate, name = 'comprobate'),
    path('', views.seleccionar_tienda, name='seleccionar_tienda')
]
