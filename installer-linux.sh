#! /bin/bash

echo "[1/5] Installing python and venv"
sudo apt install python3 python3-pip python3-venv -y

echo "[2/5] Creating the virtual env"
python3 -m venv venv

source env/bin/activate

echo "[3/5] Installing requirements"
pip install -r requirements.txt

echo "[4/5] Setup server information:"
read -p "Server IP: " server_ip
read -p "Is SSL connection [Y/n]? " server_ssl
if [ "$server_ssl" = "y" ] || [ "$server_ssl" = "Y" ] || [ "$server_ssl" = "" ];
then
    server_ssl="true"
    server_port=""
else
    server_ssl="false"
    read -p "Server Port: " server_port
fi

cat > .env <<EOF
SERVER_IP="$server_ip"
SERVER_PORT="$server_port"
SERVER_SSL="$server_ssl"
DEVELOPMENT_MODE="false"
FULLSCREEN="true"
EOF

echo "[5/5] Starting the game"
python3 ./main.py