TOKENS = {
    'OPERATIONS': {
        'plus': '+',
        'min': '-',
        'maal': '*',
        'gedeeld': '/',
        "macht": "**", # nog niet helemaal bekend in het system.
        'isgelijk': '=',
    },
    "VARIABELS": {
        'var': 'VARIABLE',
        'string': 'STRING_VARIABLE',
        'int': 'INTIGER_VARIABLE',
        'float': 'FLOAT_VARIABLE'
    },
    "SYSTEM": {
        'break': 'BREAKING_PROGRAM'
    },
    "PROCESSING":{
        #'func': "FUNCTIONS",
        #'class': 'MODEL',
    },
    "METHODS":{
        'print': "PRINTING",
        'open': 'OPENING_FILE',
        'settings': 'SETTINGS'
    }
}
SYMBOL_MAP = TOKENS['OPERATIONS'] | TOKENS['VARIABELS'] | TOKENS['SYSTEM'] | TOKENS['METHODS']
VARIABLES_TOKENS = TOKENS.get("VARIABELS")
METHODS_TOKENS = TOKENS.get('METHODS')
SYSTEM_VARIABLES = {}
REPORTS = []
ADMIN_ERRORS = {}
MAX_LINES = 10000 
NO_PRINT_SETTINGS_FILE_PATH = "no_print_settings.dll"