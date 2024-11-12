from dfplayermini import DFPlayerMini
import time

player1 = DFPlayerMini(1, 4, 5)
#data = b'\x7E\xFF\x06\x09\x00\x00\x04\xFF\xDD\xEF'
#print (f"{data}")
data = {
    'reset' : b'\x7E\xFF\x06\x0C\x01\x00\x00\xFE\xEE\xEF',
    'setvolume' : b'\x7E\xFF\x06\x06\x01\x00\x0A\xFE\xEA\xEF',
    'sdcard' : b'\x7E\xFF\x06\x09\x01\x00\x02\xFE\xEF\xEF',
    'play1' : b'\x7E\xFF\x06\x03\x01\x00\x01\xFE\xF6\xEF',
    'play2' : b'\x7E\xFF\x06\x03\x01\x00\x02\xFE\xF5\xEF'
    }

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