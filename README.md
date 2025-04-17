# dfplayermini-pico
Micropython implementation of DFPlayerMini serial MP3 player from a Raspberry Pi Pico

## About

This contains a library used to control the DFPlayer MP3 player using a serial connection from a Raspberry Pi Pico. It also includes example source code for a web based MP3 player using a Pico W.

It is only a partial implementation, implementing common features. 

It is based on the protocol defined at (https://www.dfrobot.com/).

# Library usage

Upload the file dfplayermini.py to the root of a Raspberry Pi Pico with MicroPython. Run the example program pico-mp3-demo.py from thonny. It can be run automatically by renaming the file to main.py.

### Storing music / audio on an SD Card

The SD card should be formatted using FAT32 / VFAT. Create a directory called mp3 and name the music files using 4 digits for the track number. 
Eg. 0001.mp3

The order that the mp3 files are placed on the SD card will affect the order that the music is played.

## Using in your own code

Upload the file dfplayermini.py to the Raspberry Pi Pico (you can use the upload functionality within the Thonny editor). Then import that to your own python file.

    from dfplayermini import DFPlayerMini
    
Create an instance of the DFPlayerMini class, providing the UART number (typically 0 or 1), followed by the trasmit pin number (eg. GP 4, for physical pin 5), and then the receive pin number (eg. GP 5 for physical pin 6).

    player1 = DFPlayerMini(1, 4, 5)
    
Issue a reset against the player.
    player1.reset()
    
The reset will return True when it has successfully reset the MP3 player. The next command should be to select the source.
    
Select the SD card using
    
    player1.select_source('sdcard')


You can then call any of the methods. For example set the volume to 12 (out of 30) using

    player1.set_volume(12)
    
    
Start playing a track using

    player1.play(track_number)

    
## Methods

### reset()

Reset the board ready to start communicating. 

### set_volume(volume_value)

Set the volume. volume_value can be between 0 (off) and 30 (max)

### volume_up() / volume_down()

Increase / decrease the volume

### get_volume() 

Get the current volume, returns a value 0 to 30 or False if an error occured

### select_source(source_name)

Choose the source fo the audio.
Actual sources depend upon the type of player.
Eg. 'usb', 'sdcard', 'aux', 'flash'

### stop()

Stops playing the track

### play(track_number)

Play a specific track number

### play_next() / player_previous()

Play the next, or previous track

### play_loop(track_number)

Player the specified track number in a loop

### pause()

Pauses the play (resume using start)

### start()

Plays the current track (eg. resume after a pause)


### query_num_files(<source>)

Query the number of files on the source.
If source is not supplied then current selected source is used.



## WiFi version

The repository also includes an example web server designed for the Raspberry Pi Pico. 

# Installation

This version needs to be installed on a Raspberry Pi Pico W with the appropriate network enabled MicroPython. MicroPython can be installed through the Thonny editor.

To install the program, copy all the files in the source to the top-level of the Raspberry Pi Pico, also upload the entire public directory. For the network connection you also need to create a file called secrets.py with details of your SSID and PASSWORD. The example below shows the formatting for the secrets.py file.

    SSID="NetworkSSID"
    PASSWORD="WiFiPassword"
    
## Configuration

The program can be run in two modes. 

* Access Point Mode (AP mode) - In this mode the Pico will act as a Wireless Access Point which you can connect to using another WiFi enabled device.
* Client Mode - In this mode you can connect to an existing wireless network

Note that in client mode it is currently blocking and will not operate until it has successfully connected to the network.

The mode is set by editing the entry "mode" in the pico-lights.py file. 

mode="ap"       # Use as an access point
mode="client"   # Use as a Wi-Fi client

    
## Running on startup

For the code to run automatically on start-up save the pico-mp3-demo.py file on your Pico as main.py.



## More information

For more information see [Penguin Tutor project website Raspberry Pi Pico MP3 Player](https://www.penguintutor.com/projects/pico-mp3player)

For technical details of the DFPlayer Mini see the [DFPlayer Wiki](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299)