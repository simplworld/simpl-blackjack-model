"""
WSGI config for simpl_blackjack_model project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD:blackjack_model/wsgi.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackjack_model.settings")
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "simpl_blackjack_model.settings")
>>>>>>> master:simpl_blackjack_model/wsgi.py

application = get_wsgi_application()
