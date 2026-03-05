import rclpy
from rclpy.node import Node

class FollowMeNode(Node):

  def __init__(self):
    super().__init__('follow_me_node')
    
    #TIMER
    frequency = 20 #Hz
    timer_period = 1.0 / frequency  # seconds
    self.timer=self.create_timer(timer_period, self.timer_callback)
    
  
    #INICJALIZACJA ZMIENNYCH
    self.last_time=self.get_clock().now()
    self.iteration = 0

  def timer_callback(self):
    #ZEGAR I OBLICZANIE DT
    current_time=self.get_clock().now()
    dt=(current_time-self.last_time).nanoseconds/1e9
    self.last_time=current_time
    self.get_logger().info(f"dt = {dt:.3f} seconds")

    #Informacja o średnim dt co 100 iteracji
    self.iteration+=1    
    if self.iteration < 100:
      sum_dt += dt
    elif iteration == 100:
      average_dt = sum_dt / 100
      self.get_logger().debug(f"Average dt over 100 iterations: {average_dt:.3f} seconds")   
      sum_dt = 0.0
      iteration = 0 
    
      #ZMIENNA STANOW 
      



def main(args=None):
  rclpy.init(args=args)
  node=FollowMeNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()
  


