from sympy import atan2

import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from numpy import sign
class FollowMeNode(Node):

  def __init__(self):
    super().__init__('follow_me_node')
    
    #PUBLISHER
    self.control_publisher=self.create_publisher(AckermannDriveStamped, '/cmd_ackermann', 10)          

    #SUBSCRIBERS
    self.odom_subscriber=self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
    

    #TIMER
    frequency = 20 #Hz
    timer_period = 1.0 / frequency  # seconds
    self.timer=self.create_timer(timer_period, self.timer_callback)
    

    #PID VELOCITY CONTROL PARAMETERS
    self.Ti_v=0.5
    self.Td_v=0.1
    self.Kp_v=1.0
    self.Ki_v=1/self.Ti_v
    self.Kd_v=self.Td_v
    
    
    
    #PID STEERING CONTROL PARAMETERS
    self.Ti_phi=0.5 
    self.Td_phi=0.1
    self.Kp_phi=1.0
    self.Ki_phi=1/self.Ti_phi
    self.Kd_phi=self.Td_phi

    #INITIALIZATION
    self.last_time=self.get_clock().now()
    self.iteration = 0
    self.sum_dt = 0.0
    self.control_v=0.0
    self.control_phi=0.0  
    self.deviation_v=0.0
    self.deviation_phi=0.0
    self.integral_v=0.0
    self.integral_phi=0.0 
    self.last_deviation_v=0.0
    self.last_deviation_phi=0.0 
    self.target_distance=0.0
    self.last_target_angle=0.0
    self.time_since_last_detection=0.0  
    self.lost_target_time=0.0
    self.robot_x=0.0
    self.robot_y=0.0
    self.robot_theta=0.0


    #FLAGA Z /Target_Pose - na tym etapie ustawiona na ,,sztywno'' na True, ale docelowo będzie aktualizowana przez subskrypcję
    self.target_detected = True
    self.deviation_v = 0.1  # Przykładowa wartość odchylenia prędkości
    self.deviation_phi = 0.05  # Przykładowa wartość odchylenia kąta skrętu
    self.target_angle=0.0 
    self.target_distance=0.0

  def timer_callback(self):
    
    #CLOCK AND DT CALCULATION
    current_time=self.get_clock().now()
    self.dt=(current_time-self.last_time).nanoseconds/1e9
    self.last_time=current_time

    #AVERAGE DT CALCULATION FOR DEBUGGING PURPOSES
    self.iteration+=1    
    if self.iteration < 100:
      self.sum_dt += self.dt
    elif self.iteration == 100:
      average_dt = self.sum_dt / 100
      self.get_logger().debug(f"Average dt over 100 iterations: {average_dt:.3f} seconds")   
      self.iteration = 0 
      self.sum_dt = 0.0  
    
    if self.target_detected==False:
       self.lost_target_time+=self.dt
    else:
        self.lost_target_time=0.0

    if self.target_detected:
       self.time_since_last_detection = 0.0

      #MASCHINE STATE
    if self.lost_target_time<0.50:
        self.following()
        self.get_logger().debug("Target detected - following mode. {control_v:.2f} m/s, control_phi: {self.control_phi:.2f} rad")
    else:
        self.searching()
        self.get_logger().debug("Target not detected - searching mode. {control_v:.2f} m/s, control_phi: {self.control_phi:.2f} rad")
    
    #PUBLISHING CONTROL COMMANDS
    ack_msg=AckermannDriveStamped()
    ack_msg.header.stamp=current_time.to_msg()
    ack_msg.drive.speed=self.control_v
    ack_msg.drive.steering_angle=self.control_phi
    self.control_publisher.publish(ack_msg)

  def following(self):
      
      #VELOCITY CONTROL PARAMETERS
      Ts=self.dt
      self.integral_v += self.deviation_v * Ts
      derivative_v=(self.deviation_v - self.last_deviation_v) / Ts if Ts != 0 else 0
      self.control_v=self.Kp_v*self.deviation_v + self.Ki_v*self.integral_v + self.Kd_v*derivative_v
      self.last_deviation_v = self.deviation_v

      #STEERING CONTROL PARAMETERS
     
      self.integral_phi += self.deviation_phi * Ts
      derivative_phi=(self.deviation_phi - self.last_deviation_phi) / Ts if Ts != 0 else 0
      self.control_phi=self.Kp_phi*self.deviation_phi + self.Ki_phi*self.integral_phi + self.Kd_phi*derivative_phi
      self.last_deviation_phi = self.deviation_phi

      if self.target_detected==True:
        self.last_target_angle=self.target_angle

  def searching(self):
      self.time_since_last_detection += self.dt
      #ROBOT SEARCHING
      self.control_v=0.1
      
      if self.time_since_last_detection < 5.0:
        self.control_phi= sign(self.last_target_angle)*0.5
      else:
         self.searching_mode()

  def searching_mode(self):
      self.control_v=0.1
      straight_time=5.0
      turning_time=5.0
      if self.time_since_last_detection % (straight_time + turning_time) < straight_time:
          self.control_phi = sign(self.last_target_angle) * 0.5
      else:
          self.control_phi=0  
  
  def odom_callback(self, msg):
      #EXTRACTING ODOMETRY DATA
      self.robot_x=msg.pose.pose.position.x
      self.robot_y=msg.pose.pose.position.y

      #CALCULATING ROBOT ORIENTATION (THETA) FROM QUATERNION
      q=msg.pose.pose.orientation
      siny_cosp=2*(q.w*q.z+q.x*q.y)
      cosy_cosp=1-2*(q.y*q.y+q.z*q.z)
      self.robot_theta=atan2(siny_cosp, cosy_cosp) 



def main(args=None):
  rclpy.init(args=args)
  node=FollowMeNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()
  


