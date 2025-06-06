# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : move_bowl_from_drawer_to_table.py
# @Time           : 2024-08-03 15:04:58
# @Author         : yk
# @Email          : yangkui1127@gmail.com
# @Description:   : A example to move bowl from drawer to table 
"""


import math
import os

from Config import load_config
from Env import Client
from Motion_Planning.Manipulation.OMPL_Planner import OMPL_Planner
from Motion_Planning.Navigation import *
from Robotics_API import Bestman_sim_ur5e_vacuum_long, Pose
from SLAM import simple_slam
from Visualization import Visualizer


def main(filename):

    # Load config
    config_path = "Config/move_bowl_from_drawer_to_table.yaml"
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)

    # Load scene
    scene_path = "Asset/Scene/Scene/Kitchen_1.json"
    client.create_scene(scene_path)

    # Start record
    # visualizer.start_record(filename)

    # Init robot
    bestman = Bestman_sim_ur5e_vacuum_long(client, visualizer, cfg)

    # Open the drawer
    client.change_object_joint_angle("elementA", 36, 0.4)
    visualizer.draw_aabb_link("elementA", 36)

    # Simple SLAM
    nav_obstacles_bounds = simple_slam(client, bestman, False)

    # Navigate to standing position
    nav_planner = AStarPlanner(
        robot_size=bestman.sim_get_robot_size(),
        obstacles_bounds=nav_obstacles_bounds,
        resolution=0.05,
        enable_plot=False,
    )
    # nav_planner = RRTPlanner(
    #     robot_size = bestman.get_robot_max_size(),
    #     obstacles_bounds = client.get_Nav_obstacles_bounds(),
    #     enable_plot=False
    # )
    standing_pose1 = Pose([2.85, 2.4, 0], [0.0, 0.0, 0.0])
    path = nav_planner.plan(bestman.sim_get_current_base_pose(), standing_pose1)
    bestman.sim_navigate_base(standing_pose1, path, enable_plot=True)

    # Load bowl
    bowl_id = client.load_object(
        "bowl",
        "Asset/Scene/Object/URDF_models/utensil_bowl_blue/model.urdf",
        [3.6, 2.4, 0.6],
        [0.0, 0.0, 0.0],
        1.0,
        False,
    )

    # Init planner
    ompl_planner = OMPL_Planner(bestman, cfg.Planner)

    # Get obstacles info
    ompl_planner.get_obstacles_info()

    # Get rgb image
    # bestman.update_camera()
    # bestman.get_camera_rgb_image(True, True)

    # Planning
    goal = ompl_planner.set_target("bowl")
    start = bestman.sim_get_current_joint_values()
    path = ompl_planner.plan(start, goal)

    # Robot execute, Reach object
    bestman.sim_execute_trajectory(path, enable_plot=True)

    # grasp target object
    bestman.sim_open_vacuum_gripper("bowl")

    # Come back to grasp init pose
    bestman.sim_execute_trajectory(path[::-1], enable_plot=True)

    # Navigation to next pose
    standing_pose2 = Pose([1.0, 2, 0], [0.0, 0.0, -math.pi / 2])
    path = nav_planner.plan(bestman.sim_get_current_base_pose(), standing_pose2)
    bestman.sim_navigate_base(standing_pose2, path, enable_plot=True)

    # Move arm to table
    place_pose = Pose([1.0, 1.0, 1.0], [0.0, math.pi / 2.0, 0.0])
    bestman.sim_move_eef_to_goal_pose(place_pose)

    # place the bowl
    bestman.sim_close_vacuum_gripper()

    # Up arm
    place_pose = Pose([1.0, 1.0, 1.5], [0.0, math.pi / 2.0, 0.0])
    bestman.sim_move_eef_to_goal_pose(place_pose)

    # End record
    # visualizer.end_record()

    # disconnect
    client.wait(10)
    client.disconnect()


if __name__ == "__main__":

    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # get current file name
    filename = os.path.splitext(os.path.basename(__file__))[0]

    main(filename)
