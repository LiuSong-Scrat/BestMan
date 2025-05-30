# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : grasp_bowl_on_table_vacuum_gripper.py
# @Time           : 2024-08-03 15:03:52
# @Author         : yk
# @Email          : yangkui1127@gmail.com
# @Description:   : A example to grasp bowl on table use vacuum_gripper (simplified to just display robot model)
"""

import os
import time

from Config import load_config
from Env import Client
from Motion_Planning.Navigation import *
from Robotics_API import Bestman_sim_xarm_with_gripper
from Visualization import Visualizer


def main(filename):

    # Load config
    config_path = "Config/load_xarm.yaml"
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)
    visualizer.draw_axes()

    # Start record
    visualizer.start_record(filename)

    # Init robot
    xarm = Bestman_sim_xarm_with_gripper(client, visualizer, cfg)

    # Interact with arm
    # xarm.sim_interactive_control_arm(10)
    xarm.sim_interactive_control_eef(20)

    # client.wait(10)
    # visualizer.capture_screen("xarm")

    # End record
    visualizer.end_record()

    # disconnect from server
    client.wait(5)
    client.disconnect()


if __name__ == "__main__":

    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get current file name
    filename = os.path.splitext(os.path.basename(__file__))[0]

    main(filename)
