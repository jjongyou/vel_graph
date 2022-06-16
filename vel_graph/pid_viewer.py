#!/usr/bin/env python

import rclpy
import time
from rclpy.node import Node
from ichthus_can_msgs.msg import Pid
from std_msgs.msg import Float64
import matplotlib.pyplot as plt


class Vel_graph(Node):

  def __init__(self):
    super().__init__("vel_graph")
    self.ref_subs = self.create_subscription(
      Float64, "ref_vel", self.ref_callback, 10)
    self.whl_spd_subs = self.create_subscription(
      Float64, "cur_vel", self.whl_callback, 10)
    self.start_time = time.time()
    self.whl_spd_axis = []
    self.whl_time_axis = []
    self.ref_vel_axis = []
    self.ref_vel = 0
    self.ref_subs
    self.fig = plt.figure()

  def whl_callback(self, data): 
    arrive_time = time.time()
    time_index = arrive_time - self.start_time
    print(time_index)

    curr_spd = data.data
    self.whl_spd_axis.append(curr_spd)
    self.whl_time_axis.append(time_index)
    self.ref_vel_axis.append(self.ref_vel)
 
    plt.xlabel("Time (Seconds)", fontsize=14)
    plt.ylabel("Wheel Velocity", fontsize=14)
    plt.plot(self.whl_time_axis, self.ref_vel_axis, color="red", label="Ref")
    plt.plot(self.whl_time_axis, self.whl_spd_axis, color="black", label="Vel")
    plt.draw()
    plt.pause(0.2)
    self.fig.clear()

  def ref_callback(self, data):
    self.ref_vel = data.data


def main(args=None):
  rclpy.init(args=args)
  vel_graph = Vel_graph()

  rclpy.spin(vel_graph)

  vel_graph.destroy_node()
  rclpy.shutdown()


if __name__ == "__main__":
  main()
