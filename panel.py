import RPi.GPIO as GPIO

class carPanel:
	speed_pin = 12
	rpm_pin = 33
	
	speedometer = ""
	rpm_meter = ""
	
	@classmethod
	def start(cls, speed_pin = 12, rpm_pin = 33):
		cls.speed_pin = speed_pin
		cls.rpm_pin = rpm_pin
		
		GPIO.setmode(GPIO.BOARD)
		
		GPIO.setup(speed_pin, GPIO.OUT)
		cls.speedometer = GPIO.PWM(speed_pin, 1.0)
		cls.speedometer.start(50)
		
		GPIO.setup(rpm_pin, GPIO.OUT)
		cls.rpm_meter = GPIO.PWM(rpm_pin, 1.0)
		cls.rpm_meter.start(50)
	
	@classmethod
	def set_speed(cls, speed_meters_per_second):
		kmetric_speed = speed_meters_per_second * 3.6
		freq = kmetric_speed * 5
		cls.speedometer.ChangeFrequency(freq + 0.1)

	@classmethod
	def set_rpm(cls, rpm):
		freq = rpm/30
		cls.rpm_meter.ChangeFrequency(freq + 0.1)
