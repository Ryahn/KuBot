import sys
# Begin Editable Configuration
# Default room for Command Printing
defaultRoom = "debotsch"        # A play channel for the bot to sit in, makes it where you have a place to test commands.

# Bot Version Information [Do not change!]
botver="version-0.05.04-alpha"  # Current version of the bot updates.
trunk="master"                  # Git Trunk / Branch
codename="KuBot"                # Name of the Bot's Branch
botdev="Kukumakranka"           # Name of the Bot Developer

# Storage Mode / Driver
mode = "flatfile"               # Mode of Storage, flatfile or sql.

# Debugging Mode on / off
debug = "on"

# We will include the configuration here
# End Editable Configuration
def hexc(e, rt = False):
        et, ev, tb      = sys.exc_info()
        #if not tb: log.error(str(e))
        while tb:
                lineno = tb.tb_lineno
                fn      = tb.tb_frame.f_code.co_filename
                tb      = tb.tb_next
      #  log.error("(%s:%i) %s" % (fn, lineno, str(e)))
        if rt: return "(%s:%i) %s" % (fn, lineno, str(e))
