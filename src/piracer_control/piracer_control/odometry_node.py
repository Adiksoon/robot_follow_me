import rclpy
from rclpy.node import Node
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import tf2_ros
from tf_transformations import euler_from_quaternion, quaternion_from_euler



class OdometryNode(Node):

    def __init__(self):
        super().__init__('odometry_node')
        self.tf_broadcaster=tf2_ros.TransformBroadcaster(self)
        self.odom_publisher=self.create_publisher(Odometry, 'odom', 10)
        
        timer_period = 0.02  # seconds
        self.timer=self.create_timer(timer_period, self.timer_callback)
        self.get_logger().info("Odometry node started.")

       
       
       
        #WARUNKI POCZĄTKOWE 
        self.x=0.0
        self.y=0.0
        self.theta=0.0
        self.last_time=self.get_clock().now()
        
        #PARAMETRY ROBOTA 
        self.L=0.26 #odległość między kołami
        self.r=0.05 #promień koła
        
        #PARAMETRY TESTOWE
        self.v=0.5 
        self.phi=0.3

        #INICJALIZACJA ZMIENNYCH
        self.prev_x_dot=0.0
        self.prev_y_dot=0.0
        self.prev_theta_dot=0.0
        self.prev_v=0.0
        self.prev_phi=0.0

    def timer_callback(self):
        current_time=self.get_clock().now()
        dt=(current_time-self.last_time).nanoseconds/1e9

        if dt<=0.0 or dt>0.1:
            self.last_time=current_time
            return
        
        self.last_time=current_time

       
        x_dot = self.v * math.cos(self.theta)
        y_dot = self.v * math.sin(self.theta)
        theta_dot = self.v / self.L * math.tan(self.phi)
        self.x += 0.5 * (x_dot + self.prev_x_dot) * dt
        self.y += 0.5 * (y_dot + self.prev_y_dot) * dt
        self.theta+=0.5*(theta_dot+self.prev_theta_dot)*dt
        self.get_logger().info(f"x = {self.x:.3f}  y = {self.y:.3f}  theta = {self.theta:.3f}")
        
        #NORMALIZACJA
        self.theta=math.atan2(math.sin(self.theta), math.cos(self.theta))

        #ZAPAMIĘTYWANIE POPRZEDNICH WARTOŚCI
        self.prev_x_dot=x_dot
        self.prev_y_dot=y_dot
        self.prev_theta_dot=theta_dot
        self.prev_v=self.v
        self.prev_phi=self.phi

        #TRANSFORMACJA TF
        t=TransformStamped()
        t.header.stamp=current_time.to_msg()
        t.header.frame_id='odom'
        t.child_frame_id='base_link'

        t.transform.translation.x=self.x
        t.transform.translation.y=self.y
        t.transform.translation.z=0.0

        q=quaternion_from_euler(0,0,self.theta)


        t.transform.rotation.x=q[0] 
        t.transform.rotation.y=q[1] 
        t.transform.rotation.z=q[2]     
        t.transform.rotation.w=q[3] 
        self.tf_broadcaster.sendTransform(t)


        #PUBLIKACJA ODOMETRII
        
        ##META DANE
        odom_msg=Odometry()
        odom_msg.header.stamp=current_time.to_msg()
        odom_msg.header.frame_id='odom'
        odom_msg.child_frame_id='base_link'

        ##POZYCJA
        odom_msg.pose.pose.position.x=self.x    
        odom_msg.pose.pose.position.y=self.y
        odom_msg.pose.pose.position.z=0.0
        odom_msg.pose.pose.orientation.x=q[0]
        odom_msg.pose.pose.orientation.y=q[1]
        odom_msg.pose.pose.orientation.z=q[2]
        odom_msg.pose.pose.orientation.w=q[3]

        ##PREDKOŚĆ
        odom_msg.twist.twist.linear.x=self.v*math.cos(self.theta)
        odom_msg.twist.twist.linear.y=self.v*math.sin(self.theta)
        odom_msg.twist.twist.linear.z=0.0
        
        ##KĄT SKRĘTU
        odom_msg.twist.twist.angular.x=0.0
        odom_msg.twist.twist.angular.y=0.0
        odom_msg.twist.twist.angular.z=theta_dot
       
        
        self.odom_publisher.publish(odom_msg)


def main(args=None):
    rclpy.init(args=args)
    node = OdometryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()