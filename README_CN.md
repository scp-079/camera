## 背景

1. 通过 USB 摄像头连接外接屏幕的树莓派。
2. 通过 motion 在屏幕上显示视频监控，并利用本程序搭建的机器人将 motion 检测到的动作视频片段上传到 Telegram 的频道上。
3. 机器人上传完毕视频后自动删除本地文件。
4. 机器人可接收搭建者发送的语音消息，并通过树莓派连接的扬声器播放。

## 说明

本教程仅限于使用基于 raspbian 系统的树莓派上。

默认用户为 `pi` 。

以支持 UVC 协议的 USB 摄像头为例。

## 安装 motion

```bash 
sudo apt update 
sudo apt install build-essential vim git python3-venv motion -y 
```

## 修改配置文件

```bash 
sudo vim /etc/default/motion
```

做如下修改：

```bash /etc/default/motion
start_motion_daemon=yes
``` 

```bash 
sudo vim /etc/motion/motion.conf 
```

做出如下修改（仅显示需要修改的对应的行）：

```bash /etc/motion/motion.conf
daemon on 
width 640
height 480
framerate 100
target_dir /home/pi/motion/tmp
stream_maxrate 200
```

## 创建文件夹

```bash 
mkdir -p ~/motion/tmp 
sudo chown -R motion:motion ~/motion/tmp
```

## 启动服务

```bash 
sudo systemctl enable --now motion
```

## 检查运行状态

树莓派本地访问 `http://localhost:8081` 查看运行状态是否正常。

## 部署机器人

```bash 
cd ~/motion 
git clone https://github.com/scp-079/camera.git
cd ~/motion/camera 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

## 设置机器人

编辑配置文件：

```bash 
mkdir -p ~/motion/camera/data/config
cp ~/motion/camera/examples/config.ini ~/motion/camera/data/config/config.ini 
vim ~/motion/camera/data/config/config.ini 
```

创建服务：

```bash 
mkdir -p ~/.config/systemd/user 
vim ~/.config/systemd/user/camera.service 
``` 

添加如下内容：

```bash ~/.config/systemd/user/camera.service
[Unit]
Description=SCP-079 Telegram Bot Camera Service
After=default.target

[Service]
WorkingDirectory=/home/pi/motion/camera
ExecStart=/home/pi/motion/camera/venv/bin/python -u main.py
Restart=always
RestartSec=15

[Install]
WantedBy=default.target
```

启动服务：

```bash 
systemctl --user enable --now camera
```

