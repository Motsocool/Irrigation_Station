# Irrigation_Station1.2
Pico W Webpage controlling Lawn Irrigation used with a Pico Relay B from Waveshare.

Planning to make the toggles activate timers (1.3), add an overall toggle to start a squence of timers, make this webpage remotely accessible, 
add an lcd that displays the voltage, current zone watering, and the ip address of the pico w, 
and maybe an sms system for notifying if the lawn is over due for watering and if one zone has been on too long.

find me at tmntnpizza at reddit if you want to get into conact with me. please let me know if you see or create a code ethat may help me to complete this project!

#Irrigation Station1.3
Added an auto refresh for the http (currently every 7secs for testing). 
Added a timer function activated by the http toggle button (shuts off in 6secs for testing). 

Issues/discoveries: 
- I have many sets of my 8 relays each being listed and I'm sure there is a way to compress the code.

- The timer function currently shuts off all relays at 6secs from the first relay activation (not an issue for my setup).

- Http closes on OSerror when more then 4 of my 8 timer functions are applied to my code, whether or not they are being used.

- Have to recycle Pico power when the code is interrupted in any way before you can reconnect to the server.
