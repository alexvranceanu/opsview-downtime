import sys
import argparse, getpass
import urllib, urllib2
import json

#Define global verbose variable
verbose=False

def getLoginToken(s,u,p):
    opsview_server=s
    opsview_user=u
    opsview_password=p
    global verbose
    
    #Create authentication headers
    auth_headers = {
        "Content-Type": "application/json"
    }
    
    #Create authentication JSON
    auth_request = json.dumps({
        "username": opsview_user,
        "password": opsview_password
    })
    
    if verbose:
        print ("\nAuth JSON request:\n%s\n" % auth_request)
        print ("\nAuthenticating...\n")
    
    #Connect
    try:
        ops_cookies = urllib2.HTTPCookieProcessor()
        ops_opener = urllib2.build_opener(ops_cookies)
        opsview = ops_opener.open(urllib2.Request(opsview_server + "/rest/login", auth_request, auth_headers))
    #Exit if there is a problem authenticating
    except urllib2.URLError, e:
        print("Error: %s: %s" % (e.code, e.read()))
        sys.exit()
    
    #Read response
    opsview_response = opsview.read()
    response = eval(opsview_response)
    
    if not response:
        print("Unexpected message from Opsview server: %s" % response_text)
        sys.exit()

    #Grab the token from the response
    if "token" in response:
        opsview_token = response["token"]
    else:
        print("Opsview authentication failed with: %s" % response_text)
        sys.exit()

    return token

#Schedule downtime function
def scheduleDowntime(s,u,token,h,starttime,endtime,c):
    opsview_server=s
    opsview_user=u
    opsview_token=token
    opsview_host=h
    opsview_endtime=endtime
    opsview_comment=c
    global verbose
    
    #Create header request
    downtime_headers = {
        "Content-Type": "application/json",
        "X-Opsview-Username": opsview_user,
        "X-Opsview-Token": opsview_token,
    }
    
    #Create JSON request
    downtime_request = json.dumps({
        "starttime":opsview_starttime,
        "endtime":opsview_endtime,
        "comment":opsview_comment
    })
    
    if verbose:
        print("\nDowntime headers:\n%s\n" % downtime_headers)
        print("\nDowntime JSON request:\n%s\n" % downtime_request)
        print("\nScheduling downtime...\n")
    
    #Create the URL request object
    opsview_request = urllib2.Request(opsview_server + "/rest/downtime?host=" + opsview_host, downtime_request, downtime_headers)
    
    #Connect
    try:
        opsview_cookies = urllib2.HTTPCookieProcessor()
        opsview_opener = urllib2.build_opener(opsview_cookies)
        opsview = opsview_opener.open(opeview_request)
    #Fail if connection error
    except urllib2.URLError, e:
        print("Could not schedule downtime for %s: %s: %s" % (opsview_host,e.code,e.read()))
    
    print "Downtime request result:"
    print opsview.read()

def main():
    #Initiate argument parser
    parser = argparse.ArgumentParser(description='Opsview Downtime Tool')

    #Define standard options
    parser.add_argument('-u', '--user', nargs=1, action='store', dest='user', help='Opsview username', required=True, metavar='OpsviewUser')
    parser.add_argument('-p', '--password', nargs=1, action='store', dest='password', help='Opsview password', required=False, metavar='OpsviewPassword')
    parser.add_argument('-s', '--server', nargs=1, action='store', dest='server', help='Opsview server', default='https://localhost', required=False, metavar='OpsviewServer')
    parser.add_argument('-c', '--comment', nargs=1, action='store', dest='comment', help='Downtime comment', default='Scheduled downtime.', required=False, metavar='DowntimeComment')
    parser.add_argument('-t', '--starttime', nargs=1, action='store', dest='starttime', help='When to start the downtime. Default: now', default='now', required=False, metavar='DowntimeStartTime')
    parser.add_argument('-T', '--endtime', nargs=1, action='store', dest='endtime', help='How much downtime (eg. +30m, +1h). Default: +2h', default='+2h', required=False, metavar='DowntimeEndTime')
    parser.add_argument('-v', '--verbose', action='store_true', help="Print more messages", default=False, required=False)
    
    #Define exclusive options (either -o or -f, cannot be used together)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-o', '--opsviewhost', nargs=1, action='store', dest='opsviewhost', help='Host to schedule downtime for (the name of the host in Opsview)', required=False, metavar='Host')
    group.add_argument('-f', '--file', nargs=1, action='store', dest='file', help='File to read hosts from', required=False, metavar="InputFile")

    #Parse arguments
    args = parser.parse_args()
    
    #Read user password if not specified in arguments
    if not args.password:
        args.password = getpass.getpass()
        while not args.password:
            args.password = getpass.getpass()
    
    #TODO
    if args.file:
        print "This functionality is not yet implemented."
        return 0;
    
    #Print verbose
    if args.verbose:
        global verbose
        verbose=True
    
    if verbose:
        print("\nServer: %s\nUsername: %s\nHost: %s\nPassword: %s" % (args.server[0],args.user[0],args.opsviewhost[0],str(args.password)))
    
    #Get login token from Opsview
    token = getLoginToken(args.server[0],args.user[0],str(args.password))
    if verbose:
        print("Token: %s" % token)
        
    #Schedule downtime for host
    scheduleDowntime(args.server[0],args.user[0],token,args.opsviewhost[0],args.starttime[0],args.endtime[0],args.comment[0])

if __name__ == "__main__":
    main()


