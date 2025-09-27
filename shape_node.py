#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32



class ShapeNode(Node):
    def __init__(self):
        super().__init__('shape_node')
        self.get_logger().info('Shape Node Initialized\n') 
        self.publisher_ = self.create_publisher(Int32, 'ShapeTransmitter', 10) # Create publisher

        chosen_number = self.getANumber() # Get user input

        # Publish the chosen number
        msg = Int32()
        msg.data = chosen_number
        self.publisher_.publish(msg)
        self.get_logger().info(f'Published number: {chosen_number}')
    
    def getANumber(self):

        # Choices
        print("1- Infinity Symbol")
        print("2- A Star")
        print("3- A Heart")

        # Choosing the shape
        the_shape = int(input("\nChoose a shape: "))

        if the_shape == 1:
            return 1
        elif the_shape == 2:
            return 2
        elif the_shape == 3:
            return 3


def main(args=None):
    rclpy.init(args=args)

    shape_node = ShapeNode()
    rclpy.spin(shape_node)

    rclpy.shutdown()

if __name__ == '__main__':
    main()