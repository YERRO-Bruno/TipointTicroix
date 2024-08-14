sudo npm cache clean --force
sudo rm -rf node_modules
sudo npm install
sudo systemctl daemon-reload
sudo systemctl enable monservice.service
sudo systemctl restart monservice.service