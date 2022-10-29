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

relays = []
for p in range(20, 14, -1):
    relays.append(Pin((p), Pin.OUT))
    
b_main_relay = Pin(21, Pin.OUT)
f_main_relay = Pin(14, Pin.OUT)

led_on_board = Pin("LED", Pin.OUT)
led_rgb = Pin(13, Pin.OUT)
buz = Pin(6, Pin.OUT)

timer = []
for t in range(0, 8, 1):
     timer.append(Timer())

def relays_all():
    relays_7()
    relays_1()
    sleep(sleep_msec)        #this sleep has to be set higher then the timer period, unless you want the relays on at staggered times.
    relays_2()
    sleep(sleep_msec)
    relays_3()
    sleep(sleep_msec)
    relays_4()
    sleep(sleep_msec)
    relays_8()
    relays_5()
    sleep(sleep_msec)
    relays_6()
    sleep(sleep_msec)
    print('Sprinkler Sequence Complete')

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

        #not my original work, but modified
    website = """<!DOCTYPE html>
    <html>
        <head> <title>Irrigation Station Raspberry Pico W</title> </head>
        <meta http-equiv="refresh" content="8">
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
                    <th><center>Off_Delay </center> </th>
                    <th><center>Pin State</center> </th>
                  </tr>
                  <tr>
                    <td><center>Zone_One </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_One")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_one"> </center></td>
                    <td> <center>  <span id="Zone_One">""" + str(relays[0].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Zone_Two </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_Two")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_two"> </center></td>
                    <td> <center>  <span id="Zone_Two">""" + str(relays[1].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Zone_Three </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_Three")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_three"> </center></td>
                    <td> <center>  <span id="Zone_Three">""" + str(relays[2].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Zone_Four </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_Four")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_four"> </center></td>
                    <td> <center>  <span id="Zone_Four">""" + str(relays[3].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Zone_Five </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_Five")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_five"> </center></td>
                    <td> <center>  <span id="Zone_Five">""" + str(relays[4].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Zone_Six </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Zone_Six")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_six"> </center></td>
                    <td> <center>  <span id="Zone_Six">""" + str(relays[5].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Backyard_Main </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Backyard_Main")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_seven"> </center></td>
                    <td> <center>  <span id="Backyard_Main">""" + str(b_main_relay.value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>Frontyard_Main </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Frontyard_Main")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_eight"> </center></td>
                    <td> <center>  <span id="Frontyard_Main">""" + str(f_main_relay.value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>all </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("all")'/> </center></td>
                    <td><center><input type='text' value="0" id="delay_all"> </center></td>
                    <td> <center>  <span id="All_Relays">""" + str(relays_all) + """</span></center> </td>
                  </tr>
            </table>
            
            
            <script>
                function toggleLed(led){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/led/'+led, true);
                    xhttp.send();
                }
                function toggleRelay(relays){
                    var delay = document.getElementById('delay_'+relays).value;
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('GET', '/relays/'+relays+'/'+delay, true);
                    xhttp.send();
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

        #not my original work
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

#WAN ipAddress = 142.165.122.98
ipAddress = status[0]
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

        #not my original work, but modified
while True:
    try:
        cl, addr = s.accept()
#        print('Connection from ', addr, "accepted!")
        request = cl.recv(1024)
        request = str(request)

        if request.find('/relays/') == 6:
            split_request=request.split()
            split2_request=split_request[1].split('/')
            print(split2_request[3])

            if request.find('/led/one') == 6:
                led_on_board.toggle()
                
            if request.find('/led/two') == 6:
                led_rgb.toggle()
            
            if request.find('/relays/one') == 6:
                relays_1()
                
            if request.find('/relays/two') == 6:
                relays_2()
                
            if request.find('/relays/three') == 6:
                relays_3()
                
            if request.find('/relays/four') == 6:
                relays_4()
            
            if request.find('/relays/five') == 6:
                relays_5()
                
            if request.find('/relays/six') == 6:
                relays_6()
                
            if request.find('/relays/seven') == 6:
                relays_7()
                
            if request.find('/relays/eight') == 6:
                relays_8()
                
            if request.find('/relays/all') == 6:
                relays_all()
            
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
        cb_relays_alloff()
        print("\nExiting application\n")
        machine.reset
        
def relays_1():
    relays[0].toggle()
    timer[0].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_oneoff)
    print('B_Zone 1 On')

def relays_2():
    relays[1].toggle()
    timer[1].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_twooff)
    print('B_Zone 2 On')
    
def relays_3():
    relays[2].toggle()
    timer[2].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_threeoff)
    print('B_Zone 3 On')
    
def relays_4():
    relays[3].toggle()
    timer[3].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_fouroff)
    print('B_Zone 4 On')
    
def relays_5():
    relays[4].toggle()
    timer[4].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_fiveoff)
    print('F_Zone 1 On')
    
def relays_6():
    relays[5].toggle()
    timer[5].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_sixoff)
    print('F_Zone 2 On')
    
def relays_7():
    b_main_relay.toggle()
    timer[6].init(period=b_main_on, mode=Timer.ONE_SHOT, callback=cb_relays_sevenoff)
    print('Backyard_Main On')
    
def relays_8():
    f_main_relay.toggle()
    timer[7].init(period=f_main_on, mode=Timer.ONE_SHOT, callback=cb_relays_eightoff)
    print('Frontyard_Main On')
    
def cb_relays_oneoff(Source):
    relays[0].value(0)
    print('Relay 1 off cb')
    
def cb_relays_twooff(Source):
    relays[1].value(0)
    print('Relay 2 off cb')
    
def cb_relays_threeoff(Source):
    relays[2].value(0)
    print('Relay 3 off cb')
    
def cb_relays_fouroff(Source):
    relays[3].value(0)
    print('Relay 4 off cb')
    
def cb_relays_fiveoff(Source):
    relays[4].value(0)
    print('Relay 5 off cb')
    
def cb_relays_sixoff(Source):
    relays[5].value(0)
    print('Relay 6 off cb')
    
def cb_relays_sevenoff(Source):
    b_main_relay.value(0)
    print('Backyard_Main Off cb')
    
def cb_relays_eightoff(Source):
    f_main_relay.value(0)
    print('Frontyard_Main Off cb')

water_on_time = int(split2_request[3])	#text request from http in Mins, not required just makes requests simpler.
timer_usec = water_on_time*60000		#zone timer period converted from Mins to Msecs, required for period function.
mains_on = timer_usec+10000				#Minimum timer period for each yard in Msecs, required for period function.
b_main_on = mains_on*4					#Maximum timer period for the backyard in Msecs, required for period function.
f_main_on = mains_on*2					#Maximum timer period for the frontyard in Msecs, required for period function.
water_pause = water_on_time+0.167		#requested time for watering plus 10secs pause between each zone in Mins.
sleep_msec = water_pause*60				#requested time for watering plus pause in Secs, required for sleep function.