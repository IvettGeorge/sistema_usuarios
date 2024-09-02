# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroUsuarioForm
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
import random
import string
from django.contrib.auth import authenticate, login as auth_login



@login_required
def bienvenida(request):
    messages.success(request, f'¡Bienvenido {request.user.username}!')
    
    return render(request, 'bienvenida.html')

def despedida(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente. ¡Hasta luego!')
    
    return redirect('login')

def generate_unique_username():
    while True:
        username = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        if not User.objects.filter(username=username).exists():
            return username

def registro(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El email ya está en uso.')
            return redirect('registro')
        
        username = generate_unique_username()

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
       
        
        messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
        return redirect('login')
    return render(request, 'registro.html')

def usuarios_activos(request):
    try:
        sesiones_activas = Session.objects.filter(expire_date__gte=timezone.now())
        
        usuarios_id = [session.get_decoded().get('_auth_user_id') for session in sesiones_activas if session.get_decoded().get('_auth_user_id')]

        usuarios_activos = Usuario.objects.filter(id__in=usuarios_id)
        
        messages.info(request, 'Lista de usuarios activos actualizada.')

    except Exception as e:
        messages.error(request, f'Error al obtener usuarios activos: {e}')
        usuarios_activos = []

    return render(request, 'usuarios_activos.html', {'usuarios_activos': usuarios_activos})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('bienvenida')
        else:
            messages.error(request, 'Email o contraseña incorrectos.')
            return redirect('login')
    
    return render(request, 'login.html')