# Caminus

This is the source code for the minecraft community Caminus.

http://camin.us

# Installation

    ./manage.py syncdb --migrate

Answer "no" when prompted to create a superuser. The tables for the local app
have not been created yet, and will cause saving a user to fail, as we
automatically create profiles and currency accounts when a new User is saved.

    ./manage.py createsuperuser

# Updating

    ./manage.py syncdb --migrate

That *hopefully* should be it.
