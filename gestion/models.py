from django.db import models

# 1. Gestión de Departamentos [cite: 8, 24]
class Departamento(models.Model):
    nombre = models.CharField(max_length=100) # [cite: 26]
    estado = models.BooleanField(default=True) # [cite: 27]

    def __str__(self):
        return self.nombre

# 2. Gestión de Unidades de Medida [cite: 11, 32]
class UnidadMedida(models.Model):
    descripcion = models.CharField(max_length=50) # [cite: 34]
    estado = models.BooleanField(default=True) # [cite: 35]

    def __str__(self):
        return self.descripcion

# 3. Gestión de Marcas [cite: 10, 28]
class Marca(models.Model):
    descripcion = models.CharField(max_length=50) # [cite: 30]
    estado = models.BooleanField(default=True) # [cite: 31]

    def __str__(self):
        return self.descripcion

# 4. Gestión de Proveedores [cite: 12, 36]
class Proveedor(models.Model):
    cedula_rnc = models.CharField(max_length=20, unique=True) # [cite: 38]
    nombre_comercial = models.CharField(max_length=100) # [cite: 39]
    estado = models.BooleanField(default=True) # [cite: 40]

    def __str__(self):
        return self.nombre_comercial

# 5. Gestión de Empleados [cite: 7, 18]
class Empleado(models.Model):
    cedula = models.CharField(max_length=11, unique=True) # [cite: 20]
    nombre = models.CharField(max_length=100) # [cite: 21]
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE) # Conexión con Depto [cite: 22]
    estado = models.BooleanField(default=True) # [cite: 23]

    def __str__(self):
        return self.nombre

# 6. Gestión de Artículos [cite: 9, 41]
class Articulo(models.Model):
    descripcion = models.CharField(max_length=100) # [cite: 43]
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE) # Conexión con Marca [cite: 44]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # Conexión con Unidad [cite: 45]
    existencia = models.IntegerField(default=0) # [cite: 46]
    estado = models.BooleanField(default=True) # [cite: 47]

    def __str__(self):
        return self.descripcion

# Tablas transaccionales (Solicitudes y Ordenes)
class Solicitud(models.Model): # [cite: 13, 48]
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) # [cite: 50]
    fecha_solicitud = models.DateField(auto_now_add=True) # [cite: 51]
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE) # [cite: 52]
    cantidad = models.IntegerField() # [cite: 53]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # [cite: 54]
    estado = models.CharField(max_length=20, default='Pendiente') # [cite: 55]

class OrdenCompra(models.Model): # [cite: 14, 56]
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE) # Conexión directa [cite: 58]
    fecha_orden = models.DateField(auto_now_add=True) # [cite: 59]
    estado = models.BooleanField(default=True) # [cite: 60]
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE) # [cite: 61]
    cantidad = models.IntegerField() # [cite: 62]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # [cite: 63]
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2) # [cite: 65]