apt-get install python-setuptools python-setuptools-devel gdal gdal-python python-matplotlib zlib proj python-sphinx postgresql-server python-psycopg2 rabbitmq-server
easy_install -U shapely geojson amqplib sqlalchemy psycopg2 pylons recaptcha-client python-cjson scipy
# updatedb
# LIBPROJ_PATH=`locate libproj | grep so.0$`
# LIBPROJ_PATH_LENGTH=${#LIBPROJ_PATH}
# ln -s $LIBPROJ_PATH ${LIBPROJ_PATH:0:$LIBPROJ_PATH_LENGTH-2}
# yum update -y
