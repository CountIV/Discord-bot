from configparser import ConfigParser

config = ConfigParser()
config.read('config/config.ini')


# Discord
prefix = config.get('Discord', 'prefix').split(", ")
admin_role = config.get('Discord', 'admin_role')


# Aliases
music = {}
for command in ['join', 'leave', 'play', 'clear', 'skip', 'queue', 'remove', 'loop', 'move', 'shuffle', 'playlist']:
    music[command] = config.get('Aliases', f'music_{command}').split(", ")


#Debugging
debug_channel = config.get('Debug', 'debug_channel').split(", ")
debug = config.get('Debug', 'log_debug')

