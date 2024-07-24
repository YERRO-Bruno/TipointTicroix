cd /etc/easypanel/projects/tipointticroix/tipointticroix/code
echo "Cleaning npm cache..."
npm cache clean --force

echo "Removing node_modules..."
rm -rf node_modules

echo "Installing dependencies..."
npm install

systemctl daemon-reload
systemctl enable monservice.service
systemctl restart monservice.service
echo "All done!"