# A web server implemention of the Pico MP3 Player
# based around DFRobot DFPlayerMini
# For more details see:
# https://www.penguintutor.com/projects/pico-mp3player

import network
import socket
import uasyncio as asyncio
import secrets
import re
from utime import sleep
from url_handler import URL_Handler
from dfplayermini import DFPlayerMini


# Mode can be ap (access point where the Pico acts as a web server)
# or "client" [default] which connects to an existing network
# Note that client mode is blocking and will not run the rest of the code
# until a network connection is established
mode="client"

# All documents in DocumentRoot are publically accessible
DocumentRoot = "public/"

# If ip_config not blank then use for network config
# otherwise set to "" to use dhcp
ip_config = ("192.168.0.55", "255.255.255.0", "192.168.0.1", "8.8.8.8")

# Tuple with uart number, tx gp number and receive gp no
uart_details = (1, 4, 5)

player1 = DFPlayerMini(*uart_details)
player1.select_source('sdcard')

# Special dynamic files - these are edited in real time by replacing {arg} with the value provided
# All these must have a corresponding value in url_handler
# Can either be "" (leaves as a number) or list to replace
dynamic_svg_files = {
    'audio-vol.svg' : "",
    'audio-track.svg' : ["0", "1 - voice", "2 - voice", "3 - music"]
    }

url = URL_Handler(DocumentRoot)
      
# Connect to wireless network - either AP or client mode      
def connect():
    #Connect to WLAN
    # Should allow access via hostname.local, but may depend on WiFi network
    network.hostname ("mp3player")
    if mode== "ap":
        # Access Point mode
        ip = connect_ap_mode()
    else:
        ip = connect_client_mode()
    return ip
    
def connect_ap_mode ():
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=secrets.SSID, password=secrets.PASSWORD)
    wlan.active(True)
    while wlan.active() == False:
        print ('Trying to setup AP mode')
    ip = wlan.ifconfig()[0]
    print('AP Mode is active')
    print('Connect to Wireless Network '+secrets.SSID)
    print('Connect to IP address '+ip)
    print('Hostname '+network.hostname())
    return ip

def connect_client_mode ():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power saving mode
    if ip_config != "":
        wlan.ifconfig(ip_config)
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    wlan.config(hostname = "mp3player")
    ip = wlan.ifconfig()[0]
    print('Connect to IP address '+ip)
    print('Hostname '+network.hostname())
    return ip


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = request_line.decode("utf-8")
    
    # Determine if it's command, dynamic image or static
    url_request_info  = url.request_type(request)
    
    if url_request_info[0] == "command":
        command = url_request_info[1]
        arg = url_request_info[2]
        
        status_message = 'Status ...'
        if command != None:
            if command == "play":
                #print (f"Play command {command}")
                # Check for parameter = track number
                if arg != "" and isinstance(arg, int) and arg > 0 and arg < 10000:
                    player1.play(arg)
                    status_message = f'Playing {arg}'
                else:
                    # special case if no arg supplied and paused then call start instead
                    if player1.paused:
                        player1.start()
                        status_message = f'Resume playing'
                    else:
                        player1.play(1)
                        status_message = f'Playing 1'
            elif command == "pause":
                player1.pause()
                status_message = f'Pause'
            elif command == "stop":
                player1.stop()
                status_message = f'Stop'
            elif command == "volumeup":
                player1.volume_up()
                status_message = f'{str(player1.get_volume())}'
            elif command == "volumedown":
                player1.volume_down()
                status_message = f'{str(player1.get_volume())}'
            elif command == "volume":
                if arg != "" and isinstance(arg, int) and arg >= 0 and arg <= 30:
                    player1.set_volume(arg)
                # Regardless of whether we change volume return current volume
                status_message = f'{str(player1.get_volume())}'
            elif command == "numfiles":
                num_files = player1.query_num_files()
                #print (f"Returning numfiles {num_files}")
                status_message = f'{str(num_files)}'
            # Return status - currently just text 
            writer.write('HTTP/1.0 200 OK\r\nContent-type: text/text\r\n\r\n')
            writer.write(status_message)
        
    # Handle special dynamic files related to volume or track name
    elif url_request_info[0] == "dynamic":
        url_filename = url_request_info[1]
        url_arg = url_request_info[2]
        print (f"Dynamic file {url_filename} - {url_arg}")
        # First validate value and/or convert to a string
        if dynamic_svg_files[url_filename] == "" or len(dynamic_svg_files[url_filename]) <  (url_arg+1):
            arg_string = str(url_arg)
        else:
            arg_string = dynamic_svg_files[url_filename][url_arg]
        # Load file and read - replacing {arg} as neccessary
        writer.write('HTTP/1.0 200 OK\r\nContent-type: image/svg+xml\r\n\r\n')
        # Use readline to prevent {arg} being split over lines
        with open(DocumentRoot+url_filename, "r") as read_file:
            data = read_file.readline(1024)
            while data:
                new_string = data.replace("{arg}", arg_string)
                writer.write(new_string)
                await writer.drain()
                data = read_file.readline(1024)
            read_file.close()
            
    else:
        # Else it could be "static" or "error" - handle same
        url_value = url_request_info[1]
        url_file = url_request_info[2]
        url_type = url_request_info[3]
        # Otherwise must be static
        writer.write('HTTP/1.0 {} OK\r\nContent-type: {}\r\n\r\n'.format(url_value, url_type))
        # Send file 1kB at a time (avoid problem with large files exceeding available memory)
        with open(DocumentRoot+url_file, "rb") as read_file:
            data = read_file.read(1024)
            while data:
                writer.write(data)
                await writer.drain()
                data = read_file.read(1024)
            read_file.close()

    await writer.wait_closed()
    #print("Client disconnected")


# Initialise Wifi
async def main ():
    print ("Connecting to network")
    try:
        ip = connect()
    except KeyboardInterrupt:
        machine.reset
    print ("IP address", ip)
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    print ("Web server listening on", ip)
    while True:
        #onboard.on()
        # Enable following line for heartbeat debug messages
        #print ("heartbeat")
        await asyncio.sleep(0.25)
    



if __name__ == '__main__':
    try:
        asyncio.run(main())
    finally:
        asyncio.new_event_loop()
        
