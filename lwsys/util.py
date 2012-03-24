import os
import json
from Config import config

##
# find a file corresponding to a movie id
# perhaps use glob instead ??
# @param id input - the input id
# @return the name of the file found including full path
def get_infofile_name(id):
	infodir=config.LWMC_DB_DIR+"/info-%d"%(id/500)
	# list the directory /info-xxxx/ and look for a file
	# with the name nnnn-...txt
	for line in os.listdir(infodir):
		if line[-4:]!='.txt':
			continue
		if not line[0].isdigit():
			continue
		if int(line[0:6])==id:
			return infodir+"/"+line
	# if nothing is found return None
	return None

##
# produce a ping response string
def ping_response(request):
	return plain_string_json_response(request,"pong")

##
# produce a ping response string
def plain_string_json_response(request,resstring):
	# reqid is needed for all responses
	reqid=request["id"]
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":resstring
	}
	return json.dumps(response)

##
# produce a null result string
def resultnull(reqid):
	return '{"id":%d,"jsonrpc":"2.0","result":null}'%int(reqid)
