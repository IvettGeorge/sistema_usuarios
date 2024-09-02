#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import random
import string
from django.contrib.auth import get_user_model

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistema_usuarios.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()



Usuario = get_user_model()

def generar_nombre_usuario_unico():
    while True:
        nombre_usuario = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        if not Usuario.objects.filter(username=nombre_usuario).exists():
            return nombre_usuario

# Crear 30 usuarios
for i in range(30):
    nombre_usuario = generar_nombre_usuario_unico()
    email = f"user{i}@ejemplo.com"
    password = "password123"  

   
    Usuario.objects.create_user(
        username=nombre_usuario,
        email=email,
        password=password,
        first_name=f"Nombre{i}",
        last_name=f"Apellido{i}",
        is_active=True  
    )

print("30 usuarios han sido creados exitosamente.")
