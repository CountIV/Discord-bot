import configparser

c = configparser.ConfigParser()
c.read('config/config.ini')


# Discord
prefix = c.get('Discord', 'prefix').split(", ")
admin_role = c.get('Discord', 'admin_role')


# Aliases
music = {
    'join':     c.get('Aliases', 'music_join').split(", "),
    'leave':    c.get('Aliases', 'music_leave').split(", "),
    'play':     c.get('Aliases', 'music_play').split(", "),
    'clear':    c.get('Aliases', 'music_clear').split(", "),
    'skip':     c.get('Aliases', 'music_skip').split(", "),
    'queue':    c.get('Aliases', 'music_queue').split(", "),
    'remove':   c.get('Aliases', 'music_remove').split(", "),
}


#Debugging
debug_channel = c.get('Debug', 'debug_channel').split(", ")
debug = c.get('Debug', 'log_debug')

