#!/usr/bin/env python3

import rospy
import smach 
import numpy as np
from smach_ros import SimpleActionState
from rsx_rover.msg import GPSMsg, StateMsg
from std_srvs.srv import Empty, EmptyResponse
import argparse

class StateMachineNode():

    def __init__(self, args):

        self.state_subscriber = rospy.Subscriber(StateMsg, self.state_callback)
        self.MODE = "IDLE"
        self.GPS_GOALS = np.zeros(0,3)
        self.task_config = args.task_config

        # State Machine States
        self.rover_idle = self.RoverIdle()
        self.rover_initialize = self.RoverInitialize()
        self.rover_start = self.RoverStart()
        self.rover_gps_traverse = self.RoverGPSTraverse()
        self.rover_aruco_traverse = self.RoverARucoTraverse()

    def state_callback(self, state_msg):

        self.GPS_GOAL_REACHED = state_msg.GPS_GOAL_REACHED 

    def mode_callback(self, request):
        self.handle_launch()
        return EmptyResponse()


class RoverIdle(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state IDLE')

        # Your state execution goes here
        if self.MODE == "IDLE":
            return 'STAY'
        elif self.MODE == "AUTONOMY":
            return 'MOVE_TO_INTIALIZE'
        elif self.MODE == "MANUAL":
            return 'MOVE_TO_MANUAL'

class RoverManual(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['MOVE_TO','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state MANUAL')
        # Your state execution goes here
        if self.STATE == 'MANUAL':
            return 'STAY'
        elif self.STATE == 'AUTONOMY':
            return 'MOVE_TO_INITIALIZE'
        elif self.STATE == 'IDLE':
            return 'MOVE_TO_IDLE'

class RoverInitialize(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        # Your state execution goes here
        if :
            return 'outcome1'
        else:
            return 'outcome2'

class RoverStart(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        # Your state execution goes here
        if xxxx:
            return 'outcome1'
        else:
            return 'outcome2'
    
class RoverGPSTraverse(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        # Your state execution goes here
        if xxxx:
            return 'outcome1'
        else:
            return 'outcome2'

class RoverARucoTraverse(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        # Your state execution goes here
        if xxxx:
            return 'outcome1'
        else:
            return 'outcome2'

class RoverGPSCheckpoint(smach.State):

    def __init__(self):
        smach.State.__init__(self, outcomes=['outcome1','outcome2'])
        self.counter = 0
        # Your state initialization goes here

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        # Your state execution goes here
        if xxxx:
            return 'outcome1'
        else:
            return 'outcome2'
    
# class RoverScan(smach.State):

#     def __init__(self):
#         smach.State.__init__(self, outcomes=['outcome1','outcome2'])
#         self.counter = 0
#         # Your state initialization goes here

#     def execute(self, userdata):
#         rospy.loginfo('Executing state FOO')
#         # Your state execution goes here
#         if xxxx:
#             return 'outcome1'
#         else:
#             return 'outcome2'

# class RoverTimeout(smach.State):

#     def __init__(self):
#         smach.State.__init__(self, outcomes=['outcome1','outcome2'])
#         self.counter = 0
#         # Your state initialization goes here

#     def execute(self, userdata):
#         rospy.loginfo('Executing state FOO')
#         # Your state execution goes here
#         if xxxx:
#             return 'outcome1'
#         else:
#             return 'outcome2'

# class RoverMissionOver(smach.State):

#     def __init__(self):
#         smach.State.__init__(self, outcomes=['outcome1','outcome2'])
#         self.counter = 0
#         # Your state initialization goes here

#     def execute(self, userdata):
#         rospy.loginfo('Executing state FOO')
#         # Your state execution goes here
#         if xxxx:
#             return 'outcome1'
#         else:
#             return 'outcome2'

def main(args):
    rospy.init_node('rsx_rover_state_machine')

    state_machine_node = StateMachineNode(args)

    # Create a SMACH state machine
    sm = smach.StateMachine(outcomes=['MISSION_OVER', 'MISSION_ABORTED'])

    # Open the container
    with sm:
        # Add states to the container
        smach.StateMachine.add('RoverIdle', state_machine_node.RoverIdle(),
                               transitions={'STAY': 'RoverIdle',
                                            'MOVE_TO_INITIALIZE' : 'RoverInitialize'})
        smach.StateMachine.add('RoverManual', state_machine_node.RoverManual(),
                               transitions={'STAY': 'RoverManual',
                                            'MOVE_TO_INITIALIZE' : 'RoverInitialize', 
                                            'MOVE_TO_IDLE' : 'RoverIdle'})
        smach.StateMachine.add('RoverInitialize', RoverInitialize(), 
                               transitions={'LOADING' : 'RoverInitialize',
                                            'LOAD_COMPLETE' : 'RoverStart'})
        smach.StateMachine.add('RoverStart', state_machine_node.RoverStart(), 
                               transitions={'GPS_GOAL_QUEUED':'RoverGPSTraverse'})
        smach.StateMachine.add('RoverGPSTraverse', state_machine_node.RoverGPSTraverse(), 
                               transitions={'GPS_GOAL_REACHED':'RoverARucoTraverse'})
        smach.StateMachine.add('RoverGPSCheckpoint', state_machine_node.RoverGPSCheckpoint(),
                               transitions={'GPS_GOAL_REACHED':'RoverARucoTraverse'})
        smach.StateMachine.add('RoverARucoTraverse', state_machine_node.RoverARucoTraverse(),
                               transitions={'ARUCO_FOUND':'RoverTransition', 
                                            'SEARCHING': 'RoverScan'})

    # Execute SMACH plan
    outcome = sm.execute()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import command line arguments for task')
    parser.add_argument('task_config', metavar='f', default="~/rover_ws/src/rsx-rover/task_config.json",
                        help='Task configuration file')

    args = parser.parse_args()
    main(args)