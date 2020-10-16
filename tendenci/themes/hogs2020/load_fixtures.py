############################################################################################
## Replaces "load_tendenci_defaults"
##
## That is DO NOT run"
##
##  python manage.py load_tendenci_defaults
##
## as this loads the tendenci demo site which is far richer and bloated for the purposes of a HoGS demo.
##
## Instead run this, it will load the tehem specific fixtures but also site defaults.
##
## After an instatll with a clean database:
##
## python manage.py initial_migrate   # To create the empty tables
## python manage.py deploy            # To create the basic site-settings in the database
## python manage.py createsuperuser  --username admin  # TO create the first user.
##
## The fixtures we load here expect the superuser to be called admin and have ID of 1.
##
## NOT python manage.py load_tendenci_defaults   # This is what we are replacig
##
## INSTEAD:
##
## In the Django rot direcory (where manage.py is)
##
## python themes/hogs2020/load_fixtures.py
##
## Then enable it with:
##
## python manage.py set_theme hogs2020

import subprocess, os

MANAGE = 'manage.py'
THEME_DIR = 'themes/hogs2020'

def load_data(fixture):
    subprocess.run(['python', MANAGE,  'loaddata', os.path.join(THEME_DIR, fixture)])

############################################################################################
# A minimal set of fixtures to demonstrate a HOGS site

# Minimal entities (org, commitees and memberships)
# "initial_migrate" creates one entity called Tendenci already.
# So this fixture shoudl define grousp 2 and up that we find useful. 
# We can rename Tendenci group HoGS in using the web interface later. 
load_data('fixtures/default_entities.json')

# Minimal user groups (commitee and members)
# "initial_migrate" creates one user group called Tendenci already.
# So this fixture shoudl define grousp 2 and up that we find useful. 
# We can rename Tendenci group HoGS in using the web interface later. 
load_data('fixtures/default_user_groups.json')

# A single user, on committee and member, as a demo.
load_data('fixtures/default_auth_user.json')

# Defines payement methods  that HoGS supports
load_data('fixtures/default_paymentmethod.json')

# Defines event types, and various other event related things and
# creates a single event on Jan 1 2021 as a demo.
load_data('fixtures/default_events.json')

# Creates a single demo article.
load_data('fixtures/default_articles.json')

# Creates a couple of simple demo pages (for the navs)
load_data('fixtures/default_pages.json')

# Defines membership types that HoGS supports and a form and some notices.
load_data('fixtures/default_memberships.json')

# Just pares down the tendenci demo SQL queries removing useless ones.
load_data('fixtures/default_explorer.json')

############################################################################################
# The theme specifc fixtures.

# Only the boxes that our templates use
load_data('apps/boxes/fixtures/default_boxes.json')

# Only the forms that our templates use
load_data('apps/forms-builder/forms/fixtures/default_forms.json')

# Only the navs our templates use.
load_data('apps/navs/fixtures/default_navs.json')
