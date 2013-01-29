# Handle Imports, check to see what mode we're using.
import ch
import random
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
import youtube
import glob
import helperCmd
import json
import imp
import bot_conf
import persona
import webbrowser
import csv
import subprocess
import lvl_config
import ranks_config
import zipfile
if bot_conf.mode.lower() == "sql":
     import sqlite3
from bot_conf import hexc as hexc1
# End of Imports
# Determine our Logging Information: (Might not be important, depends on mode.)

butterfly_timeout = datetime.datetime.now()
fishes_timeout = datetime.datetime.now()
update_timeout = datetime.datetime.now()
# Global Console Colors

# Main Bot Variables, It is extremely important that these remain unedited.
# Check if the bot is in Lockdown Mode
lockdown = False
# Setup the startTime variable for uptime information.
startTime = time.time()
# Print out the Bot's name and version to console.
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")
print("Hi I am %s" % bot_conf.botname.title())
print("I am currently running on core version: %s" % bot_conf.botver.title())
# Update our Status to "Online"
print("[INF] Attempting to set status to Online...")
if bot_conf.mode.lower() == "sql":
    try:
        conn = sqlite3.connect('storage/database/bot.db')
    except:
        print("[ERR] Database Connection Failed")
        dbstatus = "error"
    if lockdown == True:
        status = "lockdown"
        print("[INF] Status is in Lockdown mode, will start up in Lockdown Mode...")
        conn.execute("UPDATE settings SET setting_value = 'lockdown' WHERE setting_name = 'status'")
    if lockdown == False:
        status = "online"
        print("[INF] Status is in Online Mode..")
        conn.execute("UPDATE settings SET setting_value = 'online' WHERE setting_name = 'status'")
    if dbstatus == "available":
        conn.commit()
if bot_conf.mode.lower() == "flatfile":
    if lockdown == True:
        status = "lockdown"
        filename = "storage/flatfile/bot/status.txt"
        file = open(filename, 'w')
        print("[INF] Status is in Lockdown mode, will start up in Lockdown mode...")
        file.write("Lockdown")
        file.close()
    if lockdown == False:
        status = "online"
        filename = "storage/flatfile/bot/status.txt"
        file = open(filename, 'w')
        print("[INF] Status is in Online Mode..")
        file.write("Online")
        file.close()
# End Status Update
# Store temporary memory tables for various text files. Unimportant in SQL Mode (SQL Mode stays Live.)
bot_startup_time = datetime.datetime.now()
# Load the Definitions Table
if bot_conf.mode.lower() == "flatfile":
    dictionary = dict()
    f = open("storage/flatfile/various/definitions.txt", "r")
    print("[INF] Loading the Definitions Table...")
    time.sleep(1)
    for line in f.readlines():
        try:
            if len(line.strip())>0:
                word, definition, name = json.loads(line.strip())
                dictionary[word] = json.dumps([definition, name])
        except:
            print("[ERR] Definition not loaded: %s" % line)
    f.close()
# End Loading the Definition Table

# Populate the 'users' table.
ranks = ranks_config.ranks
users = []

for rank in ranks:
    count = 0
    rank = rank.split(",", 4)
    if len(rank) == 4:
        shortcode = rank[0]
        rank_lvl = rank[1]
        rank_file = rank[2]
        rank_name = rank[3].strip()
        
        file = open("storage/flatfile/ranks/%s" % (rank_file), "r")
        for name in file.readlines():
            if len(name.strip()) > 0:
                try:
                    users.append("%s,%s" % (name.strip(), rank_lvl))
                    count = count + 1
                except Exception as e:
                    print(e)
        file.close()
        print("Loading %s Table.. %s Found" % (rank_name, count))
    else:
        # Not enough values.
        print("skipping invalid rank information")
# End Populating the 'users' table.

# End Populating User Tables
# Begin Populating Room Data (Banned Rooms, Banned Words, Spammers, Joined Rooms)
# Load the Default Rooms Table
if bot_conf.mode.lower() == "flatfile":
    rooms = []
    rooms.append(bot_conf.defaultRoom)
    f = open("storage/flatfile/rooms/join_rooms.txt", "r")
    for name in f.readlines():
        if len(name.strip())>0: rooms.append(name.strip())
    print("[INF] Loading the default Rooms... %s" % len(rooms))
    f.close()
if bot_conf.mode.lower() == "sql":
    rooms = []
    rooms.append(bot_conf.defaultRoom)
    try:
        conn = sqlite3.connect('storage/database/bot.db')
    except:
        print("[ERR] Database Connection Failed")
        dbstatus = "error"
    counted = 0
    for row in conn.execute("SELECT room FROM rooms WHERE banned = '0';"):
        if bot_conf.debug.lower() == "on":
            print(row[0])
        counted = counted + 1
        if len(row[0].strip())>0: rooms.append(row[0].strip())
    if bot_conf.debug.lower() == "on":
        print(rooms)
    print("[INF] Loading the default Rooms... %s" % counted)
# End Loading the Default Rooms Table
# Load the Banned Rooms Table
if bot_conf.mode.lower() == "flatfile":
    badrooms = []
    f = open("storage/flatfile/rooms/banned_rooms.txt", "r")
    for name in f.readlines():
        if len(name.strip())>0: badrooms.append(name.strip())
    print("[INF] Loading the Banned Rooms... %s" % len(badrooms))
    f.close()
if bot_conf.mode.lower() == "sql":
    badrooms = []
    try:
        conn = sqlite3.connect('storage/database/bot.db')
    except:
        print("[ERR] Database Connection Failed")
        dbstatus = "error"
    counted = 0
    for row in conn.execute("SELECT room FROM rooms WHERE banned = '1';"):
        if bot_conf.debug.lower() == "on":
            print(row[0])
        counted = counted + 1
        if len(row[0].strip())>0: badrooms.append(row[0].strip())
    if bot_conf.debug.lower() == "on":
        print(badrooms)
    print("[INF] Loading the Banned Rooms... %s" % counted)
# End Loading the Banned Rooms Table
# Load the Banned Words Table
if bot_conf.mode.lower() == "flatfile":
    cuss = []
    f = open("storage/flatfile/rooms/banned_words.txt", "r")
    for name in f.readlines():
        if len(name.strip())>0: cuss.append(name.strip())
    print("[INF] Loading the Banned Words... %s" % len(cuss))
    f.close()
if bot_conf.mode.lower() == "sql":
    cuss = []
    try:
        conn = sqlite3.connect('storage/database/bot.db')
    except:
        print("[ERR] Database Connection Failed")
        dbstatus = "error"
    counted = 0
    for row in conn.execute("SELECT entry FROM words WHERE banned = '1';"):
        if bot_conf.debug.lower() == "on":
            print(row[0])
        counted = counted + 1
        if len(row[0].strip())>0: cuss.append(row[0].strip())
    if bot_conf.debug.lower() == "on":
        print(cuss)
    print("[INF] Loading the Banned Words... %s" % counted)
# End Loading the Banned Words Table
# Load the Spam Warning Table
if bot_conf.mode.lower() == "flatfile":
    spamwarn = []
    f = open("storage/flatfile/rooms/spam_warnings.txt", "r")
    for name in f.readlines():
        if len(name.strip())>0: spamwarn.append(name.strip())
    print("[INF] Loading the Spam Warnings... %s" % len(spamwarn))
    f.close()
if bot_conf.mode.lower() == "sql":
    spamwarn = []
    try:
        conn = sqlite3.connect('storage/database/bot.db')
    except:
        print("[ERR] Database Connection Failed")
        dbstatus = "error"
    counted = 0
    for row in conn.execute("SELECT username FROM warnings;"):
        if bot_conf.debug.lower() == "on":
            print(row[0])
        counted = counted + 1
        if len(row[0].strip())>0: spamwarn.append(row[0].strip())
    if bot_conf.debug.lower() == "on":
        print(spamwarn)
    print("[INF] Loading the Spam Warnings... %s" % counted)

# End Loading the Spam Warnings Table
# End Loading of Rooms, Banned Words & Spammer Warnings
# Miscellaneous
#music
music = []
f = open("storage/flatfile/various/music.txt", "r") # read-only
for name in f.readlines():
        if len(name.strip())>0: music.append(name.strip())
time.sleep(1)
print("[INF] Loading music... %s" % len(music))
f.close()
#tabs#
tabs = []
f = open("storage/flatfile/various/tabs.txt", "r") # read-only
for name in f.readlines():
        if len(name.strip())>0: tabs.append(name.strip())
print("[INF] Loading tabs... %s" % len(tabs))
f.close()
#GREETS#
greets = []
f = open("storage/flatfile/various/greets.txt", "r") # read-only
print("[INF] Loading Greets...")
for name in f.readlines():
        if len(name.strip())>0: greets.append(name.strip())
f.close()
#fapstuff

fapthings = []

f = open("storage/flatfile/other/fapthings.txt", "r") # read-only

for name in f.readlines():

        if len(name.strip())>0: fapthings.append(name.strip())

time.sleep(1)

print("[INF] Loading Fap things... %s" % len(fapthings))

f.close()

#END



randomfacts = []

f = open("storage/flatfile/other/randomfacts.txt", "r")

for name in f.readlines():

        if len(name.strip())>0: randomfacts.append(name.strip())

f.close()







###########################################################

## Thu 14 Apr 2011 00:05:52 BST

###########################################################

# CACHE
ipcache = []
lastcache = 0

if sys.version_info[0] > 2:

        import urllib.request as urlreq

else:

        import urllib2 as urlreq
        
        #dance moves was here

activated = True # Disabled on default

try:
    prefix = bot_conf.prefix
except:
    prefix = "'" # command prefix for some commands

greetson = True



def onPMMessage(self, pm, user, body):

        pm.message(user, body) #hehe... echo :3



def getUptime():

    """

    Returns the number of minutes since the program started.

    """

    # do return startTime if you just want the process start time

    return (time.time() - startTime) / 60.00 / 60.00

 
# System Uptime (No real clue why this is even necessary anymore.)    
def uptime():
     try:
         f = open( "/proc/uptime" )
         contents = f.read().split()
         f.close()
     except:
        return "Cannot open uptime file: /proc/uptime"
     total_seconds = float(contents[0])
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
     return string;



class b(ch.RoomManager):
    def onInit(self):
        try:
            self.setNameColor(bot_conf.name_color)
            self.setFontColor(bot_conf.font_color)
            self.setFontFace("5")
            self.setFontSize(12)
            self.enableBg()
            self.disableRecording()
        except:
            self.setNameColor("000000")
            self.setFontColor("000000")
            self.setFontFace("5")
            self.setFontSize(12)
            self.enableBg()
            self.disableRecording()
            
    def getAccess(self, un):
        try:
            person_found = 0
            person_to_find = un
            if person_to_find == bot_conf.botowner: return lvl_config.rank_lvl_botowner
            for person in users:
                person = person.split(",", 2)
                if person_to_find == person[0]:
                    return int(person[1])
                    person_found = 1
            if person_found == 0:
                return 0
        except Exception as e:
            print(e)
            
    def getRank(self, un):
        try:
            rank_found = 0
            rank_no = 0
            person_to_find = un
            if person_to_find == bot_conf.botowner: return "Bot Owners"
            for person in users:
                if person_to_find in person:
                    person = person.split(",", 2)
                    rank_no = person[1]
                    
            if rank_no != 0:
                for rank in ranks:
                    rank = rank.split(",", 4)
                    if len(rank) == 4:
                        if rank_no == rank[1]:
                            return rank[3]
            else:
                return "Guests"
        except Exception as e:
            print(e)
            
    def savRanks(self):
        try:
            for rank in ranks:
                users_tmp = []
                rank = rank.split(',', 4)
                if len(rank) == 4:
                    for person in users:
                        person = person.split(',', 2)
                        if len(person) == 2:
                            user_to_find = "%s" % person[1]
                            search_rank_lvl = "%s" % rank[1]
                            if person[1] in rank[1]:
                                users_tmp.append("%s" % person[0])
                    print("[INF] Saving %s Table" % rank[3])
                    ranks_file = open("storage/flatfile/ranks/%s" % (rank[2]), "w")
                    ranks_file.write("\n".join(users_tmp))
                    ranks_file.close()
        except Exception as e:
            print(e)

    def onConnect(self, room):
        print("Joining [%s]" % room.name)
    def onReconnect(self, room):
        print("[INF] Reconnected to [%s]" % room.name)
    def onDisconnect(self, room):
        room.message("i got to go ;(")
        print("Disconnecting from [%s]" % room.name)
    def onFloodWarning(self, room):
        room.reconnect()
        
    def set_timeout(self, persona_type):
        global butterfly_timeout
        global fishes_timeout
        
        if persona_type == "bfly":
            butterfly_timeout = datetime.datetime.now()
        elif persona_type == "fish":
            fishes_timeout = datetime.datetime.now()
        elif persona_type == "update":
            update_timeout = datetime.datetime.now()
        
    def checkUpdate(self):
        from urllib.request import urlopen
        urlStr = 'http://kubot.dubbedepisodes.com:8081/version.txt'
        update_url = "http://kubot.dubbedepisodes.com:8081/"
        try:
          fileHandle = urlopen(urlStr)
          str1 = fileHandle.read().decode("utf-8")
          fileHandle.close()
          str1 = str1.replace("b'", "")
          str1 = str1.replace("'", "")
        except IOError:
          print ('Cannot open URL %s for reading' % urlStr)
          str1 = 'error!'
          
        in_line = 0
        latest_version = str1
        if latest_version == bot_conf.botver.lower():
            in_line = 1
        if in_line == 0:
            print("This version will be updated.")
            if latest_version != "error!":
                try:
                    # Time to break it into versioning information.
                    latest_version = latest_version.replace("version-", "")
                    latest_version = latest_version.replace("-alpha", "")
                    latest_version = latest_version.replace(".", "")
                    current_version = bot_conf.botver.replace("version-", "")
                    current_version = current_version.replace("-alpha", "")
                    current_version = current_version.replace(".", "")
                    print('latest_ver = %s, current_ver = %s' % (latest_version, current_version))
                    no_of_updates = int(latest_version) - int(current_version)
                    print(no_of_updates)
                    count = 1
                    error = 0
                    while ( count <= no_of_updates and error != 1 ):
                        grab_ver = int(current_version) + count
                        grab_ver = str(grab_ver).zfill(5)
                        print(grab_ver)
                        rev = "%s" % grab_ver[-2:]
                        newstr = "%s" % grab_ver[:-2]
                        min_v = "%s" % newstr[-2:]
                        newstr1 = "%s" % newstr[:-2]
                        major = "%s" % newstr1
                        print(major)
                        print(min_v)
                        print(rev)
                        version = "version-%s.%s.%s-alpha.zip" % (major, min_v, rev)
                        zip_url = "http://kubot.dubbedepisodes.com:8081/%s" % (version)
                        zip_dir = "./"
                        
                        try:
                            from urllib.request import urlopen
                            file_name = os.path.basename("%s" % zip_url)
                            fullpath = os.path.join(zip_dir, '%s' % file_name)
                            print(fullpath)
                            try:
                                print("Attempting to download file..")
                                fullpath, hdrs = urllib.request.urlretrieve(zip_url, fullpath)
                            except IOError as e:
                                print ("Can't retrieve %s to %s: %s" % (zip_url, zip_dir, e))
                                return False
                            try:
                                z = zipfile.ZipFile(fullpath)
                                z.extractall(zip_dir)
                            except zipfile.error as e:
                                print ("Bad zipfile (from %s): %s" % (zip_url, e))
                                return False
                            z.close()
                            os.unlink(fullpath)
                            print("Updated to %s" % version[:-4])
                            time.sleep(1)
                        except Exception as e:
                            print(e)
                            print("Couldn't update to %s" % version[:-4])
                            error = 1
                        count = count + 1
                    if error == 1:
                        return "Error"
                    else:
                        return "Updated"
                except Exception as e:
                    return "Error"
                

        
    # Logging Chat Room Messages
    def chatLog(self, rn, un, acl, mip, mb, tm, rk):
        # Let's log the chat!
        if bot_conf.mode.lower() == "flatfile":
        
            # Validate that the Directory Exists
            directory = "storage/flatfile/logs/chat/%s" % rn
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            # Validate that the LogFile Exists (And is a file.)
            if os.path.exists("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today()))) == False:
                log_file = open("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today())), "w")
                log_file.write("")
                log_file.close()
            elif os.path.isfile("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today()))) == False and os.path.exists("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today()))) == True:
                os.unlink("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today())))
                log_file = open("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today())), "w")
                log_file.write("")
                log_file.close()
                
            # Validate that the Error LogFile Exists (And is a file.)
            if os.path.exists("storage/flatfile/logs/error.log") == False:
                log_file = open("storage/flatfile/logs/error.log", "w")
                log_file.write("")
                log_file.close()
            elif os.path.isfile("storage/flatfile/logs/error.log") == False and os.path.exists("storage/flatfile/logs/error.log") == True:
                os.unlink("storage/flatfile/logs/error.log")
                log_file = open("storage/flatfile/logs/error.log", "w")
                log_file.write("")
                log_file.close()
                
            # Write to the log file.
            log_file = open("storage/flatfile/logs/chat/%s/%s-chat.log" % (rn, str(datetime.date.today())), "a", errors="ignore", encoding="utf8")
            try:
                if mip == "" or mip == " ":
                    mip == "0.0.0.0"
                    
                log_file.write("[%s] [%s] [%s] [%s] [%s] %s: %s \n" % (tm, rn, rk, acl, mip, un, mb))
            except Exception as e:
                # Uh Oh, Error. Write to the Error Log
                print("[Error:] Unable to write to chatlog, error information pushed to error.log")
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error: ] %s \n" % (tm, e))
                error_log_file.close()
            log_file.close()

    # Logging Commands sent to the Bot (PM and Regular)
    def cmdlog(self, rn, un, acl, mip, mb, tm, rk, racl, cd, ag):
        # Command Logging
        if bot_conf.mode.lower() == "flatfile":
        
            # Validate that the Directory Exists
            directory = "storage/flatfile/logs/chat/%s" % rn
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = "storage/flatfile/logs/chat/%s/cmd-log" % rn
            if not os.path.exists(directory):
                os.makedirs(directory)
            directory = "storage/flatfile/logs/chat/%s/cmd-log/%s" % (rn, un)
            if not os.path.exists(directory):
                os.makedirs(directory)
                
            # Validate that the LogFile Exists (And is a file.)
            if os.path.exists("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today()))) == False:
                log_file = open("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today())), "w")
                log_file.write("")
                log_file.close()
            elif os.path.isfile("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today()))) == False and os.path.exists("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn, str(datetime.date.today()))) == True:
                os.unlink("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today())))
                log_file = open("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today())), "w")
                log_file.write("")
                log_file.close()
                
            # Validate that the Error LogFile Exists (And is a file.)
            if os.path.exists("storage/flatfile/logs/error.log") == False:
                log_file = open("storage/flatfile/logs/error.log", "w")
                log_file.write("")
                log_file.close()
            elif os.path.isfile("storage/flatfile/logs/error.log") == False and os.path.exists("storage/flatfile/logs/error.log") == True:
                os.unlink("storage/flatfile/logs/error.log")
                log_file = open("storage/flatfile/logs/error.log", "w")
                log_file.write("")
                log_file.close()
                
            logfile = open("storage/flatfile/logs/chat/%s/cmd-log/%s/%s-commands.log" % (rn,un,str(datetime.date.today())), "a", errors="ignore", encoding="utf8")

            if racl >= acl:
                cmd_status = "Successful"
            else:
                cmd_status = "Failed"
                
            if mip == "" or mip == " ":
                mip = "0.0.0.0"
                
            try:
                logfile.write("<entry>\n")
                logfile.write("     <date>%s</date>\n" % tm)
                logfile.write("     <ip>%s</ip>\n" % mip)
                logfile.write("     <username>%s</username>\n" % un)
                logfile.write("     <room>%s</room>\n" % rn)
                logfile.write("     <user_lvl>%s</user_lvl>\n" % acl)
                logfile.write("     <user_rank>%s</user_rank>\n" % rk)
                logfile.write("     <command>%s</command>\n" % cd)
                logfile.write("     <args>%s</args>\n" % ag)
                logfile.write("     <req_rank>%s</req_rank>\n" % racl)
                logfile.write("     <status>%s</status>\n" % cmd_status)
                logfile.write("</entry>\n")
            except Exception as e:
                # Uh Oh, Error. Write to the Error Log
                print("[Error:] Unable to write to command log, error information pushed to error.log")
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error: ] %s \n" % (tm, e))
                error_log_file.close()
            logfile.close()
            
    def getAlias(self, un):
        if bot_conf.mode.lower() == "flatfile":
            # Validate that the LogFile Exists (And is a file.)
            if os.path.exists("storage/flatfile/various/aliases.csv") == False:
                log_file = open("storage/flatfile/various/aliases.csv", "w")
                log_file.write("")
                log_file.close()
            elif os.path.isfile("storage/flatfile/various/aliases.csv") == False and os.path.exists("storage/flatfile/various/aliases.csv") == True:
                os.unlink("storage/flatfile/various/aliases.csv")
                log_file = open("storage/flatfile/various/aliases.csv", "w")
                log_file.write("")
                log_file.close()
                
            nickname = un
            try:
                alias_file = open("storage/flatfile/various/aliases.csv", "r")
                alias_flag = 0
                for line in alias_file.readlines():
                
                    alias_data = line.strip()
                    alias_username, alias_nickname = alias_data.split(",", 1)
                    # Fill Temporary Variables with the Split Line
                    
                    if un in alias_username:
                        nickname = alias_nickname
                        
                alias_file.close()
                return nickname
            except Exception as e:
                return nickname
    def onPMMessage(self,pm,user,body):
        try:
            print("[%s] [PM] [Level: %s] %s: %s" % (time.strftime("%d/%m/%y- %H:%M:%S", time.localtime(time.time())), self.getAccess(user.name.lower()), user.name.title(), body))
        except:
            print("")
        # Blacklist messages coming from the bot.
        if self.user == user: return
        
        # Blacklist messages coming from members in the Blacklist
        if self.getAccess(user.name.lower()) == -1: return
        
        # Blacklist any user less than the LockDown bypass rank.
        if self.getAccess(user.name.lower()) < 3 and lockdown == True: return
        
        # Split the message body and prepare command.
        pm_data = body.lower().split(" ", 1)
        if len(pm_data) > 1:
                pm_cmd, pm_args = pm_data[0], pm_data[1] # if command and args
        else:
                pm_cmd, pm_args = pm_data[0], ""# if command and no args
        
        # Is the command implied
        if len(pm_cmd) > 0:
                if pm_cmd[0].lower() == prefix.lower():
                        pm_prefix_used = True
                        pm_cmd = pm_cmd[1:].lower()
                else: pm_prefix_used = False
        else: return
        
        # Import Commands from pm_bot_commands.py
        
        # Import Commands from pm_commands.py
        
    def onJoin(self, room, user):
        if lockdown: return
        elif user.name in greets:
            resp = ["Yo %s " % user.name.title(), "Hey %s" % user.name.title(), "Hi %s :3" % user.name.title(),]
            room.message(random.choice(resp))
            
    def api(self, type, un, mip):
        from urllib.request import urlopen
        if type == "whois":
            try:
                apiUrl = "http://kubot.dubbedepisodes.com:8081/api.php?type=whois&un=%s&mip=%s" % (un,mip)   
                html = urlopen(apiUrl).read()
                return True
            except Exception as e:
                print(e)
        if type == "whois_check":
            try:
                apiUrl = "http://kubot.dubbedepisodes.com:8081/api.php?type=whois&un=%s&parse=yes" % (un)
                html = urlopen(apiUrl).read().decode()
                
                whois = html.split(",")
                for uname in whois:
                    if uname == '':
                        whois.remove(uname)
                return whois
            except Exception as e:
                print(e)

    def onMessage(self, room, user, message):
        try:
            font_color = bot_conf.font_color
            name_color = bot_conf.name_color
            font_face = bot_conf.font_face
            font_size = bot_conf.font_size
        except:
            font_color = "000000"
            name_color = "000000"
            font_face = "Arial"
            font_size = "12"
        update_diff = datetime.datetime.now() - update_timeout
        try:
             update_interval = int(bot_conf.update_interval) * 60
             update_check = bot_conf.update_check.lower()
        except:
             update_interval = 1800
             update_check = "yes"
             
        if update_diff.seconds > update_interval and update_check == "yes":
            self.set_timeout("update")
            if self.checkUpdate() == "Updated":
                if os.name == "nt":
                    # Re-Launch Launch.bat
                    self.setTimeout(3, subprocess.Popen(['launch.bat', '']))
                    self.setTimeout(3, self.stop)
                else:
                    # Re-Launch Launch.sh
                    self.setTimeout(3, subprocess.Popen(['/bin/bash', 'launch.sh']))
                    self.setTimeout(3, self.stop)
        # make global (if they will be changed in commands)
        global activated
        global lockdown
        global greetson
        global lastcache
        body = message.body #body ----
        body = re.sub(' +',' ', body) # regex start
        lbody = message.body.lower()
        chat_message = room.message
        ## print to console
        cur_msg_time = time.strftime("%d/%m/%y - %H:%M:%S", time.localtime(time.time()))
        try:
            # Print the message out to console.
            print("[%s] [MSG] [LVL %s] [%s] %s: %s" % (cur_msg_time, self.getAccess(user.name.lower()), room.name, user.name.title(), message.body))
        except Exception as e:
            # Uh Oh, Error. Write to the Error Log
            print("[Error:] Unable to write to console, encoding error perhaps? Wrote to error log file.")
            error_log_file = open("storage/flatfile/logs/error.log", "a")
            error_log_file.write("[%s] [Error: ] %s" % (cur_msg_time, e))
            error_log_file.close()
                    
        # Write to log.
        self.chatLog(room.name, user.name, self.getAccess(user.name.lower()), message.ip, message.body.lower(), cur_msg_time, self.getRank(user.name))
                
        # API Call to Whois
        if message.ip != "" or message.ip != " ":
            self.api("whois", user.name, message.ip)
            
        # Prevent certain users and groups from accessing the bot.
        
        # If the user is the bot's username, ignore.
        if self.user == user: return
        
        # If the command is coming from a room in the banned room list, ignore.
        if room.name in badrooms: return
        
        # If the user's access is -1 (blacklisted), ignore.
        if self.getAccess(user.name.lower()) == -1: return
        
        # If the bot is in lockdown mode, and the user's rank is less than lvl_config.lockdown_mode_bypass, ignore.
        if self.getAccess(user.name.lower()) < lvl_config.lockdown_mode_bypass and lockdown == True: return
        
        # Split the data and prepare the command.
        data = lbody.split(" ", 1)
        if len(data) > 1:
                cmd, args = data[0], data[1]
        else:
                cmd, args = data[0], ""
                
        # If the prefix is used in "cmd" then set used_prefix to true, else false.
        if len(cmd) > 0:
                if cmd[0].lower() == prefix.lower():
                        used_prefix = True
                        cmd = cmd[1:].lower()
                else: used_prefix = False
        else: return
        
        # If you have enough access, calling the bot's name will activate it (if it is deactivated.)
        if cmd.lower() == room.user.name.lower() and len(args) == 0:# blacklistS CASE NOW
                if not activated and self.getAccess(user.name.lower()) < 2: return
                responce = ["yeah? %s" % self.getAlias(user.name), "hmmhm %s" % self.getAlias(user.name), "o-o %s yesh?" % self.getAlias(user.name), "hi %s ^^" % self.getAlias(user.name),]
                chat_message("<font color='#%s' face='%s' size='%s'>%s</font>" % (font_color, font_face, font_size, random.choice(responce)), True)
                activated = True
                
        # call bot name with command after
        elif cmd.upper() == room.user.name.upper() and len(args) != 0:# blacklistS CASE NOW
                activated = True
                used_prefix = True
                data = args.split(" ", 1)
                if len(data) > 1:
                        cmd, args = data[0], data[1] # if command and args
                else:
                        cmd, args  = data[0], "" # if command and no args
        # not activated, no commands
        if not activated: return
        # sleep/deactive bot (hide)
        if used_prefix and cmd == "sleep" and self.getAccess(user.name.lower()) > 2: # level 2+
                activated = False
                room.message(cgi.escape("Ok night zzzz "))
        #eval
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_cmd_eval and cmd == "eval":
            try:
                    ret = eval(args)
                    chat_message(str(repr(ret)+" ^-^"))
            except Exception as e:
                    chat_message("<b>Error[String problem]:</b> "+str(hexc1(e, True))+" x.x", True)
        # Command Usage: 'promote <username>, 'promote <username> <rank>
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_min_promote and cmd == "promote" and len(args) > 3:
            whole_body = message.body.split(" ", 3)
            promote_username = whole_body[1].lower()
            promote_username = promote_username.strip()
            cur_rank = self.getRank(promote_username)
            try:
                next_rank = 0
                if "-" in whole_body[2]:
                    next_rank = 0 - int(whole_body[2])
                else:
                    next_rank = int(whole_body[2])
                    
                user_level = self.getAccess(promote_username)
                if user_level == lvl_config.rank_lvl_botowner:
                    next_rank = user_level
                elif user_level != -1:
                    next_rank = next_rank
                else:
                    if self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_rem:
                        next_rank = next_rank
                    else:
                        next_rank = user_level
            except:
                user_level = 0
                next_rank = 0
                
                user_level = self.getAccess(promote_username)
                if user_level == lvl_config.rank_lvl_botowner:
                    next_rank = user_level
                elif user_level != -1:
                    next_rank = user_level + 1
                else:
                    if self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_rem:
                        next_rank = user_level + 1
                    else:
                        next_rank = user_level
                    
            if next_rank > len(ranks) - 1 and self.getAccess(user.name.lower()) >= lvl_config.rank_lvl_botowner and next_rank > self.getAccess(promote_username):
                chat_message("<font color='#%s' face='%s' size='%s'>Sorry <b>%s</b>, I couldn't promote <b>%s</b> as they are already one of my <b>%s (%s)</b>.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), self.getAlias(promote_username), self.getRank(promote_username), self.getAccess(promote_username)), True)
            elif next_rank <= len(ranks) - 1 and next_rank >= 0 and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_promote and next_rank > self.getAccess(promote_username):
                print("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                try:
                    users.remove("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                except Exception as e:
                    print(e)
                if next_rank != 0:
                    users.append("%s,%s" % (str(promote_username).strip(), str(next_rank).strip()))
                try:
                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has been promoted from <b>%s (%s)</b> and is now <b>%s (%s)</b>.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), cur_rank, user_level, self.getRank(promote_username), self.getAccess(promote_username)), True)
                except Exception as e:
                    print(e)
            elif next_rank == -1 and self.getAccess(user.name.lower()) < lvl_config.rank_req_blacklist_rem and next_rank >= self.getAccess(promote_username):
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> is on the blacklist and cannot be removed by you. Contact a person with level %s or higher access.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), lvl_config.rank_req_blacklist_rem), True)
            elif next_rank == self.getAccess(promote_username):
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> is already a rank of %s (%s).</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), self.getRank(promote_username), self.getAccess(promote_username)), True)
            # Save all the data now.
            self.savRanks()
        # End Command
        
        # Command Usage: 'demote <username>, 'demote <username> <rank>
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_min_demote and cmd == "demote" and len(args) > 3:
            whole_body = message.body.split(" ", 3)
            promote_username = whole_body[1].lower()
            promote_username = promote_username.strip()
            cur_rank = self.getRank(promote_username)
            try:
                next_rank = 0
                if "-" in whole_body[2]:
                    next_rank = 0 - int(whole_body[2])
                else:
                    next_rank = int(whole_body[2])
                    
                user_level = self.getAccess(promote_username)
                if user_level == lvl_config.rank_lvl_botowner:
                    next_rank = user_level
                elif user_level != -1:
                    next_rank = next_rank
                elif self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_add and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote and next_rank == -1:
                    next_rank = next_rank
            except:
                user_level = 0
                next_rank = 0
                
                user_level = self.getAccess(promote_username)
                next_rank = user_level - 1
                if user_level == lvl_config.rank_lvl_botowner:
                    next_rank = user_level
                elif user_level != -1:
                    next_rank = next_rank
                elif self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_add and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote and next_rank == -1:
                    next_rank = next_rank
                    
            if next_rank > len(ranks) - 1 and self.getAccess(user.name.lower()) >= lvl_config.rank_lvl_botowner and next_rank > self.getAccess(promote_username):
                chat_message("<font color='#%s' face='%s' size='%s'>Sorry <b>%s</b>, I couldn't do that to <b>%s</b> as they are one of my <b>%s (%s)</b>.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), self.getAlias(promote_username), self.getRank(promote_username), self.getAccess(promote_username)), True)
            elif next_rank <= len(ranks) - 1 and next_rank >= 0 and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote and next_rank < self.getAccess(promote_username):
                print("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                try:
                    users.remove("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                except Exception as e:
                    print(e)
                if next_rank != 0:
                    users.append("%s,%s" % (str(promote_username).strip(), str(next_rank).strip()))
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has been demoted from <b>%s (%s)</b> and is now <b>%s (%s)</b>.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), cur_rank, user_level, self.getRank(promote_username), self.getAccess(promote_username)), True)
            elif next_rank == -1 and self.getAccess(user.name.lower()) < lvl_config.rank_req_blacklist_add and next_rank <= self.getAccess(promote_username) and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> is not on the blacklist and cannot be added by you. Contact a person with level %s or higher access.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), lvl_config.rank_req_blacklist_rem), True)
            elif next_rank == self.getAccess(promote_username):
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> is already a rank of %s (%s).</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), self.getRank(promote_username), self.getAccess(promote_username)), True)
            elif next_rank == -1 and self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_add and next_rank < self.getAccess(promote_username) and self.getAccess(user.name.lower()) < self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> is a higher rank than you. You are unable to blacklist them.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username)), True)
            elif next_rank == -1 and self.getAccess(user.name.lower()) >= lvl_config.rank_req_blacklist_add and next_rank < self.getAccess(promote_username) and self.getAccess(user.name.lower()) >= self.getAccess(promote_username) + lvl_config.rank_req_modifier_demote:
                print("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                try:
                    users.remove("%s,%s" % (str(promote_username).strip(), str(user_level).strip()))
                except Exception as e:
                    print(e)
                users.append("%s,%s" % (str(promote_username).strip(), str(next_rank).strip()))
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has been demoted from <b>%s (%s)</b> and is now <b>%s (%s)</b>.</font>" % (font_color, font_face, font_size, self.getAlias(promote_username), cur_rank, user_level, self.getRank(promote_username), self.getAccess(promote_username)), True)
            # Save all the data now.
            self.savRanks()
        # Command End
        # Advanced "Moderator" Commands
        # Command Usage: 'delete <username> or 'del <username>
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_del and (cmd == "delete" or cmd == "del") and len(args) > 0:
            reqrank = 4
            # Logging should always come right after reqrank.
            # Fill "name" with the "username" to be deleted.
            name = args
            # Now the command test to make sure the user has enough access.
            if self.getAccess(user.name.lower()) >= reqrank:
                room.clearUser(ch.User(name))
            else:
                chat_message("Error: You do not have the required permission. You have been reported to my master. :@+15")
                self.pm.message(ch.User(bot_conf.botowner.lower()), "The user %s attempted to use the command: %s. This user does not have permission. I have added them in the warnings list." % (user.name, cmd))
        # End Command: Delete
        # Command Usage: 'ban <username>
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_ban and cmd == "ban" and len(args) > 0:
            reqrank = lvl_config.rank_req_ban
            # Logging should always come right after reqrank.
            # Fill "name" with the "username" to be deleted & banned.
            name = args
            name = name.lower()
            # Now the command test to make sure the user has enough access.
            if self.getAccess(user.name.lower()) >= reqrank:
                if name == user.name:
                    chat_message("Silly %s, you can't ban yourself." % user.name)
                elif name in owners or name in bot_conf.botowner.lower():
                    chat_message("I would never ban one of my Owners. I'm reporting you! :@+15")
                    self.pm.message(ch.User(bot_conf.botowner.lower()), "The user %s was attempting to ban one of my owners. The user's rank is %s." % (user.name, self.getAccess(user.name.lower())))
                elif name in smasters:
                    chat_message("Nuh-uh, they gave me yummy food. :D+15")
                elif name in master:
                    chat_message("Nupe! Dis person, they be mah friend.")
                elif name in moderator:
                    if user.name in owners:
                        room.clearUser(ch.User(name))
                        room.banUser(ch.User(name))
                    chat_message("You can't ban other moderators. I've requested my owner to review.")
                    self.pm.message(ch.User(bot_conf.botowner.lower()), "The user %s was attempting to ban one of the moderators, %s. The user's rank is %s." % (user.name, name, self.getAccess(user.name.lower())))
                else:
                    room.clearUser(ch.User(name))
                    room.banUser(ch.User(name))
            else:
                chat_message("Error: You do not have the required permission. You have been reported to my master. :@+15")
                self.pm.message(ch.User(bot_conf.botowner.lower()), "The user %s attempted to use the command: %s. This user does not have permission. I have added them in the warnings list." % (user.name, cmd))
        # Command End

        # Command Usage: 'call me <alias>'
        my_alias = message.body.split(" ", 3)
        if self.getAccess(user.name.lower()) >= lvl_config.rank_req_callme and my_alias[0] == "call" and my_alias[1] == "me":
            whole_body = message.body
            whole_body = whole_body.replace("call me ", "");
            whole_body = whole_body.replace(",", "");
            chat_message("<font color='#%s' face='%s' size='%s'>%s <b>%s</b></font>" % (font_color, font_face, font_size, random.choice(["Recorded! ^_^ I will now call you", "Registah'd, you are now", "Yo, dis mah big homie, I call dem", "Ye-a-a-ah, I guess I can call you that...", "If I have to.. I suppose I'll call you..", "I decided I will call you"]), whole_body), True)
            alias_flag = 0
            finished_proc = 1
            file = open("storage/flatfile/various/aliases.csv", "r")
            for line in file.readlines():
                alias_data = line.strip()
                alias_username, alias_nickname = alias_data.split(",", 1)
                # Fill Temporary Variables with the Split Line
                if user.name in alias_username:
                    print("%s is in the alias file." % user.name)
                    alias_flag = 1
                else:
                    file2 = open("storage/flatfile/various/aliases.tmp", "a")
                    file2.write("%s,%s \n" % (alias_username, alias_nickname))
                    file2.close()
            file.close()
            if alias_flag == 0:
                file = open("storage/flatfile/various/aliases.csv", "a")
                file.write("%s,%s \n" % (user.name, whole_body))
                file.close()
                finished_proc = 1
            if alias_flag == 1:
                os.remove("storage/flatfile/various/aliases.csv")
                file = open("storage/flatfile/various/aliases.tmp", "r")
                for line in file.readlines():
                    alias_data = line.strip()
                    alias_username, alias_nickname = alias_data.split(",", 1)
                    # Fill the Original File
                    file2 = open("storage/flatfile/various/aliases.csv", "a")
                    file2.write("%s,%s \n" % (alias_username, alias_nickname))
                    file2.close()
                    # Tell our system we can delete the temp file.
                    finished_proc = 1
                file.close()
                # Append with new username.
                file = open("storage/flatfile/various/aliases.csv", "a")
                file.write("%s,%s \n" % (user.name, whole_body))
                file.close()
            if finished_proc == 1:
                try:
                    os.remove("storage/flatfile/various/aliases.tmp")
                except:
                    print("[EXCEPT] Sometimes aliases.tmp won't be available. Not necessarily an error.")
        # End Command

        # Command Usage: 'lvl, 'whoami, 'rank, 'level
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_whoami and (cmd == "lvl" or cmd == "whoami" or cmd == "rank" or cmd == "level"):
            user_level = self.getAccess(user.name.lower())
            chat_message("<font color='#%s' face='%s' size='%s'>You are <b>%s</b> and are considered to be one of my <b>%s (%s)</b>. I like to call you <b>%s</b> though.</font> :D" % (font_color, font_face, font_size, user.name, self.getRank(user.name), user_level, self.getAlias(user.name)), True)
        # Command End

        # Command Usage: 'leave, 'leave here, 'leave <room name>
        elif (used_prefix and cmd == "leave") and self.getAccess(user.name.lower()) >= lvl_config.rank_req_roomleave:
            try:
                room_name = args
                try:
                    room_name = room_name.replace(".chatango.com", "")
                except:
                    print("room_name does not contain .chatango.com")
                    
                try:
                    room_name = room_name.replace("http://", "")
                except:
                    print("room_name does not contain http://")
                    
                if room_name == "here" and room_name != bot_conf.defaultRoom.lower():
                    chat_message("<font color='#%s' face='%s' size='%s'>Okay, see you later <b>%s</b>..</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                    self.setTimeout(2, self.leaveRoom, room.name)
                elif room_name == room_name and room_name != bot_conf.defaultRoom.lower():
                    self.getRoom(room_name).message("<font color='#%s' face='%s' size='%s'><b>%s</b> told me I had to leave so.. bye ..</font> ;(" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                    self.setTimeout(2, self.leaveRoom, room_name)
            except:
                room_name = room.name
                chat_message("<font color='#%s' face='%s' size='%s'>Okay, see you later <b>%s</b>..</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                self.setTimeout(2, self.leaveRoom, room.name)
        # End Command
        
        # Command Usage: remove me | Used by member to erase themselves from the bot's memberlists.
        if message.body == "remove me":
            if user.name in users:
                users.remove(user.name)
                self.savRanks()
                chat_message("<font color='#%s' face='%s' size='%s'>Okay, %s, I have removed you.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
            else:
                chat_message("<font color='#%s' face='%s' size='%s'>I couldn't find you anywhere in the database.</font>" % (font_color, font_face, font_size), True)
        # End Command
        
        # Command Usage: 'reset
        if used_prefix and cmd == "reset":
            if user.name == bot_conf.botowner.lower():
                for user in users:
                    users.remove(user)
                self.savRanks()
                chat_message("<font color='#%s' face='%s' size='%s'>I have cleared the lists and re-established <b>%s</b> as the only owner.</font>" % (font_color, font_face, font_size, self.getAlias(bot_conf.botowner)), True)
        # Command End
        
        # Command Usage: 'version, 'v, 'ver
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_cmd_ver and (cmd == "version" or cmd == "v" or cmd == "ver"):
                chat_message("<font color='#%s' face='%s' size='%s'><br><br>======================<br><b>Bot Versioning</b><br>======================<br> Bot Name: <b>%s</b><br> Core: <i>%s</i><br><br>======================<br><b>Master Information</b><br>======================<br> Original Dev: <b>Sorch</b><br> Botteh Core: <i>v1.2</i><br><br>======================<br><b>Branch Information</b><br>======================<br> Maintainer: <b>%s</b><br><br>======================<br><b>Bot Operator</b><br>======================<br> Bot Owner: <b>%s</b></font>" % (font_color, font_face, font_size, bot_conf.codename, bot_conf.botver, bot_conf.botdev, bot_conf.botowner), True)
        # Command End

        # Command Usage: 'restart | Restarts the bot, shutting down and then runs launch.bat or launch.sh again.
        elif used_prefix and cmd == "restart" and self.getAccess(user.name.lower()) >= lvl_config.rank_req_cmd_restart:
            if os.name == "nt":
                # Re-Launch Launch.bat
                self.setTimeout(3, subprocess.Popen(['launch.bat', '']))
                self.setTimeout(3, self.stop)
            else:
                # Re-Launch Launch.sh
                self.setTimeout(3, subprocess.Popen(['/bin/bash', 'launch.sh']))
                self.setTimeout(3, self.stop)
        # Command End
                
        # Commands that require Access Levels

        # Command Usage: 'pm or 'msg
        elif used_prefix and self.getAccess(user.name.lower()) >= lvl_config.rank_req_cmd_pm and (cmd == "pm" or cmd == "msg") and len(args) > 0:
             if self.getAccess(user.name.lower()) >=1:
                  target,content = args.lower().split(" ", 1)
                  self.pm.message(ch.User(target), content)
                  room.message("Your message has been sent successfully to %s!" % target.title())
        # Command End


        #shutdown#

        elif used_prefix and cmd == ("shutdown" or cmd == "sd") and self.getAccess(user.name.lower()) >= lvl_config.rank_req_cmd_shutdown:

                if user.name.lower() == bot_conf.botowner: room.message("but.. but.. %s doesn't want to go!! :( ;( " % bot_conf.botname, True)

                self.setTimeout(1, self.stop)

        #banroom#

        elif used_prefix and cmd == "banroom" or used_prefix and cmd =="badroom":

                if len(args) >= 3:

                        do, name = args.lower().split(" ", 1)

                        if self.getAccess(ch.User(name)) > 3 or self.getAccess(user.name.lower()) <= 3:

                                room.message("no. =/")

                                return

                        if do == "add":

                                if name in badrooms: room.message("%s is already a banned room. ^^" % room.name, True)

                                else:

                                        badrooms.append(name)

                                        print("[SAV] Saving banrooms..")

                                        f = open("storage/flatfile/rooms/banned_'storage/flatfile/rooms/join_rooms.txt", "w")

                                        f.write("\n".join(badrooms))

                                        f.close()

                                        lself.getRoom("debotsch").message("%s added %s to the banroom list in %s" % (self.getAlias(user.name), name, room.name))

                                        room.message("<b>%s</b> it has been done. ^^ remember do not ban rooms without permission ^^" % self.getAlias(user.name), True)

                        elif do == "remove":

                                if name not in badrooms: room.message("%s is not a banned room. ^^" % name, True)

                                else:

                                        badrooms.remove(name)

                                        print("[SAV] Saving banroom..")

                                        f = open("storage/flatfile/rooms/banned_'storage/flatfile/rooms/join_rooms.txt", "w")

                                        f.write("\n".join(badrooms))

                                        f.close()

                                        self.getRoom("debotsch").message("%s removed %s from the banroom list in %s" % (self.getAlias(user.name), name, room.name))

                                        room.message("it has been done i can now join the room", True)

                        else:

                                room.message("what? >.>", True)


        # Command Usage: 'greets add username, 'greets remove username, 'greets rm username
        elif used_prefix and cmd == "greets" or used_prefix and cmd == "gr":
                if len(args) >= 0:
                        do, name = args.lower().split(" ", 1)
                        if self.getAccess(user.name.lower()) > 2:
                                if do == "add":
                                        if name in greets: room.message("I already greet %s. ^^" % self.getAlias(name), True)
                                        else:
                                                greets.append(name)
                                                print("[SAV] Saving Greets..")
                                                f = open("storage/flatfile/various/greets.txt", "w")
                                                f.write("\n".join(greets))
                                                f.close()
                                                self.getRoom("debotsch").message("Greeting for %s added by %s in %s" % (self.getAlias(name), self.getAlias(user.name), room.name))
                                                room.message("Ok <b>%s</b> I will now greet %s ^^" % (self.getAlias(user.name), self.getAlias(name)), True)
                                elif do == "remove" or "rm" :
                                        if name not in greets: room.message("I do not currently greet %s ^^" % self.getAlias(name), True)
                                        else:
                                                greets.remove(name)
                                                print("[SAV] Saving Greets..")
                                                f = open("storage/flatfile/various/greets.txt", "w")
                                                f.write("\n".join(greets))
                                                f.close()
                                                self.getRoom("debotsch").message("Greeting for %s Removed by %s in %s" % (self.getAlias(name), self.getAlias(user.name), room.name))
                                                room.message("ok %s I will no longer greet %s sowwy =/" % (self.getAlias(user.name), self.getAlias(name)))
                                else:
                                        room.message("what? >.>", True)
                        else:
                                if len(greets) == 0: room.message("I have no masters. ^^", True)
                                else: room.message("I greet: <b>%s</b> want greeting to ask <b>My Owner</b> ^^" %  ", ".join(greets), True)
        # Command End
        
        # Command Usage: 'memcount
        elif used_prefix and cmd == "memcount":
                chat_message("i see: " + str(room.usercount))
        # Command End

        # Command Usage: 'demod username
        elif used_prefix and cmd == "demod" and len(args) > 0 and self.getAccess(user.name.lower()) > 4:
            name = args
            if name == "me":
                    room.removeMod(ch.User(user.name))
                    name = user.name
                    room.message ("<b>%s</b> has been removed to the mod list" % self.getAlias(name), True)
            else:
                    room.removeMod(ch.User(name))
                    room.message ("<b>%s</b> has been removed to the mod list" % self.getAlias(name), True)
        # Command End

        # Command Usage: 'mod username
        elif used_prefix and cmd == "mod" and len(args) > 0 and self.getAccess(user.name.lower()) > 4:
            name = args
            if name == "me":
                    room.addMod(ch.User(user.name))
                    name = user.name
                    room.message ("<b>%s</b> has been added to the mod list" % self.getAlias(name), True)
            else:
                    room.addMod(ch.User(name))
                    room.message ("<b>%s</b> has been added to the mod list" % self.getAlias(name), True)
        # Command End

        # Command Usage: 'flag username
        elif used_prefix and cmd == "flag" and self.getAccess(user.name.lower()) > 3:
            name = args.split()[0].lower()
            if name == bot_conf.botowner.lower():
                    room.message("no way in hell :P")
            else:
                    room.flagUser(ch.User(name))
                    self.getRoom("debotsch").message("%s flagged %s in %s" % (self.getAlias(user.name), self.getAlias(name),  room.name))
                    room.message ("<b>%s</b> has been flagged, do not abuse this system" % self.getAlias(name), True)
        # Command End

        # Command Usage: 'clear (Clears the chatroom.)
        elif used_prefix and cmd == "clear" and self.getAccess(user.name.lower()) > 3:
            room.clearall()
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
            room.clearUser(ch.User(random.choice(room.usernames)))
        # Command End
        
        # Command Usage: 'send roomname message
        elif used_prefix and (cmd == "send"):
                if len(args) == 0: room.message("Hm I need a room to send to")
                if len(args) > 3:
                        r, msg = args.lower().split(" ", 1)
                        rm = self.getRoom(r)
                        if not rm: room.message("im not there o-o")
                        if rm:
                                rm.message("%s  (:" %(msg))
                                room.message("Sent! (:")
        # Command End

        # Command Usage: 'give me/username something
        elif used_prefix and (cmd == "give")  and len(args) > 1:
                try:
                        name, definition = args.split(" ", 1)
                        name = name.lower()
                except:
                        name = args.split()[0].lower()
                        definition = ""
                if name == "me":
                       room.message("~gives <b>%s</b> %s ~" % (self.getAlias(user.name), definition), True)
                else:
                        if len(name.split()) > 1:
                                room.message("error: no phrases")
                                return
                        elif len(name) > 0:
                                if name not in room.usernames: room.message("<b>%s</b> is not in the room" % self.getAlias(name), True)
                                if name in room.usernames:room.message("~gives <b>%s</b> %s ~" % (self.getAlias(name), definition), True)
        # Command End


        #mod list

        elif used_prefix and cmd == "mods" and self.getAccess(user.name.lower()) > 1:

                r = args

                if len(args) == 0: r = room.name

                if not r: room.message("im not there o-o")

                room.message("The mods are: <b>%s</b> and <b>%s</b> owns it xD"  % (", ".join(self.getRoom(r).modnames), self.getRoom(r).ownername), True)



        #music player

        elif used_prefix and cmd == "next" and user.name == bot_conf.botowner:

                song = random.choice(music)

                webbrowser.open(song)

                room.message("starting next song hope you enjoy it (:")

        #tabs

        elif used_prefix and cmd == "tab" and user.name == bot_conf.botowner:

                url = args

                webbrowser.open_new_tab(url)

                room.message("opening tab in your browser now (:")



        # help command

        elif used_prefix and (cmd == "help" or cmd == "?" or cmd == "commands"):

                chat_message("<a href=\"http://www.wix.com/knight214210/sirbot/\" target=\"_blank\"><b>Command list</b></a>", True)



        # join room

        elif (used_prefix and cmd == "goto" or cmd == "join")  and len(args) > 0 and self.getAccess(user.name.lower()) > 3:

                name = args

                if not args in badrooms: print("[INF] Joining %s..." % args.split()[0])

                if args in badrooms: print("[WAR] Badroom %s detected" % args)

                if not args in badrooms: self.joinRoom(args.split()[0])

                if not args in badrooms: chat_message("Joining <font color='#FF0000'><b>%s</b></font>..." % args, True)

                self.getRoom("debotsch").message("%s made me <b>join %s</b> from %s" % (user.name.title(), name,  room.name), True)

                if args in badrooms: chat_message("<b>%s</b> I can not join <b>%s</b> because its a blacklisted room" % (user.name.title(), args), True)

        elif used_prefix and cmd == "trace":

                if self.getAccess(user.name.lower()) > 4:

                        name = args

                        if name in trace:

                                room.message("%s:[%s]" % (name, message.ip).join(trace), True)



        # Basic "Everyone" Commands



        # We will start importing commands.py here.





########################################################################################

# Bot username password and rooms

########################################################################################



def hexc(e):

        et, ev, tb      = sys.exc_info()

        if not tb: print(str(e))

        while tb:

                lineno = tb.tb_lineno

                fn      = tb.tb_frame.f_code.co_filename

                tb      = tb.tb_next

        print("(%s:%i) %s" % (fn, lineno, str(e)))



if __name__ == "__main__":

        error = 0

        try:

            if os.name == "nt":

                os.system("cls")

            else:

                os.system("clear")

            b.easy_start(rooms, bot_conf.botname, bot_conf.password)

        except KeyboardInterrupt:

            print("[ERR] Console initiated a kill.")

        except Exception as e:

            print("[ERR] Fatal error.")

            error = 1

            hexc(e)
        try:
            for rank in ranks:
                users_tmp = []
                rank = rank.split(',', 4)
                if len(rank) == 4:
                    for person in users:
                        person = person.split(',', 2)
                        if len(person) == 2:
                            user_to_find = "%s" % person[1]
                            search_rank_lvl = "%s" % rank[1]
                            if person[1] in rank[1]:
                                users_tmp.append("%s" % person[0])
                    print("[INF] Saving %s Table" % rank[3])
                    ranks_file = open("storage/flatfile/ranks/%s" % (rank[2]), "w")
                    ranks_file.write("\n".join(users_tmp))
                    ranks_file.close()
        except Exception as e:
            print(e)
        # Save the Definitions Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/various/definitions.txt", "w")
            for word in dictionary:
                definition, name = json.loads(dictionary[word])
                f.write(json.dumps([word, definition, name])+"\n")
            f.close()
            print("[SAV] The Definitions Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Definitions Table does not have to be Saved in SQL Mode...")
        # End Saving the Definitions Table
        # Save the Spam Warnings Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/rooms/spam_warnings.txt", "w")
            f.write("\n".join(spamwarn))
            f.close()
            print("[SAV] The Spam Warnings Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Spam Warnings Table does not have to be Saved in SQL Mode...")
        # End Saving the Spam Warnings Table
        # Save the Banned Words Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/rooms/banned_words.txt", "w")
            f.write("\n".join(cuss))
            f.close()
            print("[SAV] The Banned Words Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Banned Words Table does not have to be Saved in SQL Mode...")
        # End Saving the Banned Words Table
        # Save the Default Rooms Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f2 = rooms
            if bot_conf.defaultRoom in f2: f2.remove(bot_conf.defaultRoom)
            f = open("storage/flatfile/rooms/join_rooms.txt", "w")
            f.write("\n".join(f2))
            f.close()
            print("[SAV] The Default Rooms Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Default Rooms Table does not have to be Saved in SQL Mode...")
        # End Saving the Default Rooms Table
        # Save the Banned Rooms Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/rooms/banned_rooms.txt", "w")
            f.write("\n".join(badrooms))
            f.close()
            print("[SAV] The Banned Rooms Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Banned Rooms Table does not have to be Saved in SQL Mode...")
        # End Saving the Banned Rooms Table
        # Save the User Greets Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/various/greets.txt", "w")
            f.write("\n".join(greets))
            f.close()
            print("[SAV] The User Greets Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The User Greets Table does not have to be Saved in SQL Mode...")
        # End Saving the User Greets Table
        # Save the Music Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/various/music.txt", "w")
            f.write("\n".join(music))
            f.close()
            print("[SAV] The Music Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Music Table does not have to be Saved in SQL Mode...")
        # End Saving the Music Table
        # Save the Tabs Table back to Hardfile..
        if bot_conf.mode.lower() == "flatfile":
            f = open("storage/flatfile/various/tabs.txt", "w")
            f.write("\n".join(tabs))
            f.close()
            print("[SAV] The Tabs Table has been Flushed to Disk...")
        if bot_conf.mode.lower() == "sql":
            print("[SAV] The Tabs Table does not have to be Saved in SQL Mode...")
        # End Saving the Tabs Table
        # Update our Status to "Offline"
        if bot_conf.mode.lower() == "sql":
            try:
                conn = sqlite3.connect('storage/database/bot.db')
            except:
                print("[ERR] Database Connection Failed")
                dbstatus = "error"
            if lockdown == True:
                status = "offline"
                print("[INF] Time to go Sleepy By")
                conn.execute("UPDATE settings SET setting_value = 'offline' WHERE setting_name = 'status'")
            if lockdown == False:
                status = "offline"
                print("[INF] Time to go Sleepy By")
                conn.execute("UPDATE settings SET setting_value = 'offline' WHERE setting_name = 'status'")
            if dbstatus == "available":
                conn.commit()
        if bot_conf.mode.lower() == "flatfile":
            if lockdown == True:
                status = "offline"
                filename = "storage/flatfile/bot/status.txt"
                file = open(filename, 'w')
                print("[INF] Time to go Sleepy By")
                file.write("Offline")
                file.close()
            if lockdown == False:
                status = "offline"
                filename = "storage/flatfile/bot/status.txt"
                file = open(filename, 'w')
                print("[INF] Time to go Sleepy By")
                file.write("Offline")
                file.close()
        # End Status Update
        if error == 1:
                print("Waiting 10 seconds for you to read the error..")
                time.sleep(10)
        print("[INF] Shutting down..")
########################################################################################
