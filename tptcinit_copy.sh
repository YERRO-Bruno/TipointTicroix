npm cache clean --force
rm -rf node_modules
npm install
systemctl daemon-reload
systemctl enable monservice.service
systemctl restart monservice.service