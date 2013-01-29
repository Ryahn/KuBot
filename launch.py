import sys
import os
import re
import cgi
import codecs
import traceback
import time
import urllib
import datetime
import binascii
import glob
import json
import csv
import zipfile
import codecs

input = open('storage/update/bot.py', 'r')
output = open('start.py', 'w', encoding='utf-8-sig')
for line in input.readlines():
    if "# We will start importing commands.py here." in line:
        input2 = open('commands.py', 'r', encoding='utf-8-sig')
        for line2 in input2.readlines():
            if "self.getAccess(user)" in line2:
                line2.replace("self.getAccess(user)", "self.getAccess(user.name)")
            output.write(line2)
        input3 = open('bot_commands.py', 'r', encoding='utf-8-sig')
        for line3 in input3.readlines():
            output.write(line3)
    else:        
        output.write(line)
        
if os.path.exists('conf_update.txt'):
    f = open('conf_update.txt', 'r')
    file = open('config.py', 'a')
    file.write("\n")
    file.close()
    for line in f.readlines():
        file = open('config.py', 'a')
        file.write("%s\n" % line.strip())
        file.close()
    f.close()
    os.unlink('conf_update.txt')
    
if os.path.exists('lvl_config_update.txt'):
    f = open('lvl_config_update.txt', 'r')
    file = open('lvl_config.py', 'a')
    file.write("\n")
    file.close()
    for line in f.readlines():
        file = open('lvl_config.py', 'a')
        file.write("%s\n" % line.strip())
        file.close()
    f.close()
    os.unlink('lvl_config_update.txt')
    
input.close()
output.close()
input = open('storage/update/cmds.py', 'r')
output = open('bot_conf.py', 'w')
for line in input.readlines():
    if "# We will include the configuration here" in line:
        input2 = open('config.py')
        for line2 in input2.readlines():
            output.write(line2)
    else:        
        output.write(line)
input.close()
output.close()