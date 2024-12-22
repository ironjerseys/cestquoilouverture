import os

# Détermine l'environnement à partir de la variable d'environnement
environment = os.getenv('DJANGO_ENV', 'dev')

if environment == 'prod':
    from .prod import *
elif environment == 'dev':
    from .dev import *
else:
    raise ValueError(f"Unknown DJANGO_ENV: {environment}")
