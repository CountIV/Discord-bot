import configparser

c = configparser.ConfigParser()
c.read('config/config.ini')


# Discord
prefix = c.get('Discord', 'prefix').split(", ")
admin_role = c.get('Discord', 'admin_role')


# APIs
qr_code_generator = c.get('APIs', 'qr_code_generator')
wikipedia_api = c.get('APIs', 'wikipedia_api')


# Aliases
music_join  = c.get('Aliases', 'music_join').split(", ")
music_leave = c.get('Aliases', 'music_leave').split(", ")
music_play  = c.get('Aliases', 'music_play').split(", ")
music_clear = c.get('Aliases', 'music_clear').split(", ")
music_skip  = c.get('Aliases', 'music_skip').split(", ")
music_queue = c.get('Aliases', 'music_queue').split(", ")

#Debugging
debug_channel = c.get('Debug', 'debug_channel').split(", ")
debug = c.get('Debug', 'log_debug')

