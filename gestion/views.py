from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# El @login_required es un "guardia de seguridad". 
# Si no estás logueado, te manda a la página de login automáticamente.
@login_required 
def home(request):
    return render(request, 'home.html')

