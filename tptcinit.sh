cd /etc/easypanel/projects/tipointticroix/tipointticroix/code
npm cache clean --force
rm -rf node_modules
npm install
npm install -g forever
forever start server.mjs > tptcinit.log 2>&1