# install script into /usr/bin

all:
	echo "#!/bin/sh" > scripts/visualize
	echo "$$(pwd)/visualize.py" '$$@' >> scripts/visualize

install:
	cp scripts/visualize /usr/bin/.
	cp man/visualize.1.gz /usr/share/man/man1/.
	yum install python-ply
