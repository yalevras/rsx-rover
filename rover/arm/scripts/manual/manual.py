#!/usr/bin/env python3

import numpy as np
import time
import rospy
from rover.msg import ArmInputs
from std_msgs.msg import *

######################## CLASSES ##########################

class Manual():
    """
    (None)
    
    Initializes the manual node and connects it to 
    different topics for publishing and subscribing
    """

    def __init__(self):

        ## Buffer for controller input
        # Idx - Associated Controller input:
        # 0 - Left analog horizonal
        # 1 - Left analog vertical
        # 2 - Right analog horizonal
        # 3 - Right analog vertical
        # 4 - L1 / R1 
        # 5 - L2 / R2 (analog)
        # 6 - X / circle
        # 7 - PlayStation (killswitch)
        self.controller_input    = [0, 0, 0, 0, 0, 0, 0, 0]

        ## Buffer for storing and publishing goal position
        # Idx - Associated Motor:
        # 0 - Motor 11 (Base)
        # 1 - Motor 12 (Shoulder)
        # 2 - Motor 13 (Elbow)
        # 3 - Motor 14 (Elbow Roll)
        # 4 - Motor 15 (Wrist 1)
        # 5 - Motor 16 (Wrist 2)
        # 6 - Motor 17 (End Effector Open/Close)
        self.goal_pos            = Float32MultiArray()
        self.goal_pos.data       = [0, 0, 0, 0, 0, 0, 0]

        ## Buffer to hold error messages
        # Message Descriptions:
        # 0 -> No Error
        # 1 -> Faraway position
        # 2 -> Exceeding Max Current
        # 3 -> Hitting Limit Switch
        self.error_messages      = [0, 0, 0, 0, 0, 0, 0]

        ## Constant Speed limits, values are chosen by trial and error #TODO
        self.SPEED_LIMIT         = [0.001, 0.001, 0.001, 0.001, 
                                    0.001, 0.001, 0.001]

        ## Variable for the status, start at idle
        self.status              = "Idle"

        ## ROS topics: publishing and subscribing
        self.error               = rospy.Subscriber("arm_error_msg", UInt8MultiArray, self.CallbackError)
        self.state               = rospy.Subscriber("arm_state", String, self.CallbackState)
        self.input               = rospy.Subscriber("arm_inputs", ArmInputs, self.CallbackInput)  
        self.goal                = rospy.Publisher("arm_goal_pos", Float32MultiArray, queue_size=10)

    def CallbackError (self, errors: UInt8MultiArray) -> None:
        """
        (UInt8MultiArray) -> (None)

        Recieves and stores error messages from safety node. Uses them during setup process

        @parameters

        errors (UInt8MultiArray): stores error messages received from ROS topic
        """

        # Updates errors
        self.error_messages = errors.data
    
    def CallbackState (self, status: String) -> None:
        """
        (String) -> (None)

        Recieves and stores state (idle, manual, ik or setup) from controller node

        @parameters

        status (String): stores the status received from the ROS topic
        """

        # Updates state
        self.status = status.data

    def CallbackInput (self, inputs: ArmInputs) -> None:
        """
        (ArmInputs) -> (None)

        Recieves inputs from controller and if state is "Manual",
        updates the goal positions and publishes them
        
        Also has option of kill switch

        @parameters

        inputs (ArmInputs): Stores the received inputs from controller node
        """

        # Get inputs from controller
        self.controller_input[0] = inputs.l_horizontal
        self.controller_input[1] = inputs.l_vertical
        self.controller_input[2] = inputs.r_vertical
        self.controller_input[3] = inputs.r_horizontal
        self.controller_input[4] = inputs.l1r1
        self.controller_input[5] = inputs.l2r2
        self.controller_input[6] = inputs.xo
        self.controller_input[7] = inputs.ps

        # Print Statement for console view
        print("State:", self.status)
        
        # Checking the state, only proceed if in manual
        if self.status == "Manual":

            # Checking to make sure the kill switch wasn't hit
            if self.controller_input[7] == 1:
                self.status        = "Idle"

            else:

                # Update goal positions and print/publish them
                self.goal_pos.data = self.update_pos(self.controller_input[:-1], self.goal_pos.data, 
                                                     self.SPEED_LIMIT)
                print(self.goal_pos.data)
                self.goal.publish(self.goal_pos)

        elif self.state == "Setup":
            self.setup()
        
    def update_pos(self, joy_input : list, curr_goal_pos : list, speed_limit : list) -> list:   
        """
        (list(float), list(float), list(float)) -> list(float)

        Takes in controller inputs, current goal positions, speed limits and time passed
        to update goal positions

        @parameters

        joy_input (list(float)): Buffer holding the input from controller
        
        curr_goal_pos (list(float)): List containing the current goal positions (in degrees) of the motors
        
        speed_limit (list(float)): List containing tested out manually controlled speeds for each motor
        """

        # Set controller pos based on joint speed calculations/joypos
        return list(np.array(joy_input) * np.array(speed_limit) + np.array(curr_goal_pos))
    
    # def setup(self):
    #     # For each motor/controller pos...
    #     # subscribe to current angles
    #     for i in range(len(self.controller_pos)):
    #         current = self.controller_pos[i] 
    #         # Send in a large value to hit limit switch
    #         self.controller_pos[i] = 10000000
    #         # When error occurs (recieve from safety node), set it back to zero
    #         # Currently assuming error messages will be str
    #         while "LIMIT_SWITCH" not in self.error[i]:
    #             pass
    #         # detect current angle via corrections from safety
    #         self.controller_pos[i] = current
    #     pass
    #     #a variable correction value

############################## MAIN ############################

def main():

    try:
        rospy.init_node("Arm_Manual", anonymous=True)
        
        Manual_Node = Manual()

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":

    main()