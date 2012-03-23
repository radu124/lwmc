import json
from lwmcConfig import config

files=dict()
# read files list
for line in open(config.VIDEO_FILE_LIST):
	thefile=line.split(None,4)
	if len(thefile)<5:
		continue
	files[int(thefile[0])]=(int(thefile[1]),thefile[2],int(thefile[3]),thefile[4])


def GetMovieSets(request):
	reqid=request["id"]
	props=GetPropsOrFields(request)
	response={
		"id":reqid,
		"jsonrpc":"2.0",
		"result":{
			"limits":{ "start":0, "end":1, "total":1 },
			"sets": [
				{
					"fanart":"special://fanart/11111.png" ,
					"label":"all",
					"setid":1,
					"thumbnail":"special://thumbnail/11111.png" ,
				}
			]
		}
	}
	return json.dumps(response)

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

def GetMovieData(idSet,props):
	result={
		"limits":{
			"start":0
		},
		"movies":[]
	}
	for idFile,(idPath,flags,idInfo,fname) in files.items():
		if flags!='m':
			continue
		item=dict()
		for prop in props:
			propvalue='unknown'
			if prop=='file':
				propvalue="/%d.avi"%idFile
			elif prop=='label':
				propvalue=fname
			elif prop=='fanart':
				propvalue="special://fanart/%d.jpg"%idInfo
			elif prop=='thumbnail':
				propvalue="special://thumbnail/%d.jpg"%idInfo
			elif prop=='streamdetails':
				propvalue={
					"audio": [ { "channels":2, "codec":"mp3", "language":"" } ],
					"video": [ { "aspect":1.33, "codec":"xvid", "duration":3600, "height":800, "width":600 } ]
					}
			elif prop=='imdbnumber':
				propvalue="tt0000000"
			elif prop=='movieid':
				propvalue=idFile
			elif prop=="mpaa":
				propvalue="Rated PG-13"
			elif prop=='playcount':
				propvalue=0
			elif prop=='rating':
				propvalue=5
			elif prop=='runtime':
				propvalue='60'
			elif prop=='year':
				propvalue=2000
			elif prop=='set':
				propvalue=["all"]
			elif prop=='trailer':
				propvalue="plugin://plugin.video.youtube/?action=play_video&videoid=00000000000"
			item[prop]=propvalue
		result["movies"].append(item)
	count=len(result["movies"])
	result["limits"]["end"]=count
	result["limits"]["total"]=count
	return result

##
# Sudden change in protocol?
def GetPropsOrFields(request):
	params=request["params"]
	if "properties" in params:
		props=params["properties"]
	else:
		props=params["fields"]
	return props

def GetMovies(request):
	reqid=request["id"]
	props=GetPropsOrFields(request)
	print "props: ",props
	response={
			"id":reqid,
			"jsonrpc":"2.0",
			"result": GetMovieData(1,props)
		}
	return json.dumps(response)
