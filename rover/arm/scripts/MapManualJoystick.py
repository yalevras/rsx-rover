

import time
import pygame 
import GetManualJoystickFinal
#import anglepos


joy_input = GetManualJoystickFinal.GetManualJoystick()

controller_pos = [0,0,0,0,0,0,0,0]
speed_limit = [1000/120, 1000/160, 4000/120, 2000/20, 1500/20, 1500/20, 10000/40]                    # Gear Ratio are after the /
t = 0



def SetJointSpeed(joy_input, controller_pos, speed_limit, dt):

    return (speed_limit*(joy_input)*dt)+ controller_pos



def MapJoystick(joy_input, controller_pos, speed_limit, dt):   #takes in the joystick input(I), the current position of the motors (O), the speed limits (S)

    controller_pos[0] = SetJointSpeed(joy_input[0], controller_pos[0], speed_limit[0], dt)
    controller_pos[1] = SetJointSpeed(-joy_input[1], controller_pos[1], speed_limit[1], dt)
    controller_pos[2] = SetJointSpeed(joy_input[3], controller_pos[2], speed_limit[2], dt)
    controller_pos[3] = SetJointSpeed(joy_input[2], controller_pos[3], speed_limit[3], dt)
    controller_pos[4] = SetJointSpeed(joy_input[4], controller_pos[4], speed_limit[4], dt)
    controller_pos[5] = SetJointSpeed(joy_input[5], controller_pos[5], speed_limit[5], dt)
    controller_pos[6] = SetJointSpeed(joy_input[6], controller_pos[6], speed_limit[6], dt)
    controller_pos[7] = joy_input[7]
    


    return controller_pos




#  def ManualDrive(GoalPos, SpeedLimit, dt):
#      return MapJoystick(GetJoysticParams(), GoalPos, SpeedLimit, dt)

# while (True):
    
#     pos = MapJoystick(GetManualJoystickFinal.GetManualJoystick(), controller_pos, speed_limit, t-time.time())
#     t = time.time()
#     print(pos)
#     time.sleep(.01)

    
