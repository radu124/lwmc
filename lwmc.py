#!/usr/bin/python

import SocketServer
import json
import os

from lwsys import VideoLibrary
from lwsys import XBMC
from lwsys import Files
from lwsys import Player
from lwsys import Playlist
from lwsys import Server
from lwsys import System
from lwsys.util import *

# log file for debug purposes
logf=open('lwmc.log','w')

##
# serve a json request
# forward the request to the appropriate handler
# if no handler is available for this request, return an error message
def serverequest(req):
	method=req['method']
	reqid=req['id']
	res=''
	if method=='JSONRPC.Ping':
		res=ping_response(req)
	elif method=='VideoLibrary.GetTVShows':
		res=VideoLibrary.GetTVShows(req)
	elif method=='VideoLibrary.GetMovieSets':
		res=VideoLibrary.GetMovieSets(req)
	elif method=='VideoLibrary.GetMovieSetDetails':
		res=VideoLibrary.GetMovieSetDetails(req)
	elif method=='AudioLibrary.GetArtists':
		res=resultnull(reqid)
	elif method=='AudioLibrary.GetAlbums':
		res=resultnull(reqid)
	elif method=="System.GetInfoLabels" or method=="XBMC.GetInfoLabels":
		res=XBMC.GetInfoLabels(req)
	elif method=="VideoLibrary.GetMovies":
		res=VideoLibrary.GetMovies(req)
	elif method=="Files.GetSources":
		res=Files.GetSources(req)
	elif method=="Files.GetDirectory":
		res=Files.GetDirectory(req)
	elif method=="Player.Open":
		res=Player.Open(req)
	elif method=="Playlist.Clear":
		res=Playlist.Clear(req)
	elif method=="Playlist.Add":
		res=Playlist.Add(req)
	elif method=="System.Shutdown":
		res=System.Shutdown(req)
	else:
		print "Unknown method: ",method,req
		res='{"error":{"code":-32601,"message":"Method not found."},"id":%d,"jsonrpc":"2.0"}'%reqid
	# if the request was served, but it returned an empty result
	if res=='':
		print "Method %s returned an empty result."%method
		res=resultnull(reqid)
	return res

##
# Serve dirrect command send using the old HTTP interface
# it serves several sub-commands
#    SetVolume
#    PlayerControl
#    SendKey
def servedirectcommand(line):
	print "direct command: ",line # debug
	cmdpos=line.find("ExecBuiltIn");
	# if the command string does not contain the expected keyword
	# silently ignore
	if cmdpos==-1:
		return ''
	cmd=line[cmdpos+12:]
	print "command: ",cmd # debug
	# look for known commands
	if cmd[0:9]=='SetVolume':
		Player.dcSetVolume(cmd[10:])
	if cmd[0:13]=='PlayerControl':
		Player.dcPlayerControl(cmd[14:].split(')')[0])
	if cmd[0:7]=='SendKey':
		Player.dcSendKey(cmd[8:].split(')')[0])
	return ''

##
# Container of the TCP handler callback function
class MyTCPHandler(SocketServer.StreamRequestHandler):
	##
	# TCP handler callback function
	def handle(self):
		# we will need the content length to know
		# how much we should read from the stream
		contentlength=0
		# the server should be able to serve multiple request types
		#    JSONRPC commands, with the POST method
		#    old style HTTP commands using the GET method
		#    files (TO DO)
		# note that the entire response is buffered in a string
		directcommand=''
		authorized=False
		# iterate thorugh headers
		while True:
			line=self.rfile.readline().strip()
			logf.write(line)
			logf.write("\n")
			# an empty line indicates the end of the header
			if line=='':
				break
			# if the command is a GET remember the line
			if line[0:4]=='GET ':
				directcommand=line
			# split header line at the :
			hdrline=line.split(':',2)
			# remember content length
			if hdrline[0]=='Content-Length':
				contentlength=int(hdrline[1])
			# if authorization is encountered, check against stored hash
			if hdrline[0]=='Authorization':
				if hdrline[1]!=' Basic '+config.PASSWD_HASH:
					# invalid credentials will result in an automatic
					# disconnect
					print "Authorization failed : "+hdrline[1]
					return
				authorized=True
		# not presenting any credential results in an automatic
		# disconnect
		if not authorized:
			print "Not authorized"
			return
		# serve a direct command rather than the JSONRPC-style commands
		if directcommand!='':
			res=servedirectcommand(directcommand)
		else:
			# serve JSONRPC commands
			line=self.rfile.read(contentlength)
			logf.write(line)
			logf.write("\n")
			req=json.loads(line)
			# it turns out that multiple requests may be bundled as a
			# a single list, in this case serve them separately
			if isinstance(req, (list, tuple)):
				print "ARRAY"
				res='['
				for rr in req:
					if res!='[':
						res+=','
					# forward individual commands to serverequest
					# and concatenate the results
					res+=serverequest(rr)
				res+=']'
			else:
				# forward the single command to serverequest
				res=serverequest(req)
		# write log
		logf.write("=== RESULT FOLLOWS ===\n")
		logf.write(json.dumps(json.loads(res),False,True,True,True,json.JSONEncoder,4))
		logf.write("\n======== DONE ========\n")
		logf.write("\n\n")
		# write HTTP response
		self.wfile.write("HTTP/1.1 200 OK\n")
		self.wfile.write("Content-Type: application/json\n")
		self.wfile.write("Content-Length: %d\n"%len(res))
		self.wfile.write("\n")
		self.wfile.write(res)
		# self.request.sendall(self.data.upper())

# if this is called as main - which should be the case
# start the server
if __name__ == "__main__":
	# use a slightly nonstandard port
	HOST, PORT = "", 8083
	# Create the server, binding to localhost on port 9999
	Server.server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
	# Activate the server; this will keep running until you
	# interrupt the program with Ctrl-C
	Server.server.serve_forever()
