apt-get install python-setuptools python-setuptools-devel gdal gdal-python numpy scipy python-matplotlib zlib proj ipython svn python-sphinx postgresql-server python-psycopg2 rabbitmq-server
easy_install -U shapely geojson amqplib sqlalchemy pylons recaptcha-client python-cjson
# updatedb
# LIBPROJ_PATH=`locate libproj | grep so.0$`
# LIBPROJ_PATH_LENGTH=${#LIBPROJ_PATH}
# ln -s $LIBPROJ_PATH ${LIBPROJ_PATH:0:$LIBPROJ_PATH_LENGTH-2}
# yum update -y
