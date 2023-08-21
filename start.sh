#!/bin/bash

# 查找 jiujia 进程的 PID
pids=$(pgrep -f '/root/docker/jiujia/main.py')

if [ -n "$pids" ]; then
    # 停止所有 jiujia 进程
    for pid in $pids; do
        kill -9 "$pid"
    done

    # 等待所有 jiujia 进程终止
    for pid in $pids; do
        while ps -p "$pid" > /dev/null; do sleep 1; done
    done

    # 检查所有 jiujia 进程是否已终止
    for pid in $pids; do
        if [ $? -eq 0 ]; then
            echo "Stopped jiujia process with PID $pid."
        else
            echo "Failed to stop jiujia process with PID $pid."
        fi
    done
fi

echo "------------------------------------------------"
export APP_ENV=prod

nohup python3 /root/docker/jiujia/main.py > app.log 2>&1 &
pid=$!

# 等待 jiujia 进程启动
sleep 1

# 检查 jiujia 进程是否已启动
if ps -p "$pid" > /dev/null; then
    echo "Started jiujia service with PID $pid."
else
    echo "Failed to start jiujia service."
fi