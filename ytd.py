#------------------importing modules-------------------#
import sys
import os
try:
	from bs4 import BeautifulSoup
	import requests
	import pafy
except:
	print "Did you installed required modules?"
	print "First install python-pip"
	print "Then use: 'pip install -r PATH_TO_req.txt'"
	sys.exit()
#-------------------------//---------------------------#

#----------------------color class------------------ --#
class color:
   CYAN = '\033[96m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   END = '\033[0m'
#-------------------------//---------------------------#

#giving options to arguments below
#------------------------------------------------------#
if len(sys.argv) == 3:
	path = sys.argv[2]   #path is the path on local machine where we have to store videos
	if path[-1] != "/":
		path = path + "/"
elif len(sys.argv) == 2:
	path = "./"
elif len(sys.argv) == 1:
	print "URL not Entered.\nEnter the valid url of playlist.\n" + color.RED + "exiting..." + color.END
	sys.exit()
else:
	print "Enter valid arguments.\n" + color.RED + "exiting..." + color.END
	sys.exit()
#-------------------------//---------------------------#

#initializing the variables and getting the data below
#------------------------------------------------------#
playlistUrl =  sys.argv[1]

r = requests.get(str(playlistUrl))
try:
	soup = BeautifulSoup(r.content, "lxml")
except:
	print "Have you installed lxml parser?"
	print "Try using 'sudo pip install lxml' or 'sudo apt-get install python-lxml'"
	sys.exit()
data = soup.find_all("table", {"class": "pl-video-table"})

playlist = pafy.get_playlist(playlistUrl)
videos = len(playlist["items"])
#-------------------------//---------------------------#

#code for adding a custom path for downloading the video
#------------------------------------------------------#
if not os.path.exists(path):
    os.mkdir(path)
else:
	print "Directory already exists and your contents will be mergerd."
	print color.BOLD + color.RED + "[*]Continue: y/n" + color.END
	inp = raw_input()
	if inp == "y" or inp == "Y":
		path = path
	elif inp == "n" or inp == "N":
		print "canceling..."
		sys.exit()
	else:
		print color.RED + "Invalid option selected. exiting..." + color.END
		sys.exit()
#-------------------------//---------------------------#

#creation of an file with all zeroes symbolising all videos are not downloaded and 1 in the file will indicate a downloaded video
#------------------------------------------------------#
with open(path + playlist['title']+' downloaded_videos_info.txt', 'a') as f:
	for i in range(1,videos + 1):
		f.write('0')
	f.close()
#-------------------------//---------------------------#

#getting urls of videos in the playlist
#------------------------------------------------------#
urls = []
print "Downloading the playlist " + color.CYAN + color.BOLD + str(playlist['title']) + color.END + " with " + color.CYAN + color.BOLD + str(videos) + color.END + " videos."
for item in data:
	links = item.find_all("a", {"dir": "ltr"})
	for link in links:
		vid_link = link.get("href")
		if vid_link[1] == "w":
			vid_file = "https://www.youtube.com" + vid_link
			urls.append(vid_file)
#-------------------------//---------------------------#

#storing the contents of the file in a local list so as not to read from file everytime
#------------------------------------------------------#
with open(path + playlist['title'] +' downloaded_videos_info.txt', 'r+') as f:
	true_false = f.readlines()
	f.close()	
i=1 #keeps track of printing order of string 'Video successfully downloaded'.
j=0 #keeps track of index in file reading and writing 
#-------------------------//---------------------------#

#code for downloading all videos or some specific range of videos and updating the file as videos get downloaded
#---------------------------------------------------------------------------------------------------------------#
print "Download all " + color.CYAN + color.BOLD + str(videos) + color.END + " videos or some specific videos:"
print color.BOLD + "[#]Press " + color.END + color.CYAN + color.BOLD + "a" + color.END + color.BOLD + " for all.\n[#]Press " + color.END + color.CYAN + color.BOLD + "s" + color.END + color.BOLD + " for some videos and enter i and j to download videos from index i to index j." + color.END
print color.BOLD + "[#]To download discrete videos, press " + color.END + color.CYAN + color.BOLD + "d" + color.END + color.BOLD + " and then enter indices of videos to be downloaded." + color.END

switch = "HIGH_IMPEDENCE" #to switch between {"a" or "s", switch is up} or {"d", switch is down}
#-------------------------//---------------------------#

#getting user input
#------------------------------------------------------#
usr_inp = raw_input()
down_vids_idx = []
if usr_inp == "a" or usr_inp == "A":
	switch = "up"
	idx1 = 1
	idx2 = videos + 1
elif usr_inp == "s" or usr_inp == "S":
	switch = "up"
	print "Enter appropriate integer index i"
	idx1 = int(raw_input())
	print "Enter appropriate integer index j"
	idx2 = int(raw_input())
elif usr_inp == "d" or usr_inp == "D":
	switch = "down"
	print "Enter valid number of videos to download:"
	num_vids = int(raw_input())
	for i in range(num_vids):
		print "Enter the valid integer index:"
		i = int(raw_input())
		down_vids_idx.append(i)
else:
	print color.RED + "Invalid Arguments. exiting..." + color.END
	sys.exit()	
#-------------------------//----------------------------#

#downloading the videos if usr_inp = "a" or "s"  below
#-------------------------------------------------------#
if switch == "up":
	if idx1>videos+1 or idx2>videos+1 or idx1>idx2 or idx1<0 or idx2<0:
		print color.RED + "Invalid Indexes. exiting..." + color.END
		sys.exit()
	elif idx1<=idx2:
		for j in range(idx1-1, idx2):
			try:
				if true_false[0][j]== "0":
					v = pafy.new(urls[j])
					s = v.getbest()
					size = str(int(s.get_filesize())/1000)
					print color.BLUE + color.BOLD + "Video #" + str(j+1) + ": " + color.END + color.YELLOW + v.title + color.END + " (Size: " + size + " Kb)"
					print color.GREEN + "Download Status" + color.END
					s.download(path)  # this starts the download
					print " " # necessary to see download status of the downloaded videos if nothing is appended after the download function is called the status of the latest videos will overwrite the status of the previous video because of the prewritten code of download function 
					true_false[0][j] == "1"
					print "Video successfully downloaded.\n"
					with open(path + playlist['title'] +' downloaded_videos_info.txt', 'r+') as f:
						f.seek(j)
						f.write("1")
				j=j+1
			except:
				print color.BLUE + color.BOLD + "\nVideo #" + str(j+1) + color.END + " download interrupted.\n"
		f.close()
	else:
		print color.RED + "Invalid Indexes. exiting..." + color.END
#-------------------------//---------------------------#

#downloading the videos if usr_inp = "d"   below
#------------------------------------------------------#
elif switch == "down":
	j_reducer = 0 # j_reducer will reduce the value of j by 1 so as to maintain correct sequence of videos to be downloaded as after an interrution j will increase by one
	while j < videos + 1:
		try:
			if j in down_vids_idx and true_false[0][j] == "0":
				if j_reducer == 1:
					j_reducer = 0
				v = pafy.new(urls[j-1])
				s = v.getbest()
				size = str(int(s.get_filesize())/1000)
				print color.BLUE + color.BOLD + "Video #" + str(j) + ": " + color.END + color.YELLOW + v.title + color.END + " (Size: " + size + " Kb)"
				print color.GREEN + "Download Status" + color.END
				s.download(path)  # this starts the download
				print " "
				true_false[0][j] == "1"
				print "Video successfully downloaded.\n"
				with open(path + playlist['title'] +' downloaded_videos_info.txt', 'r+') as f:
					f.seek(j)
					f.write("1")
			j=j+1
		except:
			print color.BLUE + color.BOLD + "\nVideo #" + str(j) + color.END + " download interrupted.\n"
			j=j+1  # here j is increased unlike case of above code of "a" or "s" because of nature of while loop which won't increment j unlike for loop
			j_reducer = 1
	f.close()
#-------------------------//---------------------------#