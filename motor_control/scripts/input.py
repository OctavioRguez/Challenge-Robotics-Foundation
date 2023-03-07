#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Float32

#Variables
hz = 20
counter = 0
step_stable = True
sq_stable = True
signal = 0.0
error = 0.01
sq_cond = False

#Stop Condition
def stop():
    #Setup the stop message (can be the same as the control message)
    print("Stopping")

if __name__=='__main__':
    #Initialise and Setup node
    rospy.init_node("Set_Point_Generator")
    rate = rospy.Rate(hz)
    rospy.on_shutdown(stop)

    #Setup Publishers and subscribers here
    pwm_pub = rospy.Publisher("/cmd_pwm", Float32, queue_size=1)

    print("The Set Point Generator is Running")

    #Run the node
    while not rospy.is_shutdown():
        #Write your code here
	mode = rospy.get_param("/mode", "No Parameter Found")
	amplitude = rospy.get_param("/amplitude", 1.0)
	freq = rospy.get_param("/freq", 0.5)
	sq_up = rospy.get_param("/sq_up", 1.0)
	sq_down = rospy.get_param("/sq_down", -1.0)
	step_value = rospy.get_param("/step_value", 1.0)

        time = rospy.get_time()

	#Sine signal
	if (mode == "Sine"):
	    signal = amplitude*np.sin(time*freq)
	#Square signal
	elif (mode == "Square"):
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
	#Step signal
	elif (mode == "Step"):
	    if (signal != step_value and signal > (step_value+error) or signal < (step_value-error)):
		if (step_stable):
		    x = step_value - signal
		    step_stable = False
		signal += x/8
	    else:
		signal = step_value
		step_stable = True
	else:
	    signal = 0

        pwm_pub.publish(signal)
        rospy.loginfo("Mode: %s, signal: %f", mode, signal)

        rate.sleep()
