from django.contrib import admin
from .models import Departamento, UnidadMedida, Marca, Proveedor, Empleado, Articulo, Solicitud, OrdenCompra

admin.site.register(Departamento)
admin.site.register(UnidadMedida)
admin.site.register(Marca)
admin.site.register(Proveedor)
admin.site.register(Empleado)
admin.site.register(Articulo)
admin.site.register(Solicitud)
admin.site.register(OrdenCompra)