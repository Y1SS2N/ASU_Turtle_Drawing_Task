#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32 
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import time
import math

class TurtleCommander(Node):
    def __init__(self):
        super().__init__('TurtleCommander')
        self.subscription = self.create_subscription(
            Int32,
            'ShapeTransmitter',
            self.ShapeDrawer,
            10
        )

        self.vel_publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.position_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.timer = self.create_timer(0.1, self.timer_callback) # Timer to keep the node alive

        self.current_angle = 0.0
        self.current_x = 0.0

        self.get_logger().info("TurtleCommander node has started, waiting for messages...")

    def ShapeDrawer(self, msg):
        self.currnet_shape = msg.data

        if self.currnet_shape == 1:
            self.draw_infinity() # Drawing this shape
        elif self.currnet_shape == 2:
            self.draw_a_star()
        elif self.currnet_shape == 3:
            self.drawHeart()

    def draw_infinity(self):
        twist = Twist()
        
        # Orienting the turtle
        twist.angular.z = 0.45 # Turn the Turtle to start the shape drawing
        self.vel_publisher.publish(twist)
        time.sleep(2) # Wait for 2 seconds to complete the turn

        twist.angular.z = 0.0 # Stop turning
        self.vel_publisher.publish(twist)
        time.sleep(1) # Short pause before moving forward
        #------------------------------------------------------------------

        # Moving towards the first loop
        twist.linear.x = 2.0  # Move the Turtle forward
        self.vel_publisher.publish(twist)
        time.sleep(2) # Move forward for 1 second

        # DRAW THE FIRST LOOP
        twist.linear.x = 3.14     # v = r * omega
        twist.angular.z = -4.0  # angular velocity
        self.vel_publisher.publish(twist)
        time.sleep(3) # Move forward while turning for 4 seconds

        # GO TO THE OTHER SIDE
        twist.angular.z = 0.0 # Stop turning
        twist.linear.x = 3.4  # Stop moving
        self.vel_publisher.publish(twist)
        time.sleep(1) # Short pause before stopping

        # START THE SECOND LOOP OF THE INFINITY SYMBOL
        twist.linear.x = 3.3
        twist.angular.z = 4.0
        self.vel_publisher.publish(twist)
        time.sleep(3) # Move forward while turning for 4 seconds

        # GO TO THE CENTER
        twist.angular.z = 0.0
        twist.linear.x = 1.6
        self.vel_publisher.publish(twist)
        time.sleep(1) # Short pause before stopping
        print('Finished drawing the infinity symbol')
    
    def draw_a_star(self):
        twist = Twist()

        for i in range(5):
            twist.angular.z = 0.0
            twist.linear.x = 2.0
            self.vel_publisher.publish(twist)
            time.sleep(3)

            twist.linear.x = 0.0
            twist.angular.z = -4*math.pi/5
            self.vel_publisher.publish(twist)
            time.sleep(4)
    
    def drawHeart(self):
        twist = Twist()

        # Orienting the turtle 
        twist.angular.z = 1.5708 # Turn the Turtle to start the shape drawing
        self.vel_publisher.publish(twist)
        time.sleep(2) # Wait for 2 seconds to complete the turn

        # the first half of the heart

        # Top-Right of the heart
        twist.linear.x = 4.71
        twist.angular.z = -math.pi
        self.vel_publisher.publish(twist)
        time.sleep(1.5) # Move forward while turning for 1.5 seconds

        # Bottom-Right of the heart
        twist.linear.x = 6.0
        twist.angular.z = -math.pi/3
        self.vel_publisher.publish(twist)
        time.sleep(1.5) # Move forward while turning for 1.5 seconds

        # the second half of the heart

        # Bottom-Left of the heart
        twist.angular.z = -math.pi/3
        twist.linear.x = 0.0
        self.vel_publisher.publish(twist)
        time.sleep(3) # Turn for 3 seconds to face the bottom-left of the

        twist.linear.x = 6.0
        self.vel_publisher.publish(twist)
        time.sleep(1.5) # Move forward while turning for 1.5 seconds

        # Top-Left of the heart
        twist.linear.x = 4.71
        twist.angular.z = -math.pi
        self.vel_publisher.publish(twist)
        time.sleep(1.5) # Move forward while turning for 1.5 seconds

    
    def pose_callback(self, msg):
        self.current_angle = msg.theta
        self.current_x = msg.x

    def timer_callback(self):
        if self.current_x is not None:
            self.get_logger().info(f'Current Angle: {self.current_angle}, Current X: {self.current_x}')


def main(args=None):
    rclpy.init(args=args)

    turtle_commander = TurtleCommander()
    rclpy.spin(turtle_commander)

    rclpy.shutdown()

if __name__ == '__main__':
    main()