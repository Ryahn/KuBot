#
# Includes
#
from urllib.request import urlopen
import re

#
# Exceptions
#
class YoutubeException(Exception): pass

#
# Regex
#
def tag_regex_construct(tag): 
	return re.compile(r"<%s ?[^>]*>(.*?)</%s>" %(tag, tag), re.IGNORECASE | re.DOTALL )

title_re = tag_regex_construct("title")
desc_re  = tag_regex_construct("content")
auth_re  = tag_regex_construct("name")

#
# Video class
#
class Video: 
	def __init__(self, vid, update = True): 
		self.vid = vid 
		if(update): self.update() 
	
	def update(self):
		resp = urlopen(self.get_api_link()) 
		if(resp):
			data = resp.read().decode() 
			self.title = title_re.search(data).group(1)
			try:
				self.desc = desc_re.search(data).group(1)
			except:
				self.desc = "No description avaiable."
			self.auth = auth_re.search(data).group(1) 
		else:
			raise YoutubeException("video id seems invalid")

	def get_api_link(self): 
		return "http://gdata.youtube.com/feeds/api/videos/%s" %(self.vid)
		
	def get_id(self): 
		return self.vid 
		
	def get_title(self): 
		return self.title 

	def get_desc(self): 
		return self.desc

	def get_auth(self): 
		return self.auth