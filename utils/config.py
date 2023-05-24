import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

# Discord
prefix = config.get('Discord', 'prefix').split(", ")
admin_role = config.get('Discord', 'admin_role')

# APIs


#Logging
log_channel = config.get('Logging', 'log_channel')
log_level = [
    eval(config.get('Logging', 'log_debug')),       # debug
    eval(config.get('Logging', 'log_info')),        # info
    eval(config.get('Logging', 'log_warnings')),    # warnings
    eval(config.get('Logging', 'log_errors'))       # errors
]

