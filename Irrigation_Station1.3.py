import rp2
import network
import ubinascii
import machine
import urequests as requests
import socket
import utime
import time
from machine import Pin, Timer
from secrets import secrets
from picozero import pico_temp_sensor, pico_led
from utime import sleep
from time import sleep

#Create an empty array
relays = list()

#List comprehension to create an array of sequential pins
#Same as [14,15...21]
relayPins = [x for x  in range (14, 22)]
led_on_board = Pin("LED", Pin.OUT)
led_rgb = Pin(13, Pin.OUT)
buz = Pin(6, Pin.OUT)

#Initialise the pins
for x in relayPins:
    relays.append(Pin(x, Pin.OUT)
    
#change to your country code as applicable
rp2.country('CA')

#Device details
DEV_INFO_MANUFACTURER = "Waveshare"
DEV_INFO_MODEL        = "Pico Relay B"

#WiFi credentials
ssid = secrets["ssid"]
pw  = secrets["pw"]

def Website():
    led_one = led_on_board.value()
    led_two = led_rgb.value()
    
    website = """<!DOCTYPE html>
    <html>
        <head> <title>Irrigation Station Raspberry Pico W</title> </head>
        <body>
            <h1>Irrigation Station Raspberry Pico W</h1>
            <table style="width:400px" class="center">
                  <tr>
                    <th><center>LED Number </center></th>
                    <th><center>Button </center> </th>
                    <th><center>Pin State</center> </th>
                  </tr>
                  <tr>
                    <td><center>one </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("one")'/> </center></td>
                    <td> <center>  <span id="led_one">""" + str(led_one) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>two</center> </td>
                    <td><center><input type='button' value='toggle' onclick='toggleLed("two")'/></center></td>
                    <td><center>  <span id="led_two">""" + str(led_two) + """</span></center></td>
                   </tr>
                   <tr>
                    <th><center>Relay Number </center></th>
                    <th><center>Button </center> </th>
                    <th><center>Pin State</center> </th>
                  </tr>
                  <tr>
                    <td><center>one </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("one")'/> </center></td>
                    <td> <center>  <span id="relay_one">""" + str(relays[0].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>two </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("two")'/> </center></td>
                    <td> <center>  <span id="relay_two">""" + str(relays[1].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>three </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("three")'/> </center></td>
                    <td> <center>  <span id="relay_three">""" + str(relays[2].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>four </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("four")'/> </center></td>
                    <td> <center>  <span id="relay_four">""" + str(relays[3].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>five </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("five")'/> </center></td>
                    <td> <center>  <span id="relay_five">""" + str(relays[4].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>six </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("six")'/> </center></td>
                    <td> <center>  <span id="relay_six">""" + str(relays[5].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>seven </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Seven")'/> </center></td>
                    <td> <center>  <span id="relay_seven">""" + str(relays[6].value) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>eight </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("eight")'/> </center></td>
                    <td> <center>  <span id="relay_eight">""" + str(relays[7].value) + """</span></center> </td>
                  </tr>
            </table>
            
            <input type='button' value='update' onclick='update()'/>
            <meta http-equiv="refresh" content="7" />
                        
            <script>
                function toggleLed(led){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/led/'+led, true);
                    xhttp.send();
                    setTimeout(location.reload(true),3000);
                }
                function toggleRelay(relays){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/relays/'+relays, true);
                    xhttp.send();
                    setTimeout(location.reload(true),3000);
                }
                function update(){
                    location.reload(true);
                }
                    
            </script>
        </body>
    </html>
    """
    return website
    
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, pw)

# If you need to disable powersaving mode
wlan.config(pm = 0xa11140)

# See the MAC address in the wireless chip OTP
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print('mac = ' + mac)

# Other things to query
# print(wlan.config('channel'))
# print(wlan.config('essid'))
# print(wlan.config('txpower'))
    
# Wait for connection with 10 second timeout
timeout = 10
while timeout > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    timeout -= 1
    print('Waiting for connection...')
    time.sleep(1)
    
# Define blinking function for onboard LED to indicate error codes    
def blink_onboard_led(num_blinks):
    for i in range(num_blinks):
        led_on_board.on()
        time.sleep(.2)
        led_on_board.off()
        time.sleep(.2)
    
# Handle connection error
# Error meanings
# 0  Link Down
# 1  Link Join
# 2  Link NoIp
# 3  Link Up
# -1 Link Fail
# -2 Link NoNet
# -3 Link BadAuth

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError('Wi-Fi connection failed')
else:
    print('Connected')
    status = wlan.ifconfig()
    print('ip = ' + status[0])
    led_on_board.on()


#This can replace all of the above and allow you to turn them back on too
def SetRelayStatus(relay_number, status):
    relays[relay_number].value(status)
                      
                      
ipAddress = status[0]
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)
while True:
    try:
        cl, addr = s.accept()
        print('Connection from ', addr, "accepted!")
        request = cl.recv(1024)
        request = str(request)
        
        #Replace the callbacks with SetRelay
        relays_one_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=SetRelayStatus(0,0))
        relays_two_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=SetRelayStatus(1,0))
#        relays_three_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_threeoff)
#        relays_four_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_fouroff)
#        relays_five_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_fiveoff)
#        relays_six_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_sixoff)
#        relays_seven_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_sevenoff)
#        relays_eight_Timer = Timer(period=6000, mode=Timer.ONE_SHOT, callback=cb_relays_eightoff)

        if request.find('/led/one') == 6:
            led_on_board.toggle()
            
        if request.find('/led/two') == 6:
            led_rgb.toggle()
        
        #Not familiar enough with requests to suggest how it might be trimmed

        if request.find('/relays/one') == 6:
            relays[0].toggle()
            
        if request.find('/relays/two') == 6:
            relays[1].toggle()
            
        if request.find('/relays/three') == 6:
            relays[2].toggle()
            
        if request.find('/relays/four') == 6:
            relays[3].toggle()
        
        if request.find('/relays/five') == 6:
            relays[4].toggle()
            
        if request.find('/relays/six') == 6:
            relays[5].toggle()
            
        if request.find('/relays/seven') == 6:
            relays[6].toggle()
            
        if request.find('/relays/eight') == 6:
            relays[7].toggle()
            
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(Website())
        cl.close()
        
    except OSError as e:
        cl.close()
        print('Connection closed')
        
    except KeyboardInterrupt:
        # turn the relay off
        led_on_board.value(0)
        led_rgb.value(0)
        #Unsure if x will return the pin object or a number
        #for x in range(8) if it returns the object or change SetRelayStatus to be simply relay_number.value(status)
        for x in relays:
            SetRelayStatus(x, 0)
        print("\nExiting application\n")
        machine.reset
