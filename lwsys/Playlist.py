import json
from threading import Semaphore

# the playlist, a list of strings of the form "/idPath/idFile"
playlist=[]
# semaphore for protecting playlist access
playlistSem=Semaphore()

##
# Clear the playlist
def Clear(request):
	reqid=request["id"]
	# work on global variables
	global playlist
	global playlistSem
	# protect playlist access with semaphore
	acquire(playlistSem)
	playlist=[]
	release(playlistSem)
	# plain response
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":"OK"
	}
	return json.dumps(response)

##
# Add an item to the playlist
def Add(request):
	reqid=request["id"]
	params=request["params"]
	# work on global variables
	global playlist
	global playlistSem
	# protect playlist access with semaphore
	acquire(playlistSem)
	theplaylist.append(params['item']['file'])
	release(playlistSem)
	print 'playlist: ',theplaylist # debug
	# plain response
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":"OK"
	}
	return json.dumps(response)

