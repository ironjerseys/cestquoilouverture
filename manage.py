#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def main():
    """Run administrative tasks."""
    # Détermine l'environnement (par défaut : dev)
    environment = os.getenv('DJANGO_ENV', 'dev')  # Utilise 'dev' si DJANGO_ENV n'est pas défini
    
    # Définit le module de paramètres approprié avec un contrôle d'existence
    if environment == 'prod':
        settings_module = 'cestquoilouverture.settings.prod'
    else:
        # Vérifie si settings.dev existe
        dev_settings_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'cestquoilouverture', 
            'settings', 
            'dev.py'
        )
        if os.path.exists(dev_settings_path):
            settings_module = 'cestquoilouverture.settings.dev'
        else:
            raise FileNotFoundError(
                "Le fichier 'settings.dev.py' est manquant. "
                "Veuillez le créer ou définir DJANGO_ENV à 'prod'."
            )

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

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
