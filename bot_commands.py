        # These commands are maintained by the bot developers. If you are interested in having a command you wrote here, contact the bot developer. Your commands go in commands.py
        
        # Command Usage: 'whois <username>
        if used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_whois and cmd == "whois" and len(args) > 0:
            if len(self.api("whois_check", args, "")) > 0:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, I found %s with the following accounts: %s</font>" % (font_color, font_face, font_size, self.getAlias(user.name), args, ", ".join(self.api("whois_check", args, ""))), True)
            else:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, I don't know anything about that account yet.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
        
        # Command Usage: "<botname>, would you like to play a game?" / Games: flipcoin (fc), spin-the-bottle (sb), Magic 8-Ball (8ball), Russian Roulette (rr)
        elif self.getAccess(user.name) >= lvl_config.rank_req_game_list and message.body.lower() == "%s, would you like to play a game?" % bot_conf.botname.lower():
            try:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> I can play <b>flip a coin (%sfc)</b>, <b>spin-the-bottle (%ssb)</b>, <b>Magic 8-Ball (%s8ball)</b>, and <b>Russian Roulette(%srr)</b>. I have many more games to come! ^^</font>" % (font_color, font_face, font_size, self.getAlias(user.name), bot_conf.prefix, bot_conf.prefix, bot_conf.prefix, bot_conf.prefix), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: games] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Command End
        
        # Command Usage: 'fc, 'flipcoin
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_game_fc and (cmd == "flipcoin" or cmd == "fc"):
            try:
                chat_message("<font color='#%s' face='%s' size='%s'>%s</font>" % (font_color, font_face, font_size, random.choice(["%s flips a coin and gets heads" % self.getAlias(user.name), "%s flips a coin and gets tails" % self.getAlias(user.name), "%s flips a coin and it lands on it's edge" % self.getAlias(user.name), "%s flips a coin and it falls off the table o-o" % self.getAlias(user.name), "%s flips a coin and it hits %s in the face O-O" % (self.getAlias(user.name), random.choice(room.usernames)),])), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: game_flipcoin] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Command End

        # Command Usage: 'rr, 'russian-roulette
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_game_rr and (cmd == "russian-roulette" or cmd =="rr"):
            try:
                chat_message("<font color='#%s' face='%s' size='%s'>%s</font>" % (font_color, font_face, font_size, random.choice(["%s -spins the cylinder and points it at %s- click" % (self.getAlias(user.name), random.choice(room.usernames)), "%s -spins the cylinder and points it at %s- BOOM, they is keeled." % (self.getAlias(user.name), random.choice(room.usernames)), "%s -spins the cylinder and points it at %s- click.. -fires it again- *BOOM* they is keeled." % (self.getAlias(user.name), random.choice(room.usernames))])), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: ty] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Command End
        
        # Command Usage: 'banvote <username>
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_cmd_vote and cmd == "banvote" and len(args) > 0:
            try:
                if args in self.getRoom(room.name).modnames or args in self.getRoom(room.name).ownername:
                    chat_message("<font color='#%s' face='%s' size='%s'>You cannot request a banvote against a moderator. If you have issues with moderators please report them to the chat owner: <b>%s</b></font>" % (font_color, font_face, font_size, self.getRoom(room.name).ownername), True)
                else:
                    if self.getAccess(user.name) > 2:
                        banvote_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        banvote_user = args
                        banvote = "yes"
                        banvote_status = "banvote initiated"
                        try:
                            with open("storage/update/banvote_%s.txt" % room.name, "r") as file:
                                data = file.readlines()
                                try:
                                    if "banvote initiated" in data[0]:
                                        banvote = "no"
                                except:
                                    banvote = "yes"
                        except:
                            banvote = "yes"

                        if banvote == "yes":
                            chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has initiated a vote to ban <b>%s</b> from the chat, all in favor type '<b>vote yes</b>' if not in favor type '<b>vote no</b>', your vote will only be counted once. You have <b>2 minutes</b> to vote.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), args), True)
                            banvote_data = []
                            banvote_data.append(banvote_status)
                            banvote_data.append(banvote_user)
                            banvote_data.append(banvote_time)
                            
                            # Save the Banvote Table back to Hardfile..
                            if bot_conf.mode.lower() == "flatfile":
                                f = open("storage/update/banvote_%s.txt" % room.name, "w")
                                f.write("\n".join(banvote_data))
                                f.close()
                                print("[SAV] The Banvote Table has been Flushed to Disk...")
                            if bot_conf.mode.lower() == "sql":
                                print("[SAV] The Banvote Table does not have to be Saved in SQL Mode...")
                            # End Saving the Banvote Table
                        else:
                            chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, I already have an active banvote in progress. Type '<b>vote yes</b>' or '<b>vote no</b>' to vote, voting lasts for 2 minutes.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: banvote_initiate] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Command End
        # Ban Vote No, Start
        elif self.getAccess(user.name) >= lvl_config.rank_req_vote and message.body.lower() == "vote no":
            try:
                voted_flag = 0
                banvote = "no"
                
                # Populate vote_yes & vote_no
                try:
                    f = open("storage/update/banvote_yes_%s.txt" % room.name, "r")
                    vy = f.readlines()
                except:
                    vy = []
                    vy.append("0")
                try:
                    vote_y = float(vy[0])
                    vote_y = vy[0]
                except:
                    vote_y = 0
                vote_yes = vote_y
                try:
                    f.close()
                except:
                    print("There was no banvote file for %s" % room.name)
                try:
                    f = open("storage/update/banvote_no_%s.txt" % room.name, "r")
                    vn = f.readlines()
                except:
                    vn = []
                    vn.append("0")
                try:
                    vote_n = float(vn[0])
                    vote_n = vn[0]
                except:
                    vote_n = 0
                vote_no = vote_n
                try:
                    f.close()
                except:
                    print("There was no banvote file for %s" % room.name)
                # End Populate
                bv_data = []
                try:
                    f = open("storage/update/banvote_%s.txt" % room.name, "r")
                    for line in f.readlines():
                        dat = line.strip('\n')
                        bv_data.append(dat)
                except:
                    print("No file, meaning banvote = no")
                    
                if len(bv_data) == 3:
                    banvote = "yes"
                    banvote_time = bv_data[2]
                    banvote_user = bv_data[1]
                else: 
                    banvote = "no"
                    
                if banvote == "no":
                    banvote_time = "not set"
                try:
                    f.close()
                except Exception as e:
                    print(e)
                if banvote_time == "not set":
                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> a banvote has not been initiated yet. Please try again after a Trusted member or higher has initiated one.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                else:
                    time_format = "%Y-%m-%d %H:%M:%S"
                    difference = datetime.datetime.now() - datetime.datetime.fromtimestamp(time.mktime(time.strptime(banvote_time, time_format)))
                    if difference.seconds > 120:
                        if int(vote_yes) > int(vote_no) and int(vote_yes) + int(vote_no) >= 10:
                            chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has been banned.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            room.clearUser(ch.User(banvote_user))
                            room.banUser(ch.User(banvote_user))
                            try:
                                os.unlink("storage/update/banvote_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_no_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_yes_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/voted_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            banvote_time = "not set"
                            banvote_user = "not set"
                        else:
                            if int(vote_yes) + int(vote_no) < 10:
                                chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has not been banned. Reason: Insufficient number of votes.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            else:
                                chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has not been banned. Reason: Members Voted against Ban.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            last_banvote_user = banvote_user
                            banvote_user = "not set"
                            banvote_time = "not set"
                            try:
                                os.unlink("storage/update/banvote_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_no_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_yes_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/voted_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                    else:
                        try:
                            data_file = open("storage/update/voted_%s.txt" % room.name, "r")
                            for line in data_file.readlines():
                                if user.name in line:
                                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, you have already voted. You may only vote once in any particular ban vote.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                                    voted_flag = 1
                            data_file.close()
                        except Exception as e:
                            print(e)
                        if voted_flag == 0:        
                            vote_data = []
                            if int(vote_yes) == vote_yes:
                                vote_yes = vote_yes
                            else:
                                vote_yes = int(vote_yes)
                                
                            if int(vote_no) == vote_no:
                                vote_no = vote_no + 1
                            else:
                                vote_no = int(vote_no) + 1
                            vote_data.append(str(vote_no))
                            # Save the Banvote Table back to Hardfile..
                            if bot_conf.mode.lower() == "flatfile":
                                f = open("storage/update/banvote_no_%s.txt" % room.name, "w")
                                f.write("\n".join(vote_data))
                                f.close()
                                print("[SAV] The Banvote Table has been Flushed to Disk...")
                            if bot_conf.mode.lower() == "sql":
                                print("[SAV] The Banvote Table does not have to be Saved in SQL Mode...")
                            # End Saving the Banvote Table
                            # Load the Owners User Table
                            if bot_conf.mode.lower() == "flatfile":
                                banvote_voters = []
                                try:
                                    f = open("storage/update/voted_%s.txt" % room.name, "r")
                                    for name in f.readlines():
                                        if len(name.strip())>0: banvote_voters.append(name.strip())
                                    print("[INF] Loading Owners... %s" % len(banvote_voters))
                                    f.close()
                                except Exception as e:
                                    print(e)
                                banvote_voters.append(user.name)
                            # End Loading the Owners
                            # Save the Banvote Table back to Hardfile..
                            if bot_conf.mode.lower() == "flatfile":
                                f = open("storage/update/voted_%s.txt" % room.name, "w")
                                f.write("\n".join(banvote_voters))
                                f.close()
                                print("[SAV] The Banvote Voter Table has been Flushed to Disk...")
                            if bot_conf.mode.lower() == "sql":
                                print("[SAV] The Banvote Voter Table does not have to be Saved in SQL Mode...")
                            # End Saving the Banvote Table
                            chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has voted against the banning of <b>%s</b> from the chat. There are currently <b>%s</b> votes in favor and <b>%s</b> votes against.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), banvote_user, vote_yes, vote_no), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: banvote_yes] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Ban Vote No Complete
        # Ban Vote Yes, Start
        elif self.getAccess(user.name) >= lvl_config.rank_req_vote and message.body.lower() == "vote yes":
            try:
                voted_flag = 0
                banvote = "no"
                
                # Populate vote_yes & vote_no
                try:
                    f = open("storage/update/banvote_yes_%s.txt" % room.name, "r")
                    vy = f.readlines()
                except:
                    vy = []
                    vy.append("0")
                try:
                    vote_y = float(vy[0])
                    vote_y = vy[0]
                except:
                    vote_y = 0
                vote_yes = vote_y
                try:
                    f.close()
                except:
                    print("There was no banvote file for %s" % room.name)
                try:
                    f = open("storage/update/banvote_no_%s.txt" % room.name, "r")
                    vn = f.readlines()
                except:
                    vn = []
                    vn.append("0")
                try:
                    vote_n = float(vn[0])
                    vote_n = vn[0]
                except:
                    vote_n = 0
                vote_no = vote_n
                try:
                    f.close()
                except:
                    print("There was no banvote file for %s" % room.name)
                # End Populate
                bv_data = []
                try:
                    f = open("storage/update/banvote_%s.txt" % room.name, "r")
                    for line in f.readlines():
                        dat = line.strip('\n')
                        bv_data.append(dat)
                except:
                    print("No file, meaning banvote = no")
                if len(bv_data) == 3:
                    banvote = "yes"
                    banvote_time = bv_data[2]
                    banvote_user = bv_data[1]
                else: 
                    banvote = "no"
                    
                if banvote == "no":
                    banvote_time = "not set"
                try:
                    f.close()
                except Exception as e:
                    print(e)
                if banvote_time == "not set":
                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> a banvote has not been initiated yet. Please try again after a Trusted member or higher has initiated one.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                else:
                    time_format = "%Y-%m-%d %H:%M:%S"
                    difference = datetime.datetime.now() - datetime.datetime.fromtimestamp(time.mktime(time.strptime(banvote_time, time_format)))
                    if difference.seconds > 120:
                        if int(vote_yes) > int(vote_no) and int(vote_yes) + int(vote_no) >= 10:
                            chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has been banned.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            room.clearUser(ch.User(banvote_user))
                            room.banUser(ch.User(banvote_user))
                            try:
                                os.unlink("storage/update/banvote_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_no_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_yes_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/voted_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            banvote_time = "not set"
                            banvote_user = "not set"
                        else:
                            if int(vote_yes) + int(vote_no) < 10:
                                chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has not been banned. Reason: Insufficient number of votes.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            else:
                                chat_message("<font color='#%s' face='%s' size='%s'>Voting has ended! Here's the line up [ In Favor: %s, Against: %s ]. The member, %s, has not been banned. Reason: Members Voted against Ban.</font>" % (font_color, font_face, font_size, str(vote_yes), str(vote_no), banvote_user), True)
                            last_banvote_user = banvote_user
                            banvote_user = "not set"
                            banvote_time = "not set"
                            try:
                                os.unlink("storage/update/banvote_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_no_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/banvote_yes_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                            try:
                                os.unlink("storage/update/voted_%s.txt" % room.name)
                            except Exception as e:
                                print(e)
                    else:
                        try:
                            data_file = open("storage/update/voted_%s.txt" % room.name, "r")
                            for line in data_file.readlines():
                                if user.name in line:
                                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, you have already voted. You may only vote once in any particular ban vote.</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
                                    voted_flag = 1
                            data_file.close()
                        except Exception as e:
                            print(e)
                        if voted_flag == 0:        
                            vote_data = []
                            if int(vote_yes) == vote_yes:
                                vote_yes = vote_yes + 1
                            else:
                                vote_yes = int(vote_yes) + 1
                                
                            if int(vote_no) == vote_no:
                                vote_no = vote_no
                            else:
                                vote_no = int(vote_no)
                            vote_data.append(str(vote_yes))
                            # Save the Banvote Table back to Hardfile..
                            if bot_conf.mode.lower() == "flatfile":
                                f = open("storage/update/banvote_yes_%s.txt" % room.name, "w")
                                f.write("\n".join(vote_data))
                                f.close()
                                print("[SAV] The Banvote Table has been Flushed to Disk...")
                            if bot_conf.mode.lower() == "sql":
                                print("[SAV] The Banvote Table does not have to be Saved in SQL Mode...")
                            # End Saving the Banvote Table
                            # Load the Owners User Table
                            if bot_conf.mode.lower() == "flatfile":
                                banvote_voters = []
                                try:
                                    f = open("storage/update/voted_%s.txt" % room.name, "r")
                                    for name in f.readlines():
                                        if len(name.strip())>0: banvote_voters.append(name.strip())
                                    print("[INF] Loading Owners... %s" % len(banvote_voters))
                                    f.close()
                                except Exception as e:
                                    print(e)
                                banvote_voters.append(user.name)
                            # End Loading the Owners
                            # Save the Banvote Table back to Hardfile..
                            if bot_conf.mode.lower() == "flatfile":
                                f = open("storage/update/voted_%s.txt" % room.name, "w")
                                f.write("\n".join(banvote_voters))
                                f.close()
                                print("[SAV] The Banvote Voter Table has been Flushed to Disk...")
                            if bot_conf.mode.lower() == "sql":
                                print("[SAV] The Banvote Voter Table does not have to be Saved in SQL Mode...")
                            # End Saving the Banvote Table
                            chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> has voted in favor of banning <b>%s</b> from the chat. There are currently <b>%s</b> votes in favor and <b>%s</b> votes against.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), banvote_user, vote_yes, vote_no), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: banvote_no] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Ban Vote Yes Complete
        
        # Command Usage: 'broadcast, 'a, 'announce, 'bcast
        elif used_prefix and (cmd == "broadcast" or cmd == "a" or cmd == "announce" or cmd == "bcast") and len(args) >0 and self.getAccess(user.name) >= lvl_config.rank_req_gnews:
            try:
                originating_room = room.name    
                for room in self.rooms:
                    chat_message("<font color='#%s' face='%s' size='%s'><b><i>Global Announcement:</i></b> %s by <b>%s</b> in <b>%s</b></font>" %(font_color, font_face, font_size, args, self.getAlias(user.name), originating_room), True)
            except Exception as e:
                error_log_file = open("storage/flatfile/logs/error.log", "a")
                error_log_file.write("[%s] [Error:] %s [Command: broadcast] \n" % (cur_msg_time, e))
                error_log_file.close()
        # Command End
        
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_game_sb and (cmd == "spin-bottle" or cmd == "sb"):
                chat_message("<b>%s</b> spins the bottle after it spins it lands on <b>%s</b> ^^" % (self.getAlias(user.name), random.choice(room.usernames)), True)
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_fun_parkour and cmd == "parkour":
                chat_message(random.choice(["Does a backflip xD", "Does a frontflip xD", "Climbs a high wall and freeruns off of it w00t", "Leaps off a bridge into a ravine brining yer mum with him. BICH",]))
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_fun_fap and cmd == "fap":
                chat_message("<b>%s</b>, faps to <b>%s</b>" % self.getAlias(user.name), random.choice(fapthings), True)

        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_game_8ball and cmd == "8ball" and len(args) > 0:
                                  chat_message("<i>The 8ball says</i> - <b>%s</b> -" % (random.choice(persona.eightball)), True)

        if used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_cmd_rfact and (cmd == "rf" or cmd == "randomfact"):
                chat_message("<b>%s</b> did you know: <b>%s</b>" % (self.getAlias(user.name), random.choice(randomfacts)), True)
        if used_prefix and cmd == "udict" and len(args) >= 1 and self.getAccess(user.name) >= lvl_config.rank_req_cmd_udict:
            try:
                term = args.split(" ", 1)
                import urllib.request
                with urllib.request.urlopen("http://www.urbandictionary.com/define.php?term=%s" % term[0]) as url:
                    udict = url.read().decode()
                a = re.finditer('<div class="definition">(.+?)</div>', udict)
                matches = []
                for match in a:
                    matches.append(match.group(0))
                chat_message("<font color='#%s' face='%s' size='%s'><br><b>defintion of %s:</b><br><br><i>%s</i></font>" % (font_color, font_face, font_size, term[0], random.choice(matches)), True)
            except Exception as e:
                chat_message("<font color='#%s' face='%s' size='%s'>I was unable to find anything for that term.</font>" % (font_color, font_face, font_size), True)
                
        # Command Usage: 'gis <terms>        
        elif used_prefix and cmd == "gis" and self.getAccess(user.name) >= lvl_config.rank_req_image_search:
            try:
                search = args.split()
                import urllib.request
                with urllib.request.urlopen("http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=%s" % "+".join(search)) as url:
                    udict = url.read().decode()
                a = re.finditer('"unescapedUrl":"(.+?)","url":"', udict)
                matches = []
                for match in a:
                    match = str(match.group(1))
                    matches.append(match)
                
                link = random.choice(matches)
                try:
                    link = link.replace("https", "http")
                except:
                    print("Random choice isn't SSL.")
                if not args in cuss: chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> I found:</font> %s" % (font_color, font_face, font_size, self.getAlias(user.name), link), True)
                if args in cuss: chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>. Tsk tsk. Looking up naughty things, shame on you! :|</font>" % (font_color, font_face, font_size, self.getAlias(user.name)), True)
            except Exception as e:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> I'm sorry, I was unable to find anything for search term: %s :|</font>" % (font_color, font_face, font_size, self.getAlias(user.name), args), True)
                print(e)
        # Command End
        
        # Command Usage: 'tube <terms>, 'ytb <terms>, 'yt <terms>
        elif used_prefix and (cmd == "tube" or cmd == "ytb" or cmd == "yt") and self.getAccess(user.name) >= lvl_config.rank_req_youtube_search:
            try:
                search = args.split()
                import urllib.request
                with urllib.request.urlopen("http://gdata.youtube.com/feeds/api/videos?vq=%s&racy=include&orderby=relevance&max-results=1" % "+".join(search)) as url:
                    udict = url.read().decode()
                a = re.finditer('http://www.youtube.com/watch\?v=(.+?)&amp;', udict)
                matches = []
                for match in a:
                    match = str(match.group(0))
                    match = match[:42]
                    matches.append(match)
                
                id = random.choice(matches)
                id = id[31:]
                link = "http://www.youtube.com/watch?v=%s" % id
                info = youtube.Video(id)
                info_title = "%s..." % info.get_title()[:50]
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> I Found: \"%s\" by %s. %s</font>" % (font_color, font_face, font_size, self.getAlias(user.name), info_title, info.get_auth()[:50], link), True)
            except Exception as e:
                chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> I'm sorry, I was unable to find anything for search term: %s :|</font>" % (font_color, font_face, font_size, self.getAlias(user.name), args), True)
                print(e)
        # Command End
        
        # Command Usage: 'ld, 'lockdown, 'ld release, 'lockdown release
        elif used_prefix and (cmd == "ld"or cmd == "lockdown") and self.getAccess(user.name) >= lvl_config.rank_req_lockdown:
            if len(args.split()) > 0 and args.split()[0].lower() == "release" or len(args.split()) > 0 and args.split()[0].lower() == "rl":
                lockdown = False
                self.getRoom("debotsch").message("lockdown mode deactivated by %s in %s" % (user.name.title(), room.name))
                chat_message("<font color='#33FF00'>System Restored to Normal</font> :) ", True)
                filename ="storage/flatfile/bot/status.txt"
                print("[INF]Setting status to normal mode...")
                file = open(filename, 'w')
                file.write("Online and playing")
                file.close()
            else:
                lockdown = True
                filename = "storage/flatfile/bot/status.txt"
                file = open(filename, 'w')
                print("[INF]Setting status to lockdown...")
                file.write("in lockdown mode")
                file.close()
                self.getRoom("debotsch").message("lockdown mode activated by %s in %s" % (user.name.title(), room.name))
                chat_message("<font color='#FF0000'>System LockDown</font> :|", True)
        # Command End
        
        # Command Usage: 'find <username>
        elif used_prefix and (cmd == "find" or cmd =="locate") and len(args) > 0 and self.getAccess(user.name) >= lvl_config.rank_req_cmd_find:
            try:
                name = args.split()[0].lower()
                if ch.User(name).roomnames: 
                    if name == "me":
                        chat_message("<font color='#%s' face='%s' size='%s'>Silly, yewr here with me. ^_^</font>" % (font_color, font_face, font_size), True)
                    elif name == bot_conf.botname.lower():
                        chat_message("<font color='#%s' face='%s' size='%s'>~cricket chirps~ Srsly? :|</font>" % (font_color, font_face, font_size), True)
                    else:
                        chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, I found %s in <b>%s</b>.</font>" % (font_color, font_face, font_size, self.getAlias(user.name), self.getAlias(name), ", ".join(ch.User(name).roomnames)), True)
                else:
                    chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, Sorry.. I couldn't find %s in any of the rooms I am currently in.. :|</font>" % (font_color, font_face, font_size, user.name.title(), name), True)
            except Exception as e:
                print(e)
        # Command End
        
        # Command Usage: 'rooms, 'rooms join roomname, 'rooms leave roomname
        elif used_prefix and cmd =="rooms" and self.getAccess(user.name) >= lvl_config.rank_req_rooms_list:
            f2 = []
            f2 = rooms
            doit = []
            roomit = []
            try:
                cmd_text = args.split(" ", 1)
            except:
                print("No Args")
            try:
                doit = cmd_text[0]
                roomit = cmd_text[1]
            except:
                doit = "list"
                roomit = ""
                
            if doit == "join" and lvl_config.rank_req_rooms_join:
                if roomit in f2: f2.remove(roomit)
                rooms.append(roomit)
                # Save the Default Rooms Table back to Hardfile..
                if bot_conf.mode.lower() == "flatfile":
                    if bot_conf.defaultRoom in f2: f2.remove(bot_conf.defaultRoom)
                    f = open("storage/flatfile/rooms/join_rooms.txt", "w")
                    f.write("\n".join(f2))
                    f.close()
                    print("[SAV] The Default Rooms Table has been Flushed to Disk...")
                if bot_conf.mode.lower() == "sql":
                    print("[SAV] The Default Rooms Table does not have to be Saved in SQL Mode...")
                # End Saving the Default Rooms Table
                chat_message("<font color='#%s' face='%s' size='%s'>I have added the room <b>%s</b> to the list. If you haven't done so yet, type %sjoin %s to send me to that room.</font>" % (font_color, font_face, font_size, roomit, prefix, roomit), True)
            elif doit == "leave" and lvl_config.rank_req_rooms_leave:
                # Save the Default Rooms Table back to Hardfile..
                if bot_conf.mode.lower() == "flatfile":
                    if bot_conf.defaultRoom in f2: f2.remove(bot_conf.defaultRoom)
                    if roomit in f2: f2.remove(roomit)
                    f = open("storage/flatfile/rooms/join_rooms.txt", "w")
                    f.write("\n".join(f2))
                    f.close()
                    print("[SAV] The Default Rooms Table has been Flushed to Disk...")
                if bot_conf.mode.lower() == "sql":
                    print("[SAV] The Default Rooms Table does not have to be Saved in SQL Mode...")
                # End Saving the Default Rooms Table
                chat_message("<font color='#%s' face='%s' size='%s'>I have removed the room <b>%s</b> from the list. If you haven't done so yet, type %sleave %s to make me exit that room.</font>" % (font_color, font_face, font_size, roomit, prefix, roomit), True)
            elif doit == "list":
                if bot_conf.defaultRoom in f2: f2.remove(bot_conf.defaultRoom)
                chat_message("<font color='#%s' face='%s' size='%s'>I can be found in: <b>%s</b></font>" % (font_color, font_face, font_size, ", ".join(f2)), True)
        # Command End
        
        # Command Usage: 'unban <username>, 'ub <username>
        elif used_prefix and (cmd == "unban" or cmd == "ub") and len(args) > 0 and self.getAccess(user.name) >= lvl_config.rank_req_unban:
            name = args
            room.unban(ch.User(name))
            chat_message ("<font color='#%s' face='%s' size='%s'><b>%s</b>, you have been unbanned by <b>%s</b>. Please behave and follow the rules of the chat so you don't get banned again. Thanks!</font>" % (font_color, font_face, font_size, self.getAlias(name), self.getAlias(user.name)), True)
            self.pm.message(ch.User(name.lower()), "You have been unbanned from %s by %s. Please behave and follow the rules of the chat so you don't get banned again. Thanks!" % (room.name, self.getAlias(user.name)))
        # Command End
        
        # Command Usage: 'uptime or 'ut
        elif used_prefix and self.getAccess(user.name) >= lvl_config.rank_req_cmd_ut and (cmd == "ut" or cmd == "uptime"):
            try:
                current_time = datetime.datetime.now()
                diff = current_time - bot_startup_time
                
                seconds = diff.seconds
                
                minutes, seconds = divmod(seconds, 60)
                hours, minutes = divmod(minutes, 60)
                days, hours = divmod(hours, 24)

                #hours, remainder = divmod(diff.seconds, 3600)
                #minutes, seconds = divmod(remainder, 60)
                
                if days == 0 and hours == 0 and minutes == 0:
                    bot_uptime = "%s second(s)" % (seconds)
                elif days == 0 and hours == 0 and minutes != 0:
                    bot_uptime = "%s minutes(s) and %s second(s)" % (minutes, seconds)
                elif days == 0 and hours != 0:
                    bot_uptime = "%s hours(s), %s minutes(s) and %s second(s)" % (hours, minutes, seconds)
                else:
                    bot_uptime = "%s day(s), %s hours(s), %s minutes(s) and %s second(s)" % (days, hours, minutes, seconds)
                chat_message("<font color='#%s' face='%s' size='%s'>My systems have been active for <b>%s</b>. ^^</font>" % (font_color, font_face, font_size, bot_uptime), True)
            except Exception as e:
                print(e)
        # Command End
        
        # Command Usage: 'df <term>, 'df <term> as <definition>, 'df rem <term>
        elif used_prefix and (cmd == "df" or cmd == "define" or cmd == "def") and self.getAccess(user.name) >= lvl_config.rank_req_define:
            if os.path.exists('storage/flatfile/various/dict.xml'):
                print("")
            else:
                f = open("storage/flatfile/various/dict.xml", "w")
                f.write("<root></root>")
                f.close()
            file = open("storage/flatfile/various/aliases.csv", "r")
            alias_flag = 0
            nickname = user.name
            for line in file.readlines():
            
                alias_data = line.strip()
                alias_username, alias_nickname = alias_data.split(",", 1)
                # Fill Temporary Variables with the Split Line
                
                if user.name in alias_username:
                    nickname = alias_nickname
                    alias_flag = 1
                    
            file.close()
            try:
                cont_df = args.split()

                req_term = ""
                mode = ""
                
                
                if len(cont_df) == 1:
                    req_term = cont_df[0]
                elif len(cont_df) == 2:
                    req_term = cont_df[0]
                    mode = cont_df[1]
                elif len(cont_df) > 2:
                    req_term = cont_df[0]
                    mode = cont_df[1]
            except Exception as e:
                print(e)
                print("Couldn't set 'req_term' or 'mode'")
                req_term = ""
                mode = ""
                
            try:
                data_df = args.split()
                
                if len(data_df) >= 3:
                    del data_df[0]
                    del data_df[0]
                    definition = "%s" % (" ".join(data_df))
                else:
                    definition = ""
            except Exception as e:
                print(e)
                print("Couldn't set 'definition'")
                definition = ""
            try:
                define_flag = 0
                define_term = ""
                define_auth = ""
                define_def = ""
                define_date = ""
                defin = ""
                term = ""
                auth = ""
                term_d = ""
                if mode == "as":
                    # Check to see if defined.
                    import xml.etree.ElementTree as XMLElementTree
                    
                    tree = XMLElementTree.parse('storage/flatfile/various/dict.xml')
                    root = tree.getroot()
                    child_data = []
                    child_data.append("<root>")
                    for child in root:
                        if child[0].text == req_term:
                            defin = child[1].text
                            term = child[0].text
                            auth = child[2].text
                            term_d = child[3].text
                            define_flag = 1                                
                        if child[0].text != req_term:
                            child_data.append("<entry name='%s'>" % (child[0].text))
                            child_data.append("<term>%s</term>" % (child[0].text))
                            child_data.append("<def>%s</def>" % (child[1].text))
                            child_data.append("<by>%s</by>" % (child[2].text))
                            child_data.append("<on>%s</on>" % (child[3].text))
                            child_data.append("</entry>")
                        
                    current_date_def = str(datetime.datetime.now())
                    current_def_def = definition
                    current_def_term = req_term
                    current_def_auth = user.name  
                    if define_flag == 1:
                        has_auth = 0
                        if user.name == auth:
                            # We have found the term in the xml, check if the user is the auth.
                            child_data.append("<entry name='%s'>" % (current_def_term))
                            child_data.append("<term>%s</term>" % (current_def_term))
                            child_data.append("<def>%s</def>" % (current_def_def))
                            child_data.append("<by>%s</by>" % (current_def_auth))
                            child_data.append("<on>%s</on>" % (current_date_def))
                            child_data.append("</entry>")
                            child_data.append("</root>")
                            has_auth = 1
                        elif self.getAccess(user.name) >= lvl_config.rank_req_udef_mast:
                            # We have found the term in the xml, check if the user is the auth.
                            child_data.append("<entry name='%s'>" % (current_def_term))
                            child_data.append("<term>%s</term>" % (current_def_term))
                            child_data.append("<def>%s</def>" % (current_def_def))
                            child_data.append("<by>%s</by>" % (current_def_auth))
                            child_data.append("<on>%s</on>" % (current_date_def))
                            child_data.append("</entry>")
                            child_data.append("</root>")
                            has_auth = 1
                        else:
                            child_data.append("<entry name='%s'>" % (term))
                            child_data.append("<term>%s</term>" % (term))
                            child_data.append("<def>%s</def>" % (defin))
                            child_data.append("<by>%s</by>" % (auth))
                            child_data.append("<on>%s</on>" % (term_d))
                            child_data.append("</entry>")
                            child_data.append("</root>")
                            has_auth = 0
                        
                        if has_auth == 1:
                            chat_message("<font color='#%s' face='%s' size='%s'>Defined <b>%s</b> as <b><i>%s</i></b> by <b>%s</b></font>" % (font_color, font_face, font_size, current_def_term, current_def_def, nickname), True)
                        else:
                            chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b> was defined by <b><i>%s</i></b> already.<br><br>Term: <b>%s</b><br>Definition: <i>%s</i></font>" % (font_color, font_face, font_size, current_def_term, auth, current_def_term, defin), True) 
                    else:
                        child_data.append("<entry name='%s'>" % (current_def_term))
                        child_data.append("<term>%s</term>" % (current_def_term))
                        child_data.append("<def>%s</def>" % (current_def_def))
                        child_data.append("<by>%s</by>" % (current_def_auth))
                        child_data.append("<on>%s</on>" % (current_date_def))
                        child_data.append("</entry>")
                        child_data.append("</root>")

                        chat_message("<font color='#%s' face='%s' size='%s'>Defined <b>%s</b> as <b><i>%s</i></b> by <b>%s</b></font>" % (font_color, font_face, font_size, current_def_term, current_def_def, nickname), True)
                        
                    # Write changes back to xml file.    
                    f = open("storage/flatfile/various/dict.xml", "w")
                    f.write("\n".join(child_data))
                    f.close()
                    
                elif (req_term == "rem" or req_term == "remove") and mode != "" and len(cont_df) == 2:
                    import xml.etree.ElementTree as XMLElementTree
                    tree = XMLElementTree.parse('storage/flatfile/various/dict.xml')
                    root = tree.getroot()
                    child_data = []
                    child_data.append("<root>")
                    define_flag = 0
                    has_auth = 0
                    for child in root:
                        if child[0].text == mode:
                            defin = child[1].text
                            term = child[0].text
                            auth = child[2].text
                            term_d = child[3].text
                            if user.name in auth:                
                                define_flag = 1
                                has_auth = 1
                            elif self.getAccess(user.name) >= lvl_config.rank_req_udef_mast:
                                define_flag = 1
                                has_auth = 1
                            else:
                                child_data.append("<entry name='%s'>" % (child[0].text))
                                child_data.append("<term>%s</term>" % (child[0].text))
                                child_data.append("<def>%s</def>" % (child[1].text))
                                child_data.append("<by>%s</by>" % (child[2].text))
                                child_data.append("<on>%s</on>" % (child[3].text))
                                child_data.append("</entry>")
                                has_auth = 0
                                define_flag = 1
                                
                                
                        if child[0].text != mode:
                            child_data.append("<entry name='%s'>" % (child[0].text))
                            child_data.append("<term>%s</term>" % (child[0].text))
                            child_data.append("<def>%s</def>" % (child[1].text))
                            child_data.append("<by>%s</by>" % (child[2].text))
                            child_data.append("<on>%s</on>" % (child[3].text))
                            child_data.append("</entry>")
                            
                    current_date_def = str(datetime.datetime.now())
                    current_def_def = definition
                    current_def_term = mode
                    current_def_auth = user.name
                    
                    if define_flag == 1 and has_auth == 1:
                        # We have found the term in the xml, check if the user is the auth.
                        
                        child_data.append("</root>")
                        f = open("storage/flatfile/various/dict.xml", "w")
                        f.write("\n".join(child_data))
                        f.close()
                        
                        chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, I have removed the term <b>%s</b> as requested.</font>" % (font_color, font_face, font_size, nickname, current_def_term), True)
                    elif define_flag == 1 and has_auth == 0:
                        chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, tsk tsk.. trying to remove: <b>%s</b>.. You no has permissions.</font>" % (font_color, font_face, font_size, nickname, current_def_term), True)
                    elif define_flag == 0 and self.getAccess(user.name) < lvl_config.rank_req_udef_mast:
                        chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, tsk tsk.. trying to use a remove command. Not only do you not have permission, but that word doesn't even exist in my dictionary. :|</font>" % (font_color, font_face, font_size, nickname), True)
                    else:
                        chat_message("<font color='#%s' face='%s' size='%s'><b>%s</b>, That word doesn't exist in my dictionary.</font>" % (font_color, font_face, font_size, nickname), True)
                else:
                    try:
                        import xml.etree.ElementTree as XMLElementTree
                        trunk = XMLElementTree.parse('storage/flatfile/various/dict.xml')
                        branches = trunk.getroot()
                        def_found_flag = 0
                        try:
                            for item in branches:
                                if item[0].text == req_term:
                                    lookup_term = item[0].text
                                    lookup_definition = item[1].text
                                    lookup_user = item[2].text
                                    lookup_date = item[3].text
                                    def_found_flag = 1
                        except Exception as e:
                            print("Term not found.")
                                
                        if def_found_flag == 1:
                            chat_message("<font color='#%s' face='%s' size='%s'><br><b>%s</b>, I found:<br><br>Term: <b>%s</b><br>Definition: <i>%s</i></font>" % (font_color, font_face, font_size, nickname, req_term, lookup_definition), True)
                        else:
                            chat_message("<font color='#%s' face='%s' size='%s'><br><b>%s</b>, I couldn't find that term (%s). Try defining it by using <b>%sdf %s as definition</b>.</font>" % (font_color, font_face, font_size, nickname, req_term, prefix, req_term), True)
                    except Exception as e:
                        print(e)
                        print("I couldn't complete the lookup of term.")
            except Exception as e:
                # prop isn't set, meaning we're just viewing the term
                print(e)
        # Command End  

        # Command Usage: 'update
        elif used_prefix and cmd == "update" and self.getAccess(user.name) >= lvl_config.rank_lvl_botowner:
            self.set_timeout("update")
            if self.checkUpdate() == "Updated":
                if os.name == "nt":
                    # Re-Launch Launch.bat
                    self.setTimeout(5, subprocess.Popen(['launch.bat', '']))
                    self.setTimeout(5, self.stop)
                else:
                    # Re-Launch Launch.sh
                    self.setTimeout(5, subprocess.Popen(['/bin/bash', 'launch.sh']))
                    self.setTimeout(5, self.stop)
            elif self.checkUpdate() == "Error":
                chat_message("<font color='#%s' face='%s' size='%s'>There was an error while updating..</font>" % (font_color, font_face, font_size), True)
            else:
                chat_message("<font color='#%s' face='%s' size='%s'>You are currently running the latest version.</font>" % (font_color, font_face, font_size), True)
        # Command End            
        
        # Resplit the message body to determine "persona" usage.

        data = message.body.split(" ", 1)
        if len(data) > 1:
                cmd1, args1 = data[0], args # if command and args
        else:
                cmd1, args1  = data[0], ""# if command and no args
        # butterfly responce (8|8)
        if self.getAccess(user.name) >= lvl_config.rank_req_emote_bfly and cmd1 =="8|8":
            diff = datetime.datetime.now() - butterfly_timeout
            if diff.seconds >= 10:
                chat_message(random.choice(persona.butterfly))
                self.set_timeout("bfly")
                
        elif self.getAccess(user.name) >= lvl_config.rank_req_emote_fish and cmd1 == "><>":
            diff = datetime.datetime.now() - fishes_timeout
            if diff.seconds >= 10:
                chat_message(random.choice(persona.fishes))
                self.set_timeout("fish")
                
        elif self.getAccess(user.name) >= lvl_config.rank_req_say_brb and cmd1 == "brb":
                chat_message(random.choice(persona.brb))
