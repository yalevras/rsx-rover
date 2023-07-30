#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import String, UInt8
from rover.msg import ArmInputs
#import arm_servo
#from rover.srv import Corrections

'''
publishes: arm_state, arm_inputs (joystick value)
subscribes: Joy
rosservice: correction
'''

class Controller():
    """
    (None)

    This class represents an instance of controller node and connects the node to 
    its publishing and subscribing topics
    """

    def __init__(self):

        ## Attributes to hold data for publishing to topics
        # Attribute to publish state
        self.state               = "Idle"

        # Attribute to store/publish killswitch value
        self.killswitch          = 0

        # Attribute to publish arm inputs (with initialized values)
        self.values              = ArmInputs()
        self.values.l_horizontal = 0
        self.values.l_vertical   = 0
        self.values.r_horizontal = 0
        self.values.r_vertical   = 0
        self.values.l1           = 0
        self.values.r1           = 0
        self.values.l2           = 0
        self.values.r2           = 0
        self.values.x            = 0
        self.values.o            = 0

        ## Attribute to store servo state
        # state -> angle:
        # 0 -> 63 degrees
        # 1 -> 84 degrees
        self.servo               = 0

        ## Variables for ROS publishers and subscrives
        self.joy_sub             = rospy.Subscriber("joy", Joy, self.getROSJoy)
        self.state_pub           = rospy.Publisher("arm_state", String, queue_size=0)
        self.input_pub           = rospy.Publisher("arm_inputs", ArmInputs, queue_size=0)
        self.killswitch_pub      = rospy.Publisher('arm_killswitch', UInt8, queue_size=0)

        # # Printing state on the console and publishing it
        # print("State:", self.state)
        # self.state_pub.publish(self.state)

        # # If square is pressed, flip the servo configuration
        # if rawButtons[3] == 1:
        #     self.servo = not self.servo
            
        #     if self.servo:
        #         arm_servo.write_servo_high_angle()
        #         print("Servo going to 84 degrees configuration")
            
        #     else:
        #         arm_servo.write_servo_low_angle()
        #         print("Servo going to 63 degrees configuration")
        self.rate = rospy.Rate(1000)

        triggered = 0
        while not rospy.is_shutdown():

        # Print/Publish the inputs if state is neither Idle or Setup
            if self.state != "Idle" and self.state != "Setup":

                if (abs(self.values.l_horizontal) >= 0.05 or abs(self.values.l_vertical) >= 0.05 or 
                    abs(self.values.r_horizontal) >= 0.05 or abs(self.values.r_vertical) >= 0.05 or 
                    (self.values.l1 - self.values.r1) or (self.values.l2 - self.values.r2) or 
                    (self.values.x - self.values.o)):
                    print(self.values)
                    self.input_pub.publish(self.values)
            
                ## If square is pressed, flip the servo configuration

                # # Open the Arduino port
                # arm_servo.open_arduino_port()

                # # If Arduino port is properly opened, flip servo configurations
                # if arm_servo.arduino_port:

                #     if self.servo and not triggered:
                #         arm_servo.write_servo_high_angle()
                #         print("Servo going to 84 degrees configuration")
                #         triggered = 1

                #     elif not self.servo and triggered:
                #         arm_servo.write_servo_low_angle()
                #         print("Servo going to 63 degrees configuration")
                #         triggered = 0
                    
                #     # Close the Arduino port since it was properly opened                    
                #     arm_servo.close_arduino_port()
                
                # Control rate sleep
                self.rate.sleep()

    def getROSJoy(self, joy_input : Joy) -> None:    
        ''' 
        (Joy) -> (None)

        Gets joystick values from "Joy" Topic

        Assuming using this package:
            http://wiki.ros.org/joy
        
        
        @paramters
    
        joy_input (Joy): Stores the received joystick inputs from "Joy" topic 
        '''

        ## Getting the joystick inputs
        # Axes Mapping (note: max absolute value = 1)
        # Idx : Button on PS4 (direction)
        # 0 : Left Analog Stick Horizontal (left positive, right negative)
        # 1 : Left Analog Stick vertical (Up positive, down negative)
        # 2 : L2 (1 when unpressed, -1 when full pressed)
        # 3 : Right Analog Stick Horizontal (left positive, right negative)
        # 4 : Right Analog Stick vertical (Up positive, down negative)
        # 5 : R2 (1 when unpressed, -1 when full pressed)
        # 6 : D-Pad Horizontal (left Arrow = -1, Right Arrow = 1, 0 when neither are pressed)
        # 7 : D-Pad Vertical (Up Arrow = 1, Down Arrow = -1, 0 when neither are pressed)
        rawAxes                     = joy_input.axes

        # Button Mapping (0 when unpressed, 1 when pressed)
        # Idc : Button
        # 0 : X
        # 1 : O (circle)
        # 2 : triangle
        # 3 : square
        # 4 : L1
        # 5 : R1
        # 6 : L2 (even when lightly pressed, it becomes 1)
        # 7 : R2 (even when lightly pressed, it becomes 1)
        # 8 : share
        # 9 : options
        # 10: PS
        # 11: L3
        # 12: R3
        rawButtons                  = joy_input.buttons

        # Setting the ArmInputs variable to be published later
        self.values.l_horizontal    = rawAxes[0]
        self.values.l_vertical      = rawAxes[1]
        self.values.r_horizontal    = rawAxes[3]
        self.values.r_vertical      = rawAxes[4]
        self.values.l1              = rawButtons[4]
        self.values.r1              = rawButtons[5]
        self.values.l2              = -0.5 * rawAxes[2] + 0.5
        self.values.r2              = -0.5 * rawAxes[5] + 0.5
        self.values.x               = rawButtons[0]
        self.values.o               = rawButtons[1]

        # Check if analog sticks are not moving and triggers are not pressed 
        # and any other buttons are not pressed. If any of them is false, then do not
        # change the state
        if ((not (rawAxes[0] or rawAxes[1] or rawAxes[3] or rawAxes[4])) 
            and (rawAxes[2] == 1 and rawAxes[5] == 1) and (1 not in rawButtons)
            and self.killswitch == 0):
            
            if rawAxes[7] == -1:
                self.state = "Idle"
            
            elif rawAxes[6] == 1:
                self.state = "Manual"

            elif rawAxes[7] == 1:
                self.state = "Setup"

            elif rawAxes[6] == -1:
                self.state = "IK"

        # If square is pressed, flip the servo configuration
        if rawButtons[3] == 1:
            self.servo = not self.servo

        # If triangle is pressed, change IK state if in overall state is IK
        if rawButtons[2] == 1 and self.state == "IK":
            self.values.triangle = 1

        # If PS button is pressed and killswitch was not activated, activate killswitch
        if rawButtons[10] == 1 and self.killswitch == 0:
            self.killswitch = 1
            self.killswitch_pub.publish(self.killswitch)

            # Set the state to "Idle"
            self.state      = "Idle"
        # If PS button is pressed and killswitch was already activated, deactivate it
        elif rawButtons [10] == 1 and self.killswitch == 1:
            self.killswitch = 0
            self.killswitch_pub.publish(self.killswitch)
        
        # Printing state on the console and publishing it
        print("State:", self.state, "\t killswitch:", bool(self.killswitch))
        self.state_pub.publish(self.state)
            
        # #     if self.servo:
        # #         arm_servo.write_servo_high_angle()
        # #         print("Servo going to 84 degrees configuration")
            
        # #     else:
        # #         arm_servo.write_servo_low_angle()
        # #         print("Servo going to 63 degrees configuration")

        # # Print/Publish the inputs if state is neither Idle or Setup
        # if self.state != "Idle" and self.state != "Setup":

        #     while ((rawAxes[0] or rawAxes[1] or rawAxes[3] or rawAxes[4]) 
        #            or (self.values.l2r2 != 0) or (1 in rawButtons)):
        #         print(self.values)
        #         self.input_pub.publish(self.values)



    # def updateCorrections():
    #     ''' Update the Correction values the IK node is using

    #     Paramters
    #     ---------

    #     Returns
    #     -------
    #     '''

    #     try:
    #         correctionService = rospy.ServiceProxy('update_ik_corrections', Corrections)
    #         serviceResponse = correctionService() # input data into function to send to service, response contains boolean if succesfully updated or not
    #     except rospy.ServiceException as ex:
    #         print("Service call failed: %s"%ex)
 
if __name__ == "__main__":
 
    try:
        rospy.init_node("controller")
        
        Controller_Node = Controller()

        rospy.spin()

        
    except rospy.ROSInterruptException:
        pass