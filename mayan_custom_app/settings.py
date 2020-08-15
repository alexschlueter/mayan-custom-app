from mayan.settings.production import *

LOGGING = {
    'version': 1,
    'loggers': {
        'mayan_custom_app': {
            'level': 'DEBUG'
        },
        'mayan.apps.document_states': {
            'level': 'DEBUG'
        },
        'mayan.apps.metadata': {
            'level': 'DEBUG'
        }
    }
    
}