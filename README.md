pylibratometrics
================

Simple script to send psutil (host network/cpu/disk) stats into Librato.

Install
-------

	sudo apt-get install python-pip python-dev -y
	sudo pip install pylibratometrics

Setup 
-------

    export LIBRATO_USER=your@email.com
    export LIBRATO_API=<your api key>

Usage
-------

This will push all metrics to librato. Run this periodically.

	$ pylibratometrics

 A sample crontab config:

	LIBRATO_USER=your@email.com
	LIBRATO_API=de730dcd010d8cs2577cdeaffefdc9e2dc55f68cbca5d3aeca40cc92b2cec73f
	*/5 * * * * pylibratometrics


