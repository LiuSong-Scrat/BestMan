# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
# @FileName       : load_kitchen.py
# @Time           : 2024-08-03 15:04:25
# @Author         : yk
# @Email          : yangkui1127@gmail.com
# @Description:   : A example to load kitchen
"""

import os

from Config import load_config
from Env import Client
from Visualization import Visualizer


def main():

    # Load config
    config_path = "Config/load_kitchen.yaml"
    cfg = load_config(config_path)
    print(cfg)

    # Init client and visualizer
    client = Client(cfg.Client)
    visualizer = Visualizer(client, cfg.Visualizer)
    visualizer.draw_axes()

    # Load scene
    scene_path = "Asset/Scene/Scene/Kitchen.json"
    scene_path = "Asset/Scene/Scene/kitchen_world/kitchen_lunch_tlp.lisdf"

    client.create_scene(scene_path)

    # client.load_object(
    #     "dishwashers",
    #     "Asset/Scene/Object/assets/dishwashers/urdfs/2.urdf",
    #     [0, 0, 0],
    #     [0, 0, 0, 1],
    #     fixed_base=True,
    #     external_texture=True
    # )
    
    # client.wait(5)
    # visualizer.capture_screen("kitchen_1")

    # disconnect pybullet
    client.wait(100)
    client.disconnect()


if __name__ == "__main__":

    # set work dir to Examples
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    main()
