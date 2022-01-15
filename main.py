from machine import Pin, I2C
from axp192 import AXP192
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
pmu = AXP192(i2c)

while True:
    print("localtime       : {}".format(time.localtime()))
    print("battery level   : {}%".format(pmu.get_battery_level()))
    print("battery voltage : {}V".format(pmu.get_battery_voltage()))
    print("battery current : {}mA".format(pmu.get_battery_current()))
    print("battery power   : {}mW".format(pmu.get_battery_power()))
    print("battery charging current : {}mA".format(pmu.get_battery_charging_current()))
    print("vin voltage     : {}V".format(pmu.get_vin_voltage()))
    print("vin current     : {}mA".format(pmu.get_vin_current()))
    print("vbus voltage    : {}V".format(pmu.get_vbus_voltage()))
    print("vbus current    : {}mA".format(pmu.get_vbus_current()))
    print("aps voltage     : {}V".format(pmu.get_aps_voltage()))
    print("temperature     : {}C".format(pmu.get_temperature()))
    print("warning level   : {}".format(pmu.get_warning_level()))
    print("")
    time.sleep(2)
