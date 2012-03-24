import json

##
# List directory contents
# - currently returns empty
# !! TO DO
def GetDirectory(request):
	reqid=request["id"]
	thedir=request["params"]["directory"]
	media=request["params"]["media"]
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":{
			"limits":{ "start":0, "end":0, "total":0 }
		}
	}
	return json.dumps(response)

##
# List sources
# - currently returns 1 root directory
# TO DO
def GetSources(req):
	reqid=request["id"]
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":{
			"limits":{ "start":0, "end":1, "total":1 },
			"sources":[
				{ "file":"/","label":"root" }
			]
		}
	}
	return json.dumps(response)

