import json
import Server

from threading import Thread

##
# Shutdown the server
# FIX !! this still does not work
def Shutdown(request):
	reqid=request["id"]
	# must call this in a separate thread, otherwise we get a deadlock
	# because the shutdown function blocks
	Thread(target=shutdown_thread_func,args=())
	# produce response
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":"OK"
	}
	return json.dumps(response)

##
# simply call the shutdown function for the server
def shutdown_thread_func():
	Server.server.shutdown()
