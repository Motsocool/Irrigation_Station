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
for p in range(21, 13, -1):
    relays.append(Pin((p), Pin.OUT))

led_on_board = Pin("LED", Pin.OUT)
led_rgb = Pin(13, Pin.OUT)
buz = Pin(6, Pin.OUT)

timer = []
for t in range(0, 8, 1):
     timer.append(Timer())

def relays_1():
    relays[0].toggle()
    timer[0].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_oneoff)
    print('Relay 1 on')

def relays_2():
    relays[1].toggle()
    timer[1].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_twooff)
    print('Relay 2 on')
    
def relays_3():
    relays[2].toggle()
    timer[2].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_threeoff)
    print('Relay 3 on')
    
def relays_4():
    relays[3].toggle()
    timer[3].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_fouroff)
    print('Relay 4 on')
    
def relays_5():
    relays[4].toggle()
    timer[4].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_fiveoff)
    print('Relay 5 on')
    
def relays_6():
    relays[5].toggle()
    timer[5].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_sixoff)
    print('Relay 6 on')
    
def relays_7():
    relays[6].toggle()
    timer[6].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_sevenoff)
    print('Relay 7 on')
    
def relays_8():
    relays[7].toggle()
    timer[7].init(period=timer_usec, mode=Timer.ONE_SHOT, callback=cb_relays_eightoff)
    print('Relay 8 on')
    
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
    relays[6].value(0)
    print('Relay 7 off cb')
    
def cb_relays_eightoff(Source):
    relays[7].value(0)
    print('Relay 8 off cb')
    
def cb_relays_alloff(Source):
    relays[0].value(0)
    relays[1].value(0)
    relays[2].value(0)
    relays[3].value(0)
    relays[4].value(0)
    relays[5].value(0)
    relays[6].value(0)
    relays[7].value(0)
    print('All Relays Are Off')
    
water_on_time = 0 #In mins with the convertion. 60000*desired mins = the value water_on_time needs to be.
timer_usec = water_on_time*60000 #timer function requires microsecs and I convert them to mins. 900000usecs = 15mins
water_pause = water_on_time+0.167 #In mins with the convertion. 60*desired mins = the value water_pause needs to be.
sleep_msec = water_pause*60 #sleep function requires millisecs and I convert them to mins. 900msecs = 15mins

def water_on_time():
    if request.method == 'POST':
        water_on_time = request.form['water_on_time']
        print(water_on_time)

def relays_all():
    relays_1()
    sleep(sleep_msec)        #this sleep has to be set higher then the timer period, unless you want the relays on at staggered times.
    relays_2()
    sleep(sleep_msec)
    relays_3()
    sleep(sleep_msec)
    relays_4()
    sleep(sleep_msec)
    relays_5()
    sleep(sleep_msec)
    relays_6()
    sleep(sleep_msec)
    relays_7()
    sleep(sleep_msec)
    relays_8()
    sleep(10)

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
                    <td> <center>  <span id="relay_one">""" + str(relays[0].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>two </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("two")'/> </center></td>
                    <td> <center>  <span id="relay_two">""" + str(relays[1].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>three </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("three")'/> </center></td>
                    <td> <center>  <span id="relay_three">""" + str(relays[2].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>four </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("four")'/> </center></td>
                    <td> <center>  <span id="relay_four">""" + str(relays[3].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>five </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("five")'/> </center></td>
                    <td> <center>  <span id="relay_five">""" + str(relays[4].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>six </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("six")'/> </center></td>
                    <td> <center>  <span id="relay_six">""" + str(relays[5].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>seven </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("Seven")'/> </center></td>
                    <td> <center>  <span id="relay_seven">""" + str(relays[6].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>eight </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("eight")'/> </center></td>
                    <td> <center>  <span id="relay_eight">""" + str(relays[7].value()) + """</span></center> </td>
                  </tr>
                  <tr>
                    <td><center>all </td>
                    <td><center><input type='button' value='toggle' onclick='toggleRelay("all")'/> </center></td>
                    <td> <center>  <span id="All_Relays">""" + str(relays_all) + """</span></center> </td>
                  </tr>
            </table>
            
            <input type='button' value='update' onclick='update()'/>
            <meta http-equiv="refresh" content="7" />
            
            <form action="" method="POST">
                <label> Water Timer </label>
                <input type="text" name="water_on_time" value=0>
    
                <button type="submit"> Submit
            </button>
            </form>           
            
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
                function changeTime(time){
                    var xhttp = new XMLHttpRequest();
                    xhttp.open('POST', '/time/'+time, true);
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
