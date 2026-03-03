import rclpy
from rclpy.node import Node


class FollowMeNode(Node):

  def __init__(self):
    super().__init__('follow_me_node')
    self.get_logger().info("Follow Me node started.")

  def timer_callback(self):
    pass


def main(args=None):
  rclpy.init(args=args)
  node=FollowMeNode()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()


