# dfplayermini-pico
Micropython implementation of DFPlayerMini serial MP3 player from a Raspberry Pi Pico

## About

This library is used to control the DFPlayer MP3 player using a serial connection from a Raspberry Pi Pico

It is only a partial implementation, implementing common features. 

It is based on the protocol defined at (https://www.dfrobot.com/).

## Use

Upload the file dfplayermini.py to the root of a Raspberry Pi Pico with MicroPython. Run the example program pico-mp3-demo.py from thonny. It can be run automatically by renaming the file to main.py.

### Storing music / audio on an SD Card

The SD card should be formatted using FAT32 / VFAT. Create a directory called mp3 and name the music files using 4 digits for the track number. 
Eg. 0001.mp3

## Using in your own code

Upload the file dfplayermini.py to the Raspberry Pi Pico (you can use the upload functionality within the Thonny editor). Then import that to your own python file.

    from dfplayermini import DFPlayerMini
    
Create an instance of the DFPlayerMini class, providing the UART number (typically 0 or 1), followed by the trasmit pin number (eg. GP 4, for physical pin 5), and then the receive pin number (eg. GP 5 for physical pin 6).

    player1 = DFPlayerMini(1, 4, 5)
    
Issue a reset against the player (which you may need to attempt multiple times - typically 2 to 3 times).
    player1.reset()
    
The reset will return True when it has successfully reset the MP3 player.
    
You can then call any of the methods. For example set the volume to 12 (out of 30) using

    player1.set_volume(12)
    
Select the SD card using
    
    player1.select_source('sdcard')
    
Start playing a track using

    player1.play(track_number)

    
## Methods

### reset()

Reset the board ready to start communicating. Run this until it returns True.

### set_volume(volume_value)

Set the volume. volume_value can be between 0 (off) and 30 (max)

### volume_up() / volume_down()

Increase / decrease the volume

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


## More information

For more information see [Penguin Tutor project website Raspberry Pi Pico MP3 Player](https://www.penguintutor.com/projects/pico-mp3player)