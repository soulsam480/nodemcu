from machine import Pin
import time


class OdoMeter:
    def __init__(self, lcd):
        self.sensor_pin = 14  # Hardcoded GPIO pin
        self.wheel_circumference = 2.1  # meters
        self.update_interval = 5  # seconds

        self.lcd = lcd
        self.sensor = Pin(self.sensor_pin, Pin.IN)
        self.rev_count = 0
        self.total_distance = 0.0  # in kilometers
        self.last_time = time.ticks_ms()
        self.running = False

    def _on_pulse(self, pin):
        self.rev_count += 1

    def start(self):
        self.running = True
        self.sensor.irq(trigger=Pin.IRQ_RISING, handler=self._on_pulse)
        self.last_time = time.ticks_ms()
        self.lcd.clear()

        self.lcd.putstr("OdoMeter Started")
        time.sleep(1)
        self.lcd.clear()

    def stop(self):
        self.running = False
        self.sensor.irq(handler=None)
        self.lcd.clear()
        self.lcd.putstr("OdoMeter Stopped")

    def update(self):
        now = time.ticks_ms()
        elapsed_ms = time.ticks_diff(now, self.last_time)

        if elapsed_ms <= 100:
            speed = 0.0
        else:
            distance_m = self.rev_count * self.wheel_circumference  # meters
            distance_km = distance_m / 1000.0  # convert to km

            if distance_m == 0:
                speed = 0.0
            else:
                elapsed_s = elapsed_ms / 1000.0  # convert to seconds
                speed = (distance_km / elapsed_s) * 3600  # km/h

            self.total_distance += distance_km  # accumulate in km
            self.rev_count = 0
            self.last_time = now

        return self.total_distance, speed

    def display(self):
        dist, speed = self.update()
        self.lcd.clear()
        self.lcd.putstr("Distance:{:.2f}km\nSpeed:{:.1f}km/h".format(dist, speed))

    def run_forever(self):
        self.start()
        try:
            while self.running:
                self.display()
                time.sleep(self.update_interval)
        except KeyboardInterrupt:
            self.stop()
