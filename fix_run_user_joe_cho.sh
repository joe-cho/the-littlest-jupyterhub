#!/bin/bash
sudo mkdir -p /run/user/$(id -u jupyter-joe.cho)
sudo chown jupyter-joe.cho:jupyter-joe.cho /run/user/$(id -u jupyter-joe.cho)
sudo chmod 700 /run/user/$(id -u jupyter-joe.cho)
sudo setenforce 0
