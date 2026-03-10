import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2

class ImagePublisherNode(Node):
    def __init__(self):
       super().__init__('image_publisher_node')
       self.publisher=self.create_publisher(Image, 'image_raw', 10)
       self.bridge = CvBridge()
       self.image=cv2.imread('test.jpg')
       
       self.timer=self.create_timer(0.1, self.publish_image)

    def publish_image(self):
        msg = self.bridge.cv2_to_imgmsg(self.image, encoding="bgr8")
        self.publisher.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    image_publisher_node = ImagePublisherNode()
    rclpy.spin(image_publisher_node)
    image_publisher_node.destroy_node()
    rclpy.shutdown()
