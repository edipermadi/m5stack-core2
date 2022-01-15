from machine import Pin, I2C
from axp192 import AXP192
import network
import time
import ntptime

# setup PMU
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
pmu = AXP192(i2c)
pmu.init()

# connect to wifi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'PASSWORD')
while not sta_if.isconnected():
    time.sleep_ms(100)

(ip_address, subnet, gateway, dns) = wlan.ifconfig()
print("ip-address: {}".format(ip_address))

# sync time
ntptime.settime()


