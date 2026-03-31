from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


def validar_cedula_dominicana(value):
    cedula = str(value).replace("-", "").strip()
    
    if len(cedula) != 11 or not cedula.isdigit():
        raise ValidationError('La cédula debe tener exactamente 11 dígitos numéricos.')

    total = 0
    multiplicadores = [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]

    for i in range(11):
        calculo = int(cedula[i]) * multiplicadores[i]
        if calculo < 10:
            total += calculo
        else:
            total += (calculo // 10) + (calculo % 10)

    if total % 10 != 0:
        raise ValidationError('La cédula ingresada no es válida.')

def validar_rnc_dominicano(value):
    rnc = str(value).replace("-", "").strip()
    
    if not rnc.isdigit():
        raise ValidationError('El RNC debe contener solo números.')

    if len(rnc) == 11:
        validar_cedula_dominicana(rnc)
        return
        
    if len(rnc) != 9:
        raise ValidationError('El RNC debe tener 9 dígitos (empresas) u 11 dígitos (personas físicas).')

    # Algoritmo Módulo 11 de la DGII para RNC de 9 dígitos
    pesos = [7, 9, 8, 6, 5, 4, 3, 2]
    suma = sum(int(rnc[i]) * pesos[i] for i in range(8))
    resto = suma % 11
    
    if resto == 0:
        digito_esperado = 2
    elif resto == 1:
        digito_esperado = 1
    else:
        digito_esperado = 11 - resto
        
    if int(rnc[8]) != digito_esperado:
        raise ValidationError('El RNC de empresa ingresado no es válido según la DGII.')

# --- MODELOS (Tablas de la Base de Datos) ---

# 1. Gestión de Departamentos [cite: 8]
class Departamento(models.Model):
    nombre = models.CharField(max_length=100) # [cite: 26]
    estado = models.BooleanField(default=True) # [cite: 27]

    def __str__(self):
        return self.nombre

# 2. Gestión de Unidades de Medida [cite: 11]
class UnidadMedida(models.Model):
    descripcion = models.CharField(max_length=50) # [cite: 34]
    estado = models.BooleanField(default=True) # [cite: 35]

    def __str__(self):
        return self.descripcion

# 3. Gestión de Marcas [cite: 10]
class Marca(models.Model):
    descripcion = models.CharField(max_length=50) # [cite: 30]
    estado = models.BooleanField(default=True) # [cite: 31]

    def __str__(self):
        return self.descripcion

# 4. Gestión de Proveedores [cite: 12]
class Proveedor(models.Model):
    cedula_rnc = models.CharField(max_length=11, unique=True, validators=[validar_rnc_dominicano]) # [cite: 38]
    nombre_comercial = models.CharField(max_length=100) # [cite: 39]
    estado = models.BooleanField(default=True) # [cite: 40]

    def __str__(self):
        return f"{self.nombre_comercial} ({self.cedula_rnc})"

# 5. Gestión de Empleados [cite: 7]
class Empleado(models.Model):
    cedula = models.CharField(max_length=11, unique=True, validators=[validar_cedula_dominicana]) # [cite: 20]
    nombre = models.CharField(max_length=100) # [cite: 21]
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE) # [cite: 22]
    estado = models.BooleanField(default=True) # [cite: 23]

    def __str__(self):
        return self.nombre

# 6. Gestión de Artículos [cite: 9]
class Articulo(models.Model):
    descripcion = models.CharField(max_length=100) # [cite: 43]
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE) # [cite: 44]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # [cite: 45]
    existencia = models.IntegerField(default=0, validators=[MinValueValidator(0)]) # [cite: 46]
    estado = models.BooleanField(default=True) # [cite: 47]

    def __str__(self):
        return f"{self.descripcion} - {self.marca}"

# 7. Transaccional: Solicitud de Artículos [cite: 13, 48]
class Solicitud(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE) # [cite: 50]
    fecha_solicitud = models.DateField(auto_now_add=True) # [cite: 51]
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE) # [cite: 52]
    cantidad = models.IntegerField(validators=[MinValueValidator(1)]) # [cite: 53]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # [cite: 54]
    estado = models.CharField(max_length=20, default='Pendiente') # [cite: 55]

    def __str__(self):
        return f"Solicitud #{self.id} - {self.empleado} - {self.estado}"

# 8. Transaccional: Orden de Compra [cite: 14, 56]
class OrdenCompra(models.Model):
    solicitud = models.OneToOneField(Solicitud, on_delete=models.CASCADE) # [cite: 58]
    fecha_orden = models.DateField(auto_now_add=True) # [cite: 59]
    estado = models.BooleanField(default=True) # [cite: 60]
    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE) # [cite: 61]
    cantidad = models.IntegerField(validators=[MinValueValidator(1)]) # [cite: 62]
    unidad_medida = models.ForeignKey(UnidadMedida, on_delete=models.CASCADE) # [cite: 63]
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE) # [cite: 64, 69]
    costo_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)]) # [cite: 65, 69]

    def __str__(self):
        return f"Orden #{self.id} (Solicitud {self.solicitud.id})"