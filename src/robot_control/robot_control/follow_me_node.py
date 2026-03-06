from numpy import sign

import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped

class FollowMeNode(Node):

  def __init__(self):
    super().__init__('follow_me_node')
    
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
    self.deviation_v=0.0
    self.deviation_phi=0.0
    self.integral_v=0.0
    self.integral_phi=0.0 
    self.last_deviation_v=0.0
    self.last_deviation_phi=0.0 

    #FLAGA Z /Target_Pose - na tym etapie ustawiona na ,,sztywno'' na True, ale docelowo będzie aktualizowana przez subskrypcję
    self.target_detected = True
    self.deviation_v = 0.1  # Przykładowa wartość odchylenia prędkości
    self.deviation_phi = 0.05  # Przykładowa wartość odchylenia kąta skrętu
    self.target_angel=0.0


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
    
      #MASCHINE STATE
    if self.target_detected:
        self.following()
        self.get_logger().debug("Target detected - following mode")
    else:
        self.searching()
        self.get_logger().debug("Target not detected - searching mode")

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

      if self.target_angle != 0.0:
        self.last_target_angle=self.target_angle

  def searching(self):
      self.time_since_last_detection += self.dt
      #ROBOT SEARCHING
      self.control_v=0.1
      
      if self.time_since_last_detection < 5.0:
        self.control_phi= sign(self.last_target_angle)*0.5
      else:
         self.searching_mode()






def main(args=None):
  rclpy.init(args=args)
  node=FollowMeNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()
  


