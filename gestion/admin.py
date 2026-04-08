import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import *

# --- ACCIÓN PARA EXPORTAR A EXCEL ---
@admin.action(description='Descargar Reporte en Excel (CSV)')
def exportar_a_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="reporte_compras.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID Orden', 'Fecha', 'Departamento', 'Empleado Solicitante', 'Articulo', 'Cantidad', 'Costo Unitario', 'Total RD$'])
    
    for orden in queryset:
        departamento = orden.solicitud.empleado.departamento.nombre
        empleado = orden.solicitud.empleado.nombre
        # Recorremos todos los artículos dentro de esa orden
        for detalle in orden.detalles.all():
            costo = detalle.costo_unitario or 0
            total = detalle.cantidad * costo
            writer.writerow([orden.id, orden.fecha_orden, departamento, empleado, detalle.articulo.descripcion, detalle.cantidad, costo, total])
            
    return response

# --- VISTAS INLINE (El diseño de "Carrito") ---
class DetalleSolicitudInline(admin.TabularInline):
    model = DetalleSolicitud
    extra = 1 # Cuántas filas vacías mostrar por defecto

class DetalleOrdenCompraInline(admin.TabularInline):
    model = DetalleOrdenCompra
    extra = 0 # No mostrar filas vacías, usar las copiadas de la solicitud

# --- CONFIGURACIÓN DE PÁGINAS ---
class ArticuloAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'marca', 'unidad_medida', 'existencia', 'estado')
    list_filter = ('marca', 'unidad_medida')

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'estado', 'fecha_solicitud')
    list_filter = ('estado', 'empleado__departamento')
    inlines = [DetalleSolicitudInline] # Conectamos los artículos aquí

def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "empleado":
            # Cambia el número 2 por el ID real de tu departamento de RRHH
            kwargs["queryset"] = Empleado.objects.exclude(departamento__id=2)
            
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class OrdenCompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'fecha_orden', 'estado')
    list_filter = ('fecha_orden',)
    inlines = [DetalleOrdenCompraInline] # Conectamos los artículos aquí
    actions = [exportar_a_csv]

# --- REGISTROS ---
admin.site.register(Articulo, ArticuloAdmin)
admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(OrdenCompra, OrdenCompraAdmin)
admin.site.register(Departamento)
admin.site.register(UnidadMedida)
admin.site.register(Marca)
admin.site.register(Proveedor)
admin.site.register(Empleado)