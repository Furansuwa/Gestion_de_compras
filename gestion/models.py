from django.db import models
# Importar los validadores de Django
from django.core.validators import RegexValidator, MinValueValidator

# 1. Gestión de Departamentos
class Departamento(models.Model):
    nombre = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# 2. Gestión de Unidades de Medida
class UnidadMedida(models.Model):
    descripcion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

# 3. Gestión de Marcas
class Marca(models.Model):
    descripcion = models.CharField(max_length=50)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

# 4. Gestión de Proveedores
class Proveedor(models.Model):
    # Validador de RNC/Cédula Dominicana (9 u 11 dígitos, solo números)
    rnc_validador = RegexValidator(
        regex=r'^(\d{9}|\d{11})$',
        message='El RNC/Cédula debe tener 9 u 11 dígitos numéricos, sin guiones.'
    )
    cedula_rnc = models.CharField(max_length=11, unique=True, validators=[rnc_validador])
    nombre_comercial = models.CharField(max_length=100)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre_comercial

# 5. Gestión de Empleados
class Empleado(models.Model):
    # Validador de Cédula Dominicana (Exactamente 11 dígitos, solo números)
    cedula_validador = RegexValidator(
        regex=r'^\d{11}$',
        message='La cédula debe tener exactamente 11 dígitos numéricos, sin guiones.'
    )
    cedula = models.CharField(max_length=11, unique=True, validators=[cedula_validador])
    nombre = models.CharField(max_length=100)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

# 6. Gestión de Artículos
class Articulo(models.Model):
    descripcion = models.CharField(max_length=100)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    # La existencia no puede ser negativa
    existencia = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

# Tablas transaccionales
class Solicitud(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_solicitud = models.DateField(auto_now_add=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    # La cantidad solicitada debe ser al menos 1
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, default='Pendiente')

class OrdenCompra(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE)
    fecha_orden = models.DateField(auto_now_add=True)
    estado = models.BooleanField(default=True)
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE)
    # La cantidad debe ser al menos 1
    cantidad = models.IntegerField(validators=[MinValueValidator(1)])
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE)
    # El costo no puede ser negativo ni 0
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])