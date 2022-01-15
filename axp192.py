import time

# ported from https://github.com/m5stack/M5Core2/blob/master/src/AXP192.cpp
class AXP192:
    def __init__(self, i2c):
        self.i2c = i2c

    def read(self, addr, length):
        return self.i2c.readfrom_mem(0x34, addr, length)
    
    def write(self, addr, values):
        self.i2c.writeto_mem(0x34, addr, values)
    
    def write_8bit(self, addr, *values):
        buff = bytearray(1)
        buff[0] = values[0]
        self.write(addr, buff)
        
    def read_8bit(self, addr):
        values = self.read(addr, 1)
        return values[0]
    
    def read_12bit(self, addr):
        values = self.read(addr, 2) 
        return (values[0] << 4) + values[1]
    
    def read_13bit(self, addr):
        values = self.read(addr, 2) 
        return (values[0] << 5) + values[1]
    
    def read_16bit(self, addr):
        values = self.read(addr, 2) 
        return (values[0] << 8) + values[1]
    
    def read_24bit(self, addr):
        values = self.read(addr, 3) 
        return (values[0] << 16) + (values[1] << 8) + values[2]
    
    def read_32bit(self, addr):
        values = self.read(addr, 4) 
        return (values[0] << 24) + (values[1] << 16) + (values[2] << 8) + values[3]
    
    def set_screen_brightness(self, brightness):
        if brightness < 1:
            return
        elif brightness > 12:
            brightness = 12
        
        self.write_8bit(0x28, (self.read_8bit(0x28) & 0x0f) | (brightness << 4))
    
    def get_battery_state(self):
        if self.read_8bit(0x01) & 0x20:
            return True
        else:
            return False
    
    def get_battery_power(self):
        return self.read_24bit(0x70) * 0.00055
        
    def set_dc_voltage(self, number, voltage):
        if number < 0 or number > 2:
            return
    
        if voltage < 700:
            voltage = 0
        else:
            voltage = (voltage - 700) // 25
        
        if number == 0:
            addr = 0x26
        elif number == 1:
            addr = 0x25
        else:
            addr = 0x27
        
        self.write_8bit(addr, (self.read_8bit(addr) & 0x80) | (voltage & 0x7f))
        
    def set_ldo_voltage(self, number, voltage):
        if number < 2 or number > 3:
            return
        
        if voltage > 3300:
            voltage = 15
        else:
            voltage = (voltage // 100) - 18
        
        value = self.read_8bit(0x28)
        
        if number == 2:
            self.write_8bit(0x28, (value & 0x0f) | (voltage << 4))
        else:
            self.write_8bit(0x28, (value & 0xf0) | voltage)
    
    def set_ldo_enable(self, number, state):
        if number < 2 or number > 3:
            return
        
        self.toggle_register_bit(0x12, (0x01 << number), state)
    
    def set_dcdc3(self, state):
        self.toggle_register_bit(0x12, 0x02, state)
        
    def set_esp_voltage(self, voltage):
        if voltage >= 3000 and voltage <= 3400:
            self.set_dc_voltage(0, voltage)
    
    def set_lcd_voltage(self, voltage):
        if (voltage >= 2500 and voltage <= 3300):
            self.set_dc_voltage(2, voltage)
    
    def set_led(self, state):
        self.toggle_register_bit(0x94, 0x02, state)
    
    def set_charging_current(self, current):
        options = (100, 190, 280, 360, 450, 550, 630, 700, 780, 880, 960, 1000, 1080, 1160, 1240, 1320)
        if current not in options:
            return
        
        value = self.read_8bit(0x33)
        value = (value & 0xf0) | (options.index(current) & 0x0f )
        self.write_8bit(0x33, value)
    
    def toggle_register_bit(self, addr, mask, state):
        value = self.read_8bit(addr)

        if state:
            value |= mask
        else:
            value &= ~mask
    
        self.write_8bit(addr, value)
        
    def set_lcd_reset(self, state):
        self.toggle_register_bit(0x96, 0x02, state)
    
    def set_bus_power_mode(self, state):
        if state:
            self.write_8bit(0x12, self.read_8bit(0x12) & 0xbf)
            self.write_8bit(0x90, (self.read_8bit(0x90) & 0xf8) | 0x01)
        else:
            self.write_8bit(0x91, (self.read_8bit(0x91) & 0x0f) | 0Xf0)
            self.write_8bit(0x90, (self.read_8bit(0x90) & 0xf8) | 0x02)
            self.read_8bit(0x91);
            self.write_8bit(0x12, self.read_8bit(0x12) | 0x40)

    def get_battery_voltage(self):
        return self.read_12bit(0x78) * 0.0011
    
    def get_battery_current(self):
        current_in = self.read_13bit(0x7a)
        current_out = self.read_13bit(0x7c)
        return (current_in - current_out) * 0.5
    
    def get_vin_voltage(self):
        return self.read_12bit(0x56) * 0.0017
    
    def get_vin_current(self):
        return self.read_12bit(0x58) * 0.625
    
    def get_vbus_voltage(self):
        return self.read_12bit(0x5a) * 0.0017
    
    def get_vbus_current(self):
        return self.read_12bit(0x5c) * 0.375

    def set_speaker_enable(self, state):
        self.toggle_register_bit(0x94, 0x04, state)
    
    def get_input_state(self):
        return self.read_8bit(0x00)
        
    def is_vbus(self):
        if self.get_input_state() & 0x20:
            return True
        else:
            return False
    
    def is_charging(self):
        if self.get_input_state() & 0x04:
            return True
        else:
            return False
    
    def is_acin(self):
        if self.get_input_state() & 0x80:
            return True
        else:
            return False
    
    def set_coloumb_clear(self, state):
        self.write_8bit(0xb8, 0x20)
    
    def get_battery_coloumb_in(self):
        return self.read_32bit(0xb0) * 0.3640888888888889
    
    def get_battery_coloumb_out(self):
        return self.read_32bit(0xb4) * 0.3640888888888889
    
    def get_battery_charging_current(self):
        return self.read_12bit(0x7a) * 0.5
    
    def get_aps_voltage(self):
        return self.read_12bit(0x7e) * 0.0014
    
    def poweroff(self):
        self.write_8bit(0x32, self.read_8bit(0x32) | 0x80);
    
    def set_adc_state(self, state):
        if state:
            value = 0xff
        else:
            value = 0x00
            
        self.write_8bit(0x82, value)
    
    def prepare_to_sleep(self):
        self.set_adc_state(False)
        self.set_led(False)
        self.set_dcdc3(False)
    
    def restore_from_light_sleep(self):
        self.set_dcdc3(True)
        self.set_led(True)
        self.set_adc_state(True)
    
    def get_warning_level(self):
        return self.read_8bit(0x47) & 0x01        
    
    def get_battery_level(self):
        voltage = self.get_battery_voltage()
        if voltage <  3.248088:
            percentage = 0
        else:
            percentage = (voltage - 3.120712) * 100;
        
        if percentage > 100:
            percentage = 100
        return percentage
    
    def get_temperature(self):
        return (self.read_12bit(0x5e) * 0.1) - 144.7
        
    def init(self):
        self.write_8bit(0x30, (self.read_8bit(0x30) & 0x04) | 0x02)
        self.write_8bit(0x92, self.read_8bit(0x92) & 0xf8)
        self.write_8bit(0x93, self.read_8bit(0x93) & 0xf8)
        self.write_8bit(0x35, (self.read_8bit(0x35) & 0x1c) | 0xa2)
        self.set_esp_voltage(3350)
        self.set_lcd_voltage(2800)
        self.set_ldo_voltage(2, 3300)
        self.set_ldo_voltage(3, 2000)
        self.set_ldo_enable(2, True)
        self.set_dcdc3(True)
        self.set_led(True)
        self.set_charging_current(100)
        self.write_8bit(0x95, (self.read_8bit(0x95) & 0x72) | 0x84)
        self.write_8bit(0x36, 0x4c)
        self.write_8bit(0x82, 0xff)
        
        self.set_lcd_reset(False)
        time.sleep_ms(100)
        self.set_lcd_reset(True)
        
        if self.read_8bit(0x00) & 0x08:
            self.write_8bit(0x30, self.read_8bit(0x30) | 0x80)
            self.set_bus_power_mode(True)
        else:
            self.set_bus_power_mode(False)
