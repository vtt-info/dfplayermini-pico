# A library to control the DFPlayer MP3 player
# Only partial implementation
# For more details of protocol see https://www.dfrobot.com/
# Created by Stewart Watkiss @PenguinTutor
# https://www.penguintutor.com 


from machine import UART, Pin
import time

class DFPlayerMini ():
    
    sources = {
        'usb': 1,
        'sdcard': 2,
        'sd': 2, 		# Allow sd as well as sd card
        'aux': 3,
        'sleep': 4,
        'flash': 5
        }
    
    def __init__ (self, uart_no, tx, rx):
        self.uart = UART(uart_no, baudrate=9600, tx=Pin(tx), rx=Pin(rx))
        self.uart.init(9600, bits=8, parity=None, stop=1)
        
    # Send a byte string (bytes should alread be fully encoded)
    def send_bytes (self, byte_string):
        sent_count = self.uart.write(byte_string)
        time.sleep(0.5)
        read_value = self.uart.read(10)
        return read_value
    
    def calc_checksum(self, data):
        # Data string
        sum = 0
        for byte in data:
            sum += byte
        #Convert to twos complement
        twos = (0xFFFF + 1 - sum)
        return twos
    
    def send_command (self, command, value=0, feedback=1):
        # Start = 7E
        # Version = FF
        # Len = 06
        # cmd
        # feedback = 1 or 0 (Whether response required) typically 1 for yes
        # para 1 (high data byte)
        # para 2 (low data byte)
        # checksum (from Version to para2) - 2 bytes
        # End = EF
        
        # Data without start, end or checksum
        data = b'\xFF\x06' + command.to_bytes(1) + feedback.to_bytes(1) + value.to_bytes(2)
        # Add checksum to data
        checksum = self.calc_checksum(data)
        data += checksum.to_bytes(2)
        # Add start and end bytes
        data_string = b'\x7E' + data + b'\xEF'
        #print (f"Sending: {data_string}")
        return self.send_bytes (data_string)
    
    def reset(self):
        #'reset' : b'\x7E\xFF\x06\x0C\x01\x00\x00\xFE\xEE\xEF'
        return_value = self.send_command(0x0C)
        #print (f"Return: {return_value}")
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        # Now check for a valid return value - lower data byte = [6]
        # 0 = Timeout
        if return_value[6] == 0:
            return False
        # 2 = Cardinserted, 4 = CardOnline, 7 = USBInserted, 9 = USBOnline, 10 = CardUSBOnline
        if return_value[6] in (0x02, 0x04, 0x07, 0x09, 0x10):
            return True
        # Any other value return False
        return False


    def set_volume(self, volume):
        # eg.  b'\x7E\xFF\x06\x06\x01\x00\x0A\xFE\xEA\xEF' (10)
        return_value = self.send_command(0x06, volume)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
    
    def volume_up(self, volume):
        return_value = self.send_command(0x04)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True

    def volume_down(self, volume):
        return_value = self.send_command(0x05)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True


    # select source of audio - eg. "usb", "sdcard", "aux", "sleep", "flash"
    def select_source(self, source):
        #'sdcard' : b'\x7E\xFF\x06\x09\x01\x00\x02\xFE\xEF\xEF'
        return_value = self.send_command(0x09, self.sources[source])
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True

    def stop(self):
        return_value = self.send_command(0x16)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
    
    def play (self, track_num):
        #'play1' : b'\x7E\xFF\x06\x03\x01\x00\x01\xFE\xF6\xEF',
        return_value = self.send_command(0x03, track_num)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
    
    def play_next (self):
        return_value = self.send_command(0x01)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
    
    def play_previous (self):
        return_value = self.send_command(0x02)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True

    def play_loop (self, track_num):
        return_value = self.send_command(0x08, track_num)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True

    def pause (self):
        return_value = self.send_command(0x0E)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
    
    def start (self):
        return_value = self.send_command(0x0D)
        # Check for no return value or length of value is not correct
        if return_value == None or len(return_value) != 10:
            # If so just return without checking for a value
            return False
        return True
