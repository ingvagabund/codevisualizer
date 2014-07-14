# install script into /usr/bin

all:
	echo "#!/bin/sh" > scripts/visualize
	echo "$$(pwd)/visualize.py" '$$@' >> scripts/visualize

