#!/usr/bin/env python3

from CAN_utilities import *
import rospy
from std_msgs.msg import Float32MultiArray

class CAN_Send():
	"""
	(None)

	This class represents an instance of the CAN_Send node that connects to Safety node
	by arm_safe_goal_pos topic and sends the received positions to the CAN bus
	"""

	def __init__(self):
		self.pub_rate = 2000

		# Subscriber buffers
		self.SAFE_GOAL_POS	 	= [0, 0, 0, 0, 0, 0, 0]
		# self.CURR_POS			= [0, 0, 0, 0, 0, 0, 0]

		# Variables for ROS publishers and subscribers
		self.SafePos_sub 		= rospy.Subscriber("arm_safe_goal_pos", Float32MultiArray, self.callback_SafePos)
		# self.CurrPos_sub		= rospy.Subscriber("arm_curr_pos", Float32MultiArray, self.callback_CurrPos)

		# ROS
		try:
			self.send_msgs()
		except rospy.ROSInterruptException:
			print("Exception Occured")
			pass
	
	# def callback_CurrPos(self, data : Float32MultiArray):
	# 	"""
	# 	(Float32MultiArray) -> (None)

	# 	Callback funtion for receving CURR_POS data and updating the CURR_POS variable

	# 	@parameters

	# 	data (Float32MultiArray) : The data from the topic is stored in this parameter
	# 	"""
		
	# 	# Save the data from the topic into our buffer
	# 	self.CURR_POS = list(data.data)

	def callback_SafePos(self, data : Float32MultiArray):
		"""
		(Float32MultiArray) -> (None)

		Callback funtion for receving SAFE_GOAL_POS data and updating the SAFE_GOAL_POS variable

		@parameters

		data (Float32MultiArray) : The data from the topic is stored in this parameter
		"""

		# Save the data from the topic into our buffer
		self.SAFE_GOAL_POS = list(data.data)
	
	def send_msgs(self):
		
		# Set publishing rate to self.pub_rate
		rate = rospy.Rate(self.pub_rate)

		# Start the infinite loop
		while not rospy.is_shutdown():

			# Convert SparkMAX angles to SparkMAX data packets
			spark_input = generate_data_packet(self.SAFE_GOAL_POS) # assuming data is safe
			print(self.SAFE_GOAL_POS)
			
			# Send data packets
			for i in range(1, len(spark_input)+1):
						
				# Motor number corresponds with device ID of the SparkMAX
				motor_num = 10 + i

				#print(spark_input)
				if motor_num > 10 and motor_num < 18:
					id = generate_can_id(dev_id= motor_num, api= CMD_API_POS_SET)
					send_can_message(can_id= id, data= spark_input[i - 1])
				
				else:
					break

			# Control rate
			rate.sleep()


if __name__=="__main__":
        
	# # Instantiate CAN bus
	# initialize_bus()
	
	# Initialize node
	rospy.init_node('CAN_Send', anonymous=True)

	# Setup and run node
	CAN_Send_Node = CAN_Send()

	# Spin to keep node alive
	rospy.spin()
