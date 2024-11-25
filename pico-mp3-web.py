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
ip_config = ("192.168.0.54", "255.255.255.0", "192.168.0.1", "8.8.8.8")

# Tuple with uart number, tx gp number and receive gp no
uart_details = (1, 4, 5)

player1 = DFPlayerMini(*uart_details)


url = URL_Handler(DocumentRoot)

      
# Connect to wireless network - either AP or client mode      
def connect():
    #Connect to WLAN
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
    ip = wlan.ifconfig()[0]
    print('Connect to IP address '+ip)    
    return ip


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    request = request_line.decode("utf-8")
    
    # Dynamic command - returns None if not a recognised command
    # returns a tuple - first entry is string for command
    # subsequent entries (optional) are any parameters
    command = url.read_request(request)
    if command != None:
        if command[0] == "play":
            print (f"Play command {command}")
            # Check for parameter = track number
            if len(command) > 1 and isinstance(command[1], int) and command[1] > 0 and command[1] < 10000:
                player1.play(command[1])
            else:
                player1.play(1)
        elif command[0] == "pause":
            player1.pause()
        elif command[0] == "stop":
            player1.stop()
        elif command[0] == "volumeup":
            player1.volume_down()
        elif command[0] == "volumedown":
            player1.volume_down()
        # Return status - currently just text (will change to JSON)
        writer.write('HTTP/1.0 200 OK\r\nContent-type: text/text\r\n\r\n')
        writer.write('Status ...')
        
    
    # Otherwise if not a command is this a static file request
    else:
        
        url_value, url_file, url_type = url.validate_file(request)

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
    print("Client disconnected")


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
        
