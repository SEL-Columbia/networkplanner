cd
wget http://backpack.invisibleroads.com/scripts.tar.gz
tar xzvf scripts.tar.gz
cd scripts
./setup
cd ..
rm -Rf scripts*
su -c "cd /var/www; mkdir np; chown 134f np; chgrp 134f np"
cd /var/www
git clone git://github.com/invisibleroads/networkplanner.git np
cd np
su -c "rm $HOME/.ssh/known_hosts; ./deployment/dependencies-setup.sh"
cd /var/www/np
./restart cp
