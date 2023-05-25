import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

# Discord
prefix = config.get('Discord', 'prefix').split(", ")
admin_role = config.get('Discord', 'admin_role')

# APIs
qr_code_generator = config.get('APIs', 'qr_code_generator')

#Debugging
debug_channel = config.get('Debug', 'log_channel').split(", ")
debug = config.get('Debug', 'log_debug')

