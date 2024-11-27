# Module for pico-mp3-web to validate requests
# For security reasons all files that the user may
# access must be listed in this file
import re
from dfplayermini import DFPlayerMini

class URL_Handler:
    
    static_files = {
        "index.html": "text/html",
        "jquery.min.js": "text/javascript",
        "picomp3play.js": "text/javascript",
        "picomp3play.css": "text/css"
        }
    
    def __init__(self, docroot):
        self.docroot = docroot
    
    # The read_request is used for dynamic requests
    # typically requested through jquery they return short codes or sections of text
    # static files are normally used for the main page
    # read command from request - look for configured commands
    # Returns tuple (even if single command) or None
    def read_request (self, request):
        # Split request into parts - eg. GET <filename> HTTPcode
        url_parts = request.split(" ", 2)
        # Check it's a GET request (don't use posts)
        if (url_parts[0] != "GET"):
            return None
        # Check it is http 1.x
        if (not url_parts[2].startswith("HTTP/1.")):
            return None
        # Check for a matching command
        if (url_parts[1][0:5] == "/play"):
            print (f"Play Command received: {url_parts[1]}")
            if url_parts[1][5:12] == "?track=":
                # Get after equals
                track_no = int(url_parts[1][12:])
                if isinstance(track_no, int) and track_no > 0 and track_no < 10000:
                    print (f"Play track {track_no}")
                    return ("play", track_no)
            # If track not provided or is not a valid integer return just play which = track 1
            return ("play",)
        elif (url_parts[1][0:6] == "/pause"):
            print (f"Pause command received: {url_parts[1]}")
            return ("pause",)
        elif (url_parts[1][0:5] == "/stop"):
            print (f"Stop command received: {url_parts[1]}")
            return ("stop",)
        elif (url_parts[1][0:9] == "/volumeup"):
            print (f"Volume up command received: {url_parts[1]}")
            return ("volumeup",)
        elif (url_parts[1][0:11] == "/volumedown"):
            print (f"Volume down command received: {url_parts[1]}")
            return ("volumedown",)
        # /volume can either be ?set= or ?query
        # Only check for ?set in which case set the volume, otherwise return value
        elif (url_parts[1][0:7] == "/volume"):
            if url_parts[1][7:12] == "?set=":
                # Get after equals
                vol_no = int(url_parts[1][12:])
                if isinstance(vol_no, int) and vol_no >= 0 and vol_no <= 30:
                    print (f"Set volume {vol_no}")
                    return ("volume", vol_no)
            return ("volume", )
        # Debug - note that this triggers even if it's a static file as we check that later
        
        return None
    
    # Is this a valid file?
    # If so return (200, filename, filetype)
    # If not return index.html (may change to 404 file in future)
    def validate_file (self, request):
        # Split request into parts - eg. GET <filename> HTTPcode
        url_parts = request.split(" ", 2)
        # Check it's a GET request (don't use posts)
        if (url_parts[0] != "GET"):
            return (400, "index.html", "text/html")
        # Check it is http 1.x
        if (not url_parts[2].startswith("HTTP/1.")):
            return (400, "index.html", "text/html")
        # Check first character is a /
        if (url_parts[1][0] != "/"):
            return (400, "index.html", "text/html")
        # Strip /
        req_filename = url_parts[1][1:]
        # If filename in list of allowed static files then return as a 200
        if req_filename in URL_Handler.static_files.keys():
            print ("Permitted file "+req_filename)
            return (200, req_filename, URL_Handler.static_files[req_filename])
        # Finally if no other file matches return the index.html file
        return (200, "index.html", "text/html")
        
        