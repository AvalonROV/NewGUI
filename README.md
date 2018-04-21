# NewGUI

(correct for 22/03 update)

working on
- folder containing the files I am directly editing, for convenience

blank gui
- script that is a template GUI, blank, which is of the correct format so
that different GUIs can be integrated with each other easily

calculating_location
- GUI for calculating the location of the aircraft wreck

calculating_power_gen
- GUI for calculating the max power possible to be generated

copilot_gui
- includes OBS graph, IMU and depth readings, flight location data calculation,
power calculation, web address for deepzoom

graphing
- GUI for plotting OBS data from the wifi connection (not necessary now)

motor_debug
- GUI to debug motor. User inputs thrust value [-400, 400], can flip direction
of motor by pressing 'Flip Direction' button, and can change order of string.
GUI displays the three lists produced from these operations if you press 
'Display String Order' button, and displays thruster values string to console

pilot_gui
- includes two camerafeed displays, two sliders to select camerafeed source, 
indicators for inflating and detatching lifting bag and dropping inductive power
source, readouts for IMU and depth, opens motor_debug window on startup

README
- this doc

single_camerafeed_display
- using openCV to display camerafeed from the laptop webcam