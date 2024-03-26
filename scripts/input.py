#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

# Variables
hz = 20
counter = 0
step_stable = True
sq_stable = True
signal = 0.0
error = 0.01
sq_cond = False

# Stop Condition
def stop():
    # Setup the stop message (can be the same as the control message)
    print("Stopping")

if __name__=='__main__':
	# Initialise and Setup node
	rospy.init_node("Set_Point_Generator")
	rate = rospy.Rate(hz)
	rospy.on_shutdown(stop)

	# Setup Publishers and subscribers here
	pwm_pub = rospy.Publisher("/cmd_pwm", Float32, queue_size = 1)

	print("The Set Point Generator is Running")

	# Run the node
	while not rospy.is_shutdown():
		signal_type = rospy.get_param("/signal/type", default = "No signal type found")
		amplitude = rospy.get_param("/signal/amplitude", default = 1.0)
		freq = rospy.get_param("/signal/freq", default = 0.5)
		sq_up = rospy.get_param("/signal/square/up_limit", default = 1.0)
		sq_down = rospy.get_param("/signal/square/down_limit", default = -1.0)
		step_value = rospy.get_param("/signal/step/value", default = 1.0)

		time = rospy.get_time()

		# Sine signal
		if (signal_type == "Sine"):
			signal = amplitude*np.sin(time*freq)
		# Square signal
		elif (signal_type == "Square"):
			if (counter >= (hz/2)/freq):
				counter = 0
				sq_cond = not(sq_cond)
			else:
				counter += 1

			if (signal != sq_up and sq_cond and (signal > (sq_up+error) or signal < (sq_up-error))):
				if (sq_stable or counter == 0):
					m = sq_up - signal
					sq_stable = False
				signal += m/8
			elif (signal != sq_down and not(sq_cond) and (signal > (sq_down+error) or signal < (sq_down-error))):
				if (sq_stable or counter == 0):
					m = sq_down - signal
					sq_stable = False
				signal += m/8
			else:
				if (sq_cond):
					signal = sq_up
				elif (not(sq_cond)):
					signal = sq_down
				sq_stable = True
		# Step signal
		elif (signal_type == "Step"):
			if (signal != step_value and signal > (step_value+error) or signal < (step_value-error)):
				if (step_stable):
					x = step_value - signal
					step_stable = False
				signal += x/8
			else:
				signal = step_value
				step_stable = True
		# No signal
		else:
			signal = 0
			rospy.loginfo(signal)

		pwm_pub.publish(signal)
		rospy.loginfo("Type: %s, Value: %f", signal_type, signal)

		rate.sleep()