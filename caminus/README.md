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

    $ ./manage.py syncdb --migrate --noinput
    
Then, create a superuser account:

    $ ./manage.py createsuperuser

If you're using beanstalkd for webchat and server events, start it up:

    $ beanstalkd

# Updating

    ./manage.py syncdb --migrate

# Dependencies

Check out the pip-requirements file. You can install them with:

    # pip install -r pip-requirements

beanstalkd is a soft dependency. It provides webchat and server
event processing.

# Tools

There are a couple of tools that come with caminus.

## Event Stats

    $ ./manage.py event_stats

This prints out various statistics about the beanstalkd event queues.

## Flush Events

    $ ./manage.py flush_events

This flushes out all the beanstalkd event queues. All of them, not just caminus
ones. Forever. It can break things and cause lost data if you aren't careful
and know exactly why you need to flush the queue.

## Server Broadcast

    $ ./manage.py server_broadcast "Your Message"

Sends a universe-wide broadcast that shows up in all servers and active
webchats.
