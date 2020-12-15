from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.01,
    'participation_fee': 0.00,
    'doc': "",
    'participation_fee':0,
}

SESSION_CONFIGS = [
    {
        'name':'treatment_1',
        'display_name':'Treatment 1 - Groups of 2, Hard',
        'num_demo_participants': 2,
        'app_sequence': ['type_1_p1','type_1_p2','payment_info'],
    },
    {
        'name':'treatment_2',
        'display_name':'Treatment 2 - Groups of 4, Hard',
        'num_demo_participants': 4,
        'app_sequence': ['type_2_p1','type_2_p2','payment_info'],
    },
    {
        'name':'treatment_3',
        'display_name':'Treatment 3 - Groups of 4, Easy',
        'num_demo_participants': 4,
        'app_sequence': ['type_3_p1','type_3_p2','payment_info'],
    },
    {
        'name':'treatment_4',
        'display_name':'Treatment 4 - Groups of 2, Hard/Groups of 4, Hard',
        'num_demo_participants': 4,
        'app_sequence': ['type_4_p1','type_4_p2','payment_info'],
    },
    {
        'name':'treatment_5',
        'display_name':'Treatment 5 - Groups of 4, Hard/Groups of 2, Hard',
        'num_demo_participants': 4,
        'app_sequence': ['type_5_p1','type_5_p2','payment_info'],
    },
    {
        'name':'treatment_6',
        'display_name':'Treatment 6 - Groups of 4, Hard/Groups of 4, Hard, Chat',
        'num_demo_participants': 4,
        'app_sequence': ['type_6_p1','type_6_p2','payment_info'],
    },
    {
        'name':'treatment_7',
        'display_name':'Treatment 7 - Groups of 4, Hard/Groups of 4, Hard, Chat',
        'num_demo_participants': 4,
        'app_sequence': ['type_7_p1','type_7_p2','payment_info'],
    },
    {
        'name':'treatment_8',
        'display_name':'Treatment 8 - Groups of 10, Easy',
        'num_demo_participants': 10,
        'app_sequence': ['type_8_p1','type_8_p2','payment_info'],
    },
    {
        'name':'treatment_9',
        'display_name':'Treatment 9 - Groups of 4, Hard Anti-Bertrand',
        'num_demo_participants': 4,
        'app_sequence': ['type_9_p1','type_9_p2','payment_info'],
    },
]

LANGUAGE_CODE = 'en'

REAL_WORLD_CURRENCY_CODE = 'USD'

USE_POINTS = False

ROOMS = []

# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = 'peel'

# Consider '', None, and '0' to be empty/false
OTREE_PRODUCTION = '1'
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """
The treatments are included on this page.
"""

OTREE_AUTH_LEVEL = "STUDY"

SECRET_KEY = '3gpm*!9g=ye+w(7bze$2oe74h$g2d_+wpiwjc=didh3i*^2zd4' # Do Not Share

INSTALLED_APPS = ['otree']
