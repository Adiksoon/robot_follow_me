import rclpy
from rclpy.node import Node
from vision_msgs.msg import Detection2DArray
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


class TargetDetectionNode(Node):

    def __init__(self):
        super().__init__('target_detection_node')
        self.get_logger().info("Target detection node started.")
      #PUBLISHER
        self.detection_pub=self.create_publisher(Detection2DArray, '/target_detection', 10)
       
      #SUBSCRIBER
        self.image_sub=self.create_subscription(Image, '/image_raw', self.image_callback, 10)


      #TYMCZASOWE 
        timer_period = 0.1  # seconds
        self.timer=self.create_timer(timer_period, self.timer_callback)
      #INITIALIZATION CV_BRIDGE
        
        self.bridge=CvBridge()
        


    def timer_callback(self):
       
       #PUBLISHING A DUMMY DETECTION MESSAGE
       detection_msg=Detection2DArray()
       detection_msg.header.stamp = self.get_clock().now().to_msg()
       detection_msg.header.frame_id="camera_frame"
        
       self.detection_pub.publish(detection_msg)

    def image_callback(self, msg):
        self.get_logger().info(f"Received image message. {msg.width}x{msg.height } pixels.")

        
        #CONVERTING ROS IMAGE TO OPENCV IMAGE
      
        cv_image=self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        cv2.imshow("camera", cv_image)
        cv2.waitKey(1)  
        
def main(args=None):
  rclpy.init(args=args)
  node=TargetDetectionNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()