import json
import time

# memorize startup time so that we can report uptime
startuptime=time.time()

##
# return various system variables
# @param .id = the request id
#        .params {
#           <list of variables>
#           or labels:<list of variables>
#        }
# @return json output containing list of label:value pairs
def GetInfoLabels(request):
	print request # for debug purposes
	reqid=request["id"]
	params=request["params"]
	# in different protocol versions params
	# either contained the list directly or inside the "labels" member
	if isinstance(params, (list,tuple)):
		labels=params
	else:
		labels=params["labels"]
	# base response
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":dict()
	}
	# enumerate requested variables and give their value
	for label in labels:
		value=None
		# system uptime
		if label=='System.Uptime':
			uptime=int(time.time()-startuptime)
			# if uptime<1 Minute, report in seconds
			# otherwise in Minutes
			if uptime<60:
				value="%d Seconds"%uptime
			else:
				value="%d Minutes"%int(uptime/60)
		# warn if unknown variable is requested
		if value==None:
			print "WARN: GetInfoLabels: unknown variable - "+label
			value="0"
		response["result"][label]=value
	# serialize response as json
	return json.dumps(response)
