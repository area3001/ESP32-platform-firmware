import machine, sys, system, time, os, buttons
import _device as device

rtc = machine.RTC()
rtc.write(0,0)
rtc.write(1,0)

device.prepareForWakeup()

__chk_recovery = False
__chk_develop  = False

if machine.wake_reason() == (7, 0) and machine.nvs_getint("system", 'factory_checked'):
	try:
		recovery_button = buttons.BTN_START #Use the START button if available
	except:
		recovery_button = buttons.BTN_B #Else use the B button
	__chk_recovery = buttons.value(recovery_button)
	__chk_develop = buttons.value(buttons.BTN_LEFT)

if __chk_recovery:
	app = "dashboard.recovery"
elif __chk_develop:
	app = "dev"
else:
	app = rtc.read_string()
	if not app:
		if not machine.nvs_getint("system", 'factory_checked') == 2:
			app = "factory_checks"
		else:
			app = machine.nvs_getstr("system", 'default_app')
			if not app:
				app = 'dashboard.home'

if app and not (app == "shell" or app == "dev"):
	try:
		print("Starting app '%s'..." % app)
		system.__current_app__ = app
		if app:
			__import__(app)
	except BaseException as e:
		sys.print_exception(e)
		if not machine.nvs_get_u8("system", "ignore_crash"):
			print("Fatal exception in the running app!")
			system.crashedWarning()
			time.sleep(3)
			system.launcher()

if app and app == "shell":
	print("\nWelcome to the python shell of your badge!\nNeed help? Check out https://docs.badge.team/ for documentation.")
