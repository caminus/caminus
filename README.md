# Caminus

This is the source code for the minecraft community Caminus.

http://camin.us

# Installation

Caminus is designed to keep sensitive database credentials and whatnot out of settings.py. To accomplish this,
you'll need to create a local_settings.py in the same directory as settings.py. Override anything you see fit.

For example:

    TEMPLATE_DIRS = (
        "/usr/share/caminus/templates/"
    )
    
    STATCFILES_DIRS = (
        "/usr/share/caminus/static/"
    )
    
Next, install the database:

    ./manage.py syncdb --migrate --noinput
    
Finally, create a superuser account:

    ./manage.py createsuperuser

# Updating

    ./manage.py syncdb --migrate

# Dependencies

Check out the pip-requirements file. You can install them with:

    # pip install -r pip-requirements
