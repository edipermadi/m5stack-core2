import time

DEVICE_ADDRESS    = const(0x34)
REG_POWER_STATUS  = const(0x00)
REG_POWER_MODE    = const(0x01)
REG_OUTPUT_CONTROL_1 = const(0x10)
REG_OUTPUT_CONTROL_2 = const(0x12)
REG_DC_TO_DC2_OUTPUT_VOLTAGE          = const(0x23)
REG_DC_TO_DC2_DYNAMIC_VOLTAGE_CONTROL = const(0x25)
REG_DC_TO_DC1_OUTPUT_VOLTAGE          = const(0x26)
REG_DC_TO_DC3_OUTPUT_VOLTAGE          = const(0x27)
REG_LDO2_LDO3_OUTPUT_VOLTAGE          = const(0x28)
REG_IRQ_ENABLE_1 = const(0x40)
REG_IRQ_ENABLE_2 = const(0x41)
REG_IRQ_ENABLE_3 = const(0x42)
REG_IRQ_ENABLE_4 = const(0x43)
REG_IRQ_STATUS_1 = const(0x44)
REG_IRQ_STATUS_2 = const(0x45)
REG_IRQ_STATUS_3 = const(0x46)

# ported from https://github.com/m5stack/M5Core2/blob/master/src/AXP192.cpp
class AXP192:
    def __init__(self, i2c):
        self.__i2c = i2c

    def __read(self, addr, length):
        return self.__i2c.readfrom_mem(DEVICE_ADDRESS, addr, length)
    
    def __write(self, addr, values):
        self.__i2c.writeto_mem(DEVICE_ADDRESS, addr, values)
    
    def __write_8bit(self, addr, *values):
        buff = bytearray(1)
        buff[0] = values[0]
        self.__write(addr, buff)
        
    def __read_8bit(self, addr):
        values = self.__read(addr, 1)
        return values[0]
    
    def __read_12bit(self, addr):
        values = self.__read(addr, 2) 
        return (values[0] << 4) + values[1]
    
    def __read_13bit(self, addr):
        values = self.__read(addr, 2) 
        return (values[0] << 5) + values[1]
    
    def __read_16bit(self, addr):
        values = self.__read(addr, 2) 
        return (values[0] << 8) + values[1]
    
    def __read_24bit(self, addr):
        values = self.__read(addr, 3) 
        return (values[0] << 16) + (values[1] << 8) + values[2]
    
    def __read_32bit(self, addr):
        values = self.__read(addr, 4) 
        return (values[0] << 24) + (values[1] << 16) + (values[2] << 8) + values[3]
    
    def __read_bit(self, addr, bit):
        return (self.__read_8bit(addr) & (1 << bit)) > 0
    
    def __set_bit(self, addr, bit_num, bit_val):
        value = self.__read_8bit(addr)
        if bit_val:
            value |= (1 << bit_num)
        else:
            value &= ~(1 << bit_num)
        self.__write_8bit(addr, value)
    
    @property
    def is_acin_present(self):
        return self.__read_bit(REG_POWER_STATUS, 7)
    
    @property
    def is_acin_valid(self):
        return self.__read_bit(REG_POWER_STATUS, 6)
    
    @property
    def is_vbus_present(self):
        return self.__read_bit(REG_POWER_STATUS, 5)
    
    @property
    def is_vbus_valid(self):
        return self.__read_bit(REG_POWER_STATUS, 4)
    
    @property
    def is_vbus_above_vhold(self):
        return self.__read_bit(REG_POWER_STATUS, 3)
    
    @property
    def is_battery_charging(self):
        return self.__read_bit(REG_POWER_STATUS, 2)
    
    @property
    def is_acin_or_vbus_shorted(self):
        return self.__read_bit(REG_POWER_STATUS, 1)
    
    @property
    def is_boot_triggered_by_acin_or_vbus(self):
        return self.__read_bit(REG_POWER_STATUS, 0)
    
    @property
    def is_over_temperature(self):
        return self.__read_bit(REG_POWER_MODE, 7)
    
    @property
    def is_charging_in_progress(self):
        return self.__read_bit(REG_POWER_MODE, 6)
    
    @property
    def is_battery_present(self):
        return self.__read_bit(REG_POWER_MODE, 5)
    
    @property
    def is_battery_active(self):
        return self.__read_bit(REG_POWER_MODE, 3)
    
    @property
    def is_undercurrent_charging(self):
        return self.__read_bit(REG_POWER_MODE, 2)

    @property
    def exten_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_1, 2)
    
    @exten_enable.setter
    def exten_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_1, 2, value)
        
    @property
    def dc_to_dc2_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_1, 0)
    
    @dc_to_dc2_enable.setter
    def dc_to_dc2_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_1, 0, value)
    
    @property
    def ldo3_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_2, 3)
    
    @ldo3_enable.setter
    def ldo3_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_2, 3, value)
    
    @property
    def ldo2_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_2, 2)
    
    @ldo2_enable.setter
    def ldo2_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_2, 2, value)
        
    @property
    def dc_to_dc3_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_2, 1)
    
    @dc_to_dc3_enable.setter
    def dc_to_dc3_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_2, 1, value)
    
    @property
    def dc_to_dc1_enable(self):
        return self.__read_bit(REG_OUTPUT_CONTROL_2, 0)
    
    @dc_to_dc1_enable.setter
    def dc_to_dc1_enable_setter(self, value):
        self.__set_bit(REG_OUTPUT_CONTROL_2, 0, value)
    
    @property
    def dc_to_dc2_voltage(self):
        return ((self.__read_8bit(REG_DC_TO_DC2_OUTPUT_VOLTAGE) & 0x3f) * 0.025) + 0.7
    
    @dc_to_dc2_voltage.setter
    def dc_to_dc2_voltage_setter(self, voltage):
        if voltage < 0.7:
            voltage = 0.7
        elif voltage > 2.275:
            voltage = 2.275
        value = (voltage - 0.7) // 0.025
        self.__write_8bit(REG_DC_TO_DC2_OUTPUT_VOLTAGE, value & 0x3f)
        
    @property
    def dc_to_dc2_vrc_enable(self):
        return self.__read_bit(REG_DC_TO_DC2_DYNAMIC_VOLTAGE_CONTROL, 2)
    
    @dc_to_dc2_vrc_enable.setter
    def dc_to_dc2_vrc_enable_setter(self, value):
        self.__set_bit(REG_DC_TO_DC2_DYNAMIC_VOLTAGE_CONTROL, 2, value)
    
    @property
    def dc_to_dc2_vrc_slope(self):
        return self.__read_bit(REG_DC_TO_DC2_DYNAMIC_VOLTAGE_CONTROL, 0)
    
    @dc_to_dc2_vrc_slope.setter
    def dc_to_dc2_vrc_slope_setter(self, value):
        self.__set_bit(REG_DC_TO_DC2_DYNAMIC_VOLTAGE_CONTROL, 0, value)
    
    @property
    def dc_to_dc1_voltage(self):
        return ((self.__read_8bit(REG_DC_TO_DC1_OUTPUT_VOLTAGE) & 0x7f) * 0.025) + 0.7
    
    @dc_to_dc1_voltage.setter
    def dc_to_dc1_voltage_setter(self, voltage):
        if voltage < 0.7:
            voltage = 0.7
        elif voltage > 3.5:
            voltage = 3.5
        value = (voltage - 0.7) // 0.025
        self.__write_8bit(REG_DC_TO_DC1_OUTPUT_VOLTAGE, value & 0x7f)
    
    @property
    def dc_to_dc3_voltage(self):
        return ((self.__read_8bit(REG_DC_TO_DC3_OUTPUT_VOLTAGE) & 0x7f) * 0.025) + 0.7
    
    @dc_to_dc3_voltage.setter
    def dc_to_dc3_voltage_setter(self, voltage):
        if voltage < 0.7:
            voltage = 0.7
        elif voltage > 3.5:
            voltage = 3.5
        value = (voltage - 0.7) // 0.025
        self.__write_8bit(REG_DC_TO_DC3_OUTPUT_VOLTAGE, value & 0x7f)
    
    @property
    def ldo2_voltage(self):
        return (((self.__read_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE) >> 4) & 0x0f) * 0.1) + 1.8
    
    @ldo2_voltage.setter
    def ldo2_voltage_setter(self, voltage):
        if voltage < 1.8:
            voltage = 1.8
        elif voltage > 3.3:
            voltage = 3.3
        value = (self.__read_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE) & 0x0f) | ((((voltage - 1.8) // 0.1) << 4) & 0xf0)
        self.__write_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE, value)
    
    @property
    def ldo3_voltage(self):
        return ((self.__read_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE) & 0x0f) * 0.1) + 1.8
    
    @ldo3_voltage.setter
    def ldo3_voltage_setter(self, voltage):
        if voltage < 1.8:
            voltage = 1.8
        elif voltage > 3.3:
            voltage = 3.3
        value = (self.__read_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE) & 0xf0) | (((voltage - 1.8) // 0.1) & 0x0f)
        self.__write_8bit(REG_LDO2_LDO3_OUTPUT_VOLTAGE, value)
    
    @property
    def acin_over_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 7)
    
    @property
    def acin_insert_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 6)
    
    @property
    def acin_remove_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 5)
    
    @property
    def vbus_over_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 4)
    
    @property
    def vbus_insert_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 3)
    
    @property
    def vbus_remove_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 2)
    
    @property
    def vbus_valid_but_lower_than_vhold_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_1, 1)
    
    @property
    def battery_insert_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 7)
    
    @property
    def battery_remove_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 6)
    
    @property
    def battery_active_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 5)
    
    @property
    def battery_quit_active_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 4)
    
    @property
    def battery_charging_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 3)
    
    @property
    def battery_charging_finished_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 2)
    
    @property
    def battery_over_temperature_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 1)
    
    @property
    def battery_under_temperature_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_2, 1)
    
    @property
    def pmu_over_temperature_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 7)
    
    @property
    def insufficient_charging_current_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 6)
    
    @property
    def dc_to_dc1_under_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 5)
    
    @property
    def dc_to_dc2_under_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 4)
    
    @property
    def dc_to_dc3_under_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 3)
    
    @property
    def short_time_key_press_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 1)
    
    @property
    def long_time_key_press_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_3, 0)
    
    @property
    def power_on_by_noe_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 7)
    
    @property
    def power_off_by_noe_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 6)
    
    @property
    def vbus_valid_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 5)
    
    @property
    def vbus_invalid_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 4)
    
    @property
    def vbus_session_ab_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 3)
    
    @property
    def vbus_session_end_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 2)
    
    @property
    def aps_under_voltage_irq_enable(self):
        return self.__read_bit(REG_IRQ_ENABLE_4, 0)
    
    @property
    def acin_over_voltage_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 7)
    
    @acin_over_voltage_irq_status.setter
    def acin_over_voltage_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 7, value)
        
    @property
    def acin_insert_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 6)
    
    @acin_insert_irq_status.setter
    def acin_insert_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 6, value)
    
    @property
    def acin_remove_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 5)
    
    @acin_remove_irq_status.setter
    def acin_remove_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 5, value)
    
    @property
    def vbus_over_voltage_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 4)
    
    @vbus_over_voltage_irq_status.setter
    def vbus_over_voltage_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 4, value)
    
    @property
    def vbus_insert_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 3)
    
    @vbus_insert_irq_status.setter
    def vbus_insert_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 3, value)
    
    @property
    def vbus_remove_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 2)
    
    @vbus_remove_irq_status.setter
    def vbus_remove_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 2, value)
    
    @property
    def vbus_valid_but_lower_than_vhold_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_1, 1)
    
    @vbus_valid_but_lower_than_vhold_irq_status.setter
    def vbus_valid_but_lower_than_vhold_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_1, 1, value)
    
    @property
    def battery_insert_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 7)
    
    @battery_insert_irq_status.setter
    def battery_insert_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 7, value)
    
    @property
    def battery_remove_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 6)
    
    @battery_remove_irq_status.setter
    def battery_remove_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 6, value)
    
    @property
    def battery_active_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 5)
    
    @battery_active_irq_status.setter
    def battery_active_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 5, value)
    
    @property
    def battery_quit_active_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 4)
    
    @battery_quit_active_irq_status.setter
    def battery_quit_active_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 4, value)
    
    @property
    def charging_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 3)
    
    @charging_irq_status.setter
    def charging_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 3, value)
    
    @property
    def charging_finished_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 2)
    
    @charging_finished_irq_status.setter
    def charging_finished_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 2, value)
    
    @property
    def battery_over_temperature_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 1)
    
    @battery_over_temperature_irq_status.setter
    def battery_over_temperature_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 1, value)
    
    @property
    def battery_under_temperature_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_2, 0)
    
    @battery_under_temperature_irq_status.setter
    def battery_under_temperature_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_2, 0, value)
    
    @property
    def over_temperature_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 7)
    
    @over_temperature_irq_status.setter
    def over_temperature_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 7, value)
    
    @property
    def insufficient_charging_current_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 6)
    
    @insufficient_charging_current_irq_status.setter
    def insufficient_charging_current_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 6, value)
        
    @property
    def dc_to_dc1_under_voltage_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 5)
    
    @dc_to_dc1_under_voltage_irq_status.setter
    def dc_to_dc1_under_voltage_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 5, value)
    
    @property
    def dc_to_dc2_under_voltage_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 4)
    
    @dc_to_dc2_under_voltage_irq_status.setter
    def dc_to_dc2_under_voltage_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 4, value)
    
    @property
    def dc_to_dc3_under_voltage_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 3)
    
    @dc_to_dc3_under_voltage_irq_status.setter
    def dc_to_dc3_under_voltage_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 3, value)
    
    @property
    def short_time_key_press_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 1)
    
    @short_time_key_press_irq_status.setter
    def short_time_key_press_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 1, value)
    
    @property
    def long_time_key_press_irq_status(self):
        return self.__read_bit(REG_IRQ_STATUS_3, 0)
    
    @long_time_key_press_irq_status.setter
    def long_time_key_press_irq_status_setter(self, value):
        self.__set_bit(REG_IRQ_STATUS_3, 0, value)
            
    def set_screen_brightness(self, brightness):
        if brightness < 1:
            return
        elif brightness > 12:
            brightness = 12
        
        self.__write_8bit(0x28, (self.__read_8bit(0x28) & 0x0f) | (brightness << 4))
    
    def get_battery_state(self):
        if self.__read_8bit(0x01) & 0x20:
            return True
        else:
            return False
    
    def get_battery_power(self):
        return self.__read_24bit(0x70) * 0.00055
        
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
        
        self.__write_8bit(addr, (self.__read_8bit(addr) & 0x80) | (voltage & 0x7f))
        
    def set_ldo_voltage(self, number, voltage):
        if number < 2 or number > 3:
            return
        
        if voltage > 3300:
            voltage = 15
        else:
            voltage = (voltage // 100) - 18
        
        value = self.__read_8bit(0x28)
        
        if number == 2:
            self.__write_8bit(0x28, (value & 0x0f) | (voltage << 4))
        else:
            self.__write_8bit(0x28, (value & 0xf0) | voltage)
        
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
        
        value = self.__read_8bit(0x33)
        value = (value & 0xf0) | (options.index(current) & 0x0f )
        self.__write_8bit(0x33, value)
    
    def toggle_register_bit(self, addr, mask, state):
        value = self.__read_8bit(addr)

        if state:
            value |= mask
        else:
            value &= ~mask
    
        self.__write_8bit(addr, value)
        
    def set_lcd_reset(self, state):
        self.toggle_register_bit(0x96, 0x02, state)
    
    def set_bus_power_mode(self, state):
        if state:
            self.__write_8bit(0x12, self.__read_8bit(0x12) & 0xbf)
            self.__write_8bit(0x90, (self.__read_8bit(0x90) & 0xf8) | 0x01)
        else:
            self.__write_8bit(0x91, (self.__read_8bit(0x91) & 0x0f) | 0Xf0)
            self.__write_8bit(0x90, (self.__read_8bit(0x90) & 0xf8) | 0x02)
            self.__read_8bit(0x91);
            self.__write_8bit(0x12, self.__read_8bit(0x12) | 0x40)

    def get_battery_voltage(self):
        return self.__read_12bit(0x78) * 0.0011
    
    def get_battery_current(self):
        current_in = self.__read_13bit(0x7a)
        current_out = self.__read_13bit(0x7c)
        return (current_in - current_out) * 0.5
    
    def get_vin_voltage(self):
        return self.__read_12bit(0x56) * 0.0017
    
    def get_vin_current(self):
        return self.__read_12bit(0x58) * 0.625
    
    def get_vbus_voltage(self):
        return self.__read_12bit(0x5a) * 0.0017
    
    def get_vbus_current(self):
        return self.__read_12bit(0x5c) * 0.375

    def set_speaker_enable(self, state):
        self.toggle_register_bit(0x94, 0x04, state)
    
    def get_input_state(self):
        return self.__read_8bit(0x00)
        
    def is_vbus(self):
        if self.get_input_state() & 0x20:
            return True
        else:
            return False
    
    def set_coloumb_clear(self, state):
        self.__write_8bit(0xb8, 0x20)
    
    def get_battery_coloumb_in(self):
        return self.__read_32bit(0xb0) * 0.3640888888888889
    
    def get_battery_coloumb_out(self):
        return self.__read_32bit(0xb4) * 0.3640888888888889
    
    def get_battery_charging_current(self):
        return self.__read_12bit(0x7a) * 0.5
    
    def get_aps_voltage(self):
        return self.__read_12bit(0x7e) * 0.0014
    
    def poweroff(self):
        self.__write_8bit(0x32, self.__read_8bit(0x32) | 0x80);
    
    def set_adc_state(self, state):
        if state:
            value = 0xff
        else:
            value = 0x00
            
        self.__write_8bit(0x82, value)
    
    def prepare_to_sleep(self):
        self.set_adc_state(False)
        self.set_led(False)
        self.dc_to_dc3 = False
    
    def restore_from_light_sleep(self):
        self.dc_to_dc3 = True
        self.set_led(True)
        self.set_adc_state(True)
    
    def get_warning_level(self):
        return self.__read_8bit(0x47) & 0x01        
    
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
        return (self.__read_12bit(0x5e) * 0.1) - 144.7
        
    def init(self):
        self.__write_8bit(0x30, (self.__read_8bit(0x30) & 0x04) | 0x02)
        self.__write_8bit(0x92, self.__read_8bit(0x92) & 0xf8)
        self.__write_8bit(0x93, self.__read_8bit(0x93) & 0xf8)
        self.__write_8bit(0x35, (self.__read_8bit(0x35) & 0x1c) | 0xa2)
        self.set_esp_voltage(3350)
        self.set_lcd_voltage(2800)
        self.set_ldo_voltage(2, 3300)
        self.set_ldo_voltage(3, 2000)
        self.ldo2_enable = True
        self.dc_to_dc3_enable = True
        self.set_led(True)
        self.set_charging_current(100)
        self.__write_8bit(0x95, (self.__read_8bit(0x95) & 0x72) | 0x84)
        self.__write_8bit(0x36, 0x4c)
        self.__write_8bit(0x82, 0xff)
        
        self.set_lcd_reset(False)
        time.sleep_ms(100)
        self.set_lcd_reset(True)
        
        if self.__read_8bit(0x00) & 0x08:
            self.__write_8bit(0x30, self.__read_8bit(0x30) | 0x80)
            self.set_bus_power_mode(True)
        else:
            self.set_bus_power_mode(False)

