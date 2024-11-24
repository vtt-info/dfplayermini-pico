# Demonstration program for the Raspberry Pi Pico MP3 Player
# based around DFRobot DFPlayerMini
# More details see:
# https://www.penguintutor.com/projects/pico-mp3player

from dfplayermini import DFPlayerMini
import time

player1 = DFPlayerMini(1, 4, 5)

# Loop until reset successful
while True:
    print ("Reset")
    if player1.reset() == True:
        break

print ("Set Volume 12")
read_value = player1.set_volume(12)

print ("Set SD Card")
read_value = player1.select_source('sdcard')

print ("Play 01")
read_value = player1.play(1)

time.sleep(10)

print ("Play 02")
read_value = player1.play(2)

time.sleep(10)

print ("Play Next")
read_value = player1.play_next()

time.sleep(5)

print ("Pause")
read_value = player1.pause()

time.sleep(2)

print ("Resume")
read_value = player1.start()

time.sleep(5)

print ("Stop")
read_value = player1.stop()