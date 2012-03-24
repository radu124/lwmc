import json
from Config import config,files,paths

##
# movie sets not supported right now
def GetMovieSets(request):
	reqid=request["id"]
	props=GetPropsOrFields(request)
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":{
			"limits":{ "start":0, "end":0, "total":0 },
		}
	}
	return json.dumps(response)

##
# produce dummy movie set containing all movies if asked for
def GetMovieSetDetails(request):
	reqid=request["id"]
	props=GetPropsOrFields(request)
	response={
			"id":reqid,
			"jsonrpc":"2.0",
			"result":{
				"fanart":"special://fanart/11111.png" ,
				"thumbnail":"special://thumbnail/11111.png"
			}
		}
	response["items"]=GetMovieData(1,["label","movieid"])
	return json.dumps(response)

##
# Retrieve data for the list of movies
# @param idSet - currently ignored, restrict response to the given
#    movie set
# @param props - properties(fields) to be retrieved
# @result {
#   limits: start/end/total idicating size of movie list
#   movies: array of movie entries, each entry containing a dictionary of
#       prop:value pairs
#	}
# this is the format for GetMovies response
def GetMovieData(idSet,props):
	# only the start limit is set to 0, end and total will be set at
	# the end, after counting the movie entries
	result={
		"limits":{
			"start":0
		},
		"movies":[]
	}
	# traverse the list of files
	for idFile,(idPath,flags,idInfo,fname) in files.items():
		# ignore everything but movies
		if flags!='m':
			continue
		# each item is a dictionary of prop:value entries
		item=dict()
		for prop in props:
			value='unknown'
			# for now just produce a list of dummy values
			if prop=='file':
				value="/%d.avi"%idFile
			elif prop=='label':
				value=fname
			elif prop=='fanart':
				value="special://fanart/%d.jpg"%idInfo
			elif prop=='thumbnail':
				value="special://thumbnail/%d.jpg"%idInfo
			elif prop=='streamdetails':
				value={
					"audio": [ { "channels":2, "codec":"mp3", "language":"" } ],
					"video": [ { "aspect":1.33, "codec":"xvid", "duration":3600, "height":800, "width":600 } ]
					}
			elif prop=='imdbnumber':
				value="tt0000000"
			elif prop=='movieid':
				value=idFile
			elif prop=="mpaa":
				value="Rated PG-13"
			elif prop=='playcount':
				value=0
			elif prop=='rating':
				value=5
			elif prop=='runtime':
				value='60'
			elif prop=='year':
				value=2000
			elif prop=='set':
				value=[]
			elif prop=='trailer':
				value="plugin://plugin.video.youtube/?action=play_video&videoid=00000000000"
			item[prop]=value
		result["movies"].append(item)
	# assign end limits to the count of movies
	count=len(result["movies"])
	result["limits"]["end"]=count
	result["limits"]["total"]=count
	return result

##
# This field name seems to have changed in between protocol versions
# we support both
def GetPropsOrFields(request):
	params=request["params"]
	if "properties" in params:
		props=params["properties"]
	else:
		props=params["fields"]
	return props

##
# Produce a list of movies, essentially pack the list returned
# by GetMovieData into a jsonrpc response
def GetMovies(request):
	reqid=request["id"]
	props=GetPropsOrFields(request)
	print "props: ",props
	response={
			"id":reqid,
			"jsonrpc":"2.0",
			"result": GetMovieData(1,set(props) or [ "label" ])
		}
	return json.dumps(response)
