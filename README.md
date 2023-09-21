YOLOv7 ROS with Docker
======================

MRK : Webcam demo に追記

This ROS package wraps the [Official YOLOv7](https://github.com/WongKinYiu/yolov7) repo. Further, [`nvidia-docker`](https://github.com/NVIDIA/nvidia-docker) is used to build an image with all the necessary YOLOv7 dependencies. Then, [`docker compose`](https://docs.docker.com/compose/install/) can be used to create a container to launch a ROS node. Note that the `docker-compose.yml` file shares the container network with the host network---thus, the node will be able to communicate with other ROS nodes on the host machine.

**Tested on:**
- Docker version 23.0.0, build e92dd87
- NVIDIA Container Runtime Hook version 1.12.0, commit: 62bd015475656ef795cb0d59cc4030a6bd4a9526
- NVIDIA GTX 1070 8GB
- Ubuntu 20.04 / ROS Noetic

## Getting Started

Install `docker`, `docker-compose`, `nvidia-docker` (i.e., `nvidia-container-toolkit`). Note that you do not need CUDA installed on your host machine, but you do need an NVIDIA driver installed on the host for your particular NVIDIA GPU.


```bash
$ git clone --recurse-submodules https://github.com/kosuke-mr4/demo_yolov7_ros # get YOLOv7 submodule
$ cd demo_yolov7_ros
$ docker compose build
$ docker compose up
```


## Webcam demo

0. ホストPCにROS Noeticをインストールします
1. Install your favorite ROS web camera package. We will use [`usb_cam`](http://wiki.ros.org/usb_cam): `sudo apt install ros-noetic-usb-cam`.
2. Start a `roscore`.
3. Start the USB camera (with remapping): `rosrun usb_cam usb_cam_node usb_cam/image_raw:=image_raw`．この際 `unable to decode APP fields: Invalid data found when processing input` という表示が出ますが問題ないです．
4. Start `yolov7_ros` via `docker compose up`
5. コンテナ内で `Rviz`　を起動します(なければインストール) ．再インストールが必要との旨のエラーが出た場合は，ホストPCで`xhost +local:docker`を行ってから再度試してください．
7. Rvizから add -> by topic -> image_dets/Image で推定結果を追加した映像を確認できます．


### Credits

- [Official YOLOv7](https://github.com/WongKinYiu/yolov7)
- [lukazso/yolov7-ros](https://github.com/lukazso/yolov7-ros)