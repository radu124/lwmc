import json
from threading import Thread
from threading import Semaphore

import VideoLibrary
from Playlist import playlist,playlistSem
from util import *

# whether the player thread is running
playerstarted=False
# force jumping to another position in the playlist after finishing
# playing current file, if negative playback will continue with the
# next playlist entry
playlistreentry=-1


##
# thread that is in charge or advancing through the playlist and
# launching the external
def player_thread_func():
	global playerstarted
	global theplaylist
	global playlistreentry
	global playlistSem
	i=0
	# iterate through the playlist we prefer while true for better
	# control over the order of iteration and access to playlist
	while True:
		try:
			# remove commands file
			os.system('rm mplayercmdfifo; touch mplayercmdfifo')
		except:
			print 'some problem creating comm fifo'
		# protect using semaphore
		acquire(playlistSem)
		# check whether we should skip to another playlist position
		if playlistreentry>=0:
			i=playlistreentry
			playlistreentry=-1
		# check whether end of playlist is reached
		if i>=len(playlist):
			# we should not make sure we exit the thread exactly
			# when we are doing a (re)Open
			playerstarted=False
			# do not forget to release sempahore
			release(playlistSem)
			break
		toplay=playlist[i].split('/')
		release(playlistSem)
		i+=1
		# check whether the path and file id exist
		if not ((toplay[2] in paths) or (toplay[1] in files)):
			# not found, just skip
			continue
		# translate to real file name
		toplayfn=paths[toplay[2]][2]+files[toplay[1]][3]
		# try to run player
		try:
			# tricky, may be dependent on shell
			# a commands file is continuously tailed to mplayer,
			# commands accumulate here but it will be reset
			# next time anyway
			os.system('tail -f mplayercmdfifo | ( QQ=$$; mplayer -slave -fs "'+toplayfn+'" ; kill $QQ ) | while read A; do echo "$A" >mplayerstatus.temp; mv -f mplayerstatus.temp mplayerstatus; done')
		except:
			print 'error running mplayer'
		print 'mplayer exited'
	# finished playlist, can exit thread
	print "finished playlist: ",playlist # debug

##
# Start player, or, if necessary restart
def Open(request):
	params=request["params"]
	global playerstarted
	global playerthread
	global playlistreentry
	# we don't modify the playlist
	# but to make sure we don't exit the playback thread at the exact
	# same time we are modifying the playlistreentry we lock the
	# semaphore here
	acquire(playlistSem)
	if playerstarted:
		# the player is already started
		print "player already busy" # debug
		playlistreentry=0
		# we can now release the semaphore
		release(playlistSem)
		dcControl('Stop')
		# respond Busy, whether it makes a difference or not
		return plain_string_json_response(request,"Busy")
	else:
		# release the semaphore on the other branch as well
		release(playlistSem)

	# start playback thread
	playerstarted=True
	playerthread=Thread(target=player_thread_func,args=())
	playerthread.start()
	# respond OK
	return plain_string_json_response(request,"OK")

##
# handle direct command: player control
# contains a list of sub-commands: Stop, Play
#    SmallSkipForward, SmallSkipBackward
#
# the command is passed to mplayer through a file tailed
# to its standard input (plain unix fifo had some trouble, though
# it could have been an option as well)
def dcControl(par):
	print "playercontrol: ",par
	if par=='Stop':
		os.system('echo "quit" >>mplayercmdfifo')
	if par=='Play':
		os.system('echo "pause" >>mplayercmdfifo')
	if par=='SmallSkipForward':
		os.system('echo "seek +15 0" >>mplayercmdfifo')
	if par=='SmallSkipBackward':
		os.system('echo "seek -15 0" >>mplayercmdfifo')

##
# handle SetVolume direct command
# @param par the volume level, on a scale to 100
def dcSetVolume(par):
	pars=par.split(')')
	print "Set volume: ",pars[0]
	os.system('echo "volume %d 1" >>mplayercmdfifo'%int(pars[0]))

##
# send a key command
# - currently does nothing
# TO DO
def dcSendKey(par):
	print "sendkey: ",int(par)
