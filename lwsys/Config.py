import os

class config:
	USER_HOME_DIR=os.getenv("HOME")
	LWMC_DB_DIR=USER_HOME_DIR+"/.config/lwmc/userdata"
	VIDEO_FILE_LIST=LWMC_DB_DIR+"/files.txt"
	PATHS_FILE_LIST=LWMC_DB_DIR+"/paths.txt"

# dictionary of video files indexed
# key = numeric file id
#  value[0] = path id
#  value[1] = flags (m=movie)
#  value[2] = info id - id of the info entry
#  value[3] = filename
files=dict()
# read files list - space delimited fields fifth field may contain spaces
for line in open(config.VIDEO_FILE_LIST):
	thefile=line.split(None,4)
	if len(thefile)<5:
		continue
	files[int(thefile[0])]=(int(thefile[1]),thefile[2],int(thefile[3]),thefile[4])

# dictionary of folders
# key = numeric folder id
#  value[0] = flags
#  value[1] = path
paths=dict()
# read paths list - space delimited fields
for line in open(config.PATHS_FILE_LIST):
	thepath=line.split(None,2)
	if len(thepath)<3:
		continue
	paths[int(thepath[0])]=(thepath[1],thepath[2])
