# Module for pico-mp3-web to validate requests
# For security reasons all files that the user may
# access must be listed in this file
import re
from dfplayermini import DFPlayerMini

class URL_Handler:
    
    # Default home page - must also be in static files to determine file type
    home_page = "index.html"
    
    # All static files needs to be registered here
    # Also need to include file type http string
    # For SVG must be svg+xml, otherwise prevented due to security
    static_files = {
        "index.html": "text/html",
        "jquery.min.js": "text/javascript",
        "picomp3play.js": "text/javascript",
        "picomp3play.css": "text/css",
        "audio-vol-inc.svg": "image/svg+xml",
        "audio-vol-dec.svg": "image/svg+xml",
        "audio-play.svg": "image/svg+xml",
        "audio-stop.svg": "image/svg+xml",
        "audio-pause.svg": "image/svg+xml"
        }
    
    # commands has two parts, the command and an optional single parameter which can be int
    # does not support multiple parameters
    # If not parameter then that is empty
    # only validate value type, does not check valid value as not always known
    commands = {
        "play": "?track=",
        "pause": "",
        "stop": "",
        "volumeup": "",
        "volumedown": "",
        "volume": "?set="
        }
    
    # Dynamically generated svg files
    # String is filename plus 3 digit number
    # Filename must follow shortname, then x.svg
    # This is used for security checking only, if special naming
    # is required then that is handled in main program
    dynamic_svg_files = [
        "audio-vol-",
        "audio-track-"
        ]
    
    def __init__(self, docroot):
        self.docroot = docroot
    
    
    # First pre-check for valid format of the request
    # Performs initial checks common to all request types
    # If successful returns Tuple with True, filename
    # If not then returns False followed by defaut error (False, 400, filename, type)
    # If not return index.html (may change to 404 file in future)
    def pre_check (self, request):
        # Split request into parts - eg. GET <filename> HTTPcode
        url_parts = request.split(" ", 2)
        # Check it's a GET request (don't use posts)
        if (url_parts[0] != "GET"):
            return (False, 400, "index.html", "text/html")
        # Check it is http 1.x
        if (not url_parts[2].startswith("HTTP/1.")):
            return (False, 400, "index.html", "text/html")
        # Check first character is a /
        if (url_parts[1][0] != "/"):
            return (False, 400, "index.html", "text/html")
        # Strip /
        # req_filename still includes any parameters
        req_filename = url_parts[1][1:]
        return (True, 0, req_filename)
    
    # Return the type of reqest  
    def request_type (self, request):
        # First perform pre-check
        check_value = self.pre_check(request)
        if check_value[0] == False:
            return ("error", check_value[1], check_value[2], check_value[3])
        req_filename = check_value[2]
        # Is it a static file?
        check_static = self.validate_static_file(req_filename)
        if check_static[0] == True:
            return ("static", 200, check_static[1], check_static[2])
        # check if it's a dynamic file - ie. generated as a image etc.
        check_dynamic = self.validate_dynamic_file (req_filename)
        if check_dynamic[0] == True:
            return ("dynamic", check_dynamic[1], check_dynamic[2])
        # Finally check if it's a command
        check_command = self.validate_command (req_filename)
        if check_command[0] == True:
            return ("command", check_command[1], check_command[2])
        return ("static", 400, "index.html", "text/html")

    # Check for a valid static file
    # If so return (True, 200, filename, filetype)
    # Otherwise return (False, 0, filename)
    # Check to see if this is a static file
    def validate_static_file (self, req_filename):
        # / has already been stripped
        # If it's just / then return index.html
        if req_filename == "":
            req_filename = self.home_page
        # If filename in list of allowed static files then return as a 200
        if req_filename in URL_Handler.static_files.keys():
            print ("Permitted file "+req_filename)
            return (True, req_filename, URL_Handler.static_files[req_filename])
        # Finally if no other file matches returns False (need to check if dynamic if not error)
        return (False, req_filename)
        
    # Some files can be dynamically generated, just check prefix and do more security checks later (eg. checking valid extension)
    def validate_dynamic_file (self, req_filename):
        for this_prefix in self.dynamic_svg_files:
            if req_filename.startswith(this_prefix):
                return (True, req_filename, this_prefix)
        # Reach here it's not been found
        return (False, req_filename)
    
    # Check for a command
    # Typically these are requested via jquery and then retun short code or string
    # Look in commands to see if it's valid
    # If valid returns (True, command, parameter) or parameter "" if no parameter
    # # Otherwise return (False, req_string)
    def validate_command (self, req_string):
        print (f"Command {req_string}")
        # Check for a matching command
        for this_command in self.commands.keys():
            # Checks either for a complete match or for a match followed by ?
            if req_string == this_command or req_string.startswith(this_command+'?'):
                print (f"Command is {this_command}")
                # If no params then just return and ignore rest of request
                if self.commands[this_command] == "":
                    return (True, this_command, "")
                # If here then look to see if there are parameters
                # Strip off the command
                remaining_string = req_string[len(this_command):]
                print (f"Remaining string {remaining_string}")
                # Now check if we have that string if not then return just the command
                if not remaining_string.startswith(self.commands[this_command]):
                    return (True, this_command, "")
                # Now strip that and check we have a number left
                number_string = remaining_string[len(self.commands[this_command]):]
                print (f"Track no string {number_string}")
                # should just have a number now
                try:
                    number = int (number_string)
                except ValueError:
                    return (True, this_command, "")
                else:
                    print (f"Track no {int(number_string)}")
                    return (True, this_command, int(number_string))

        # Otherwise return False
        return (False, req_string)

   
    
    # Todo implement dynamic svg numbering
    def validate_dynamic_svg (self, request):
        return False
    
    

        
        