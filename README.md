P2Pool Server Node software for Scrypt-N coins. Currently supported:
* Vertcoin [VTC]
* GPUCoin [GPUC]
* Execoin [EXE]


Requirements:
-------------------------
Generic:
* Coindaemon >=0.8.5
* Python >=2.6
* Twisted >=10.0.0
* python-argparse (for Python =2.6)

Linux:
* sudo apt-get install python-zope.interface python-twisted python-twisted-web
* sudo apt-get install python-argparse # if on Python 2.6

Windows:
* Install Python 2.7: http://www.python.org/getit/
* Install Twisted: http://twistedmatrix.com/trac/wiki/Downloads
* Install Zope.Interface: http://pypi.python.org/pypi/zope.interface/3.8.0
* Install python win32 api: http://sourceforge.net/projects/pywin32/files/pywin32/Build%20218/
* Install python win32 api wmi wrapper: https://pypi.python.org/pypi/WMI/#downloads
* Unzip the files into C:\Python27\Lib\site-packages


Running P2Pool:
-------------------------
To use P2Pool, you must be running your own local bitcoind. For standard
configurations, using P2Pool should be as simple as:

    python run_p2pool.py

Then run your miner program, connecting to 127.0.0.1 on P2Pool-port with any
username and password.

If you are behind a NAT, you should enable TCP port forwarding on your
router. Forward port 9333 to the host running P2Pool.

Run for additional options.

    python run_p2pool.py --help


Official P2Pool wiki:
-------------------------
https://en.bitcoin.it/wiki/P2Pool


Alternate web front ends:
-------------------------
* https://github.com/hardcpp/P2PoolExtendedFrontEnd
* https://github.com/johndoe75/p2pool-node-status


Notes for Scrypt-N-Coins:
=========================

Requirements:
-------------------------
In order to run P2Pool with the Scrypt-N-Coins, you would need to build and install the
vtc_scrypt module that includes the scrypt proof of work code that Scrypt-N-Coins uses for hashes.

Linux:

    cd py_modules/vertcoin_scrypt
    sudo python setup.py install

Windows (mingw):
* Install MinGW: http://www.mingw.org/wiki/Getting_Started
* Install Python 2.7: http://www.python.org/getit/

In bash type this:

    cd py_modules\vertcoin_scrypt
    C:\Python27\python.exe setup.py build --compile=mingw32 install

Windows (microsoft visual c++)
* Open visual studio console

In bash type this:

    SET VS90COMNTOOLS=%VS110COMNTOOLS%	           # For visual c++ 2012
    SET VS90COMNTOOLS=%VS100COMNTOOLS%             # For visual c++ 2010
    cd py_modules\vertcoin_scrypt
    C:\Python27\python.exe setup.py build --compile=mingw32 install

If you run into an error with unrecognized command line option '-mno-cygwin', see this:
http://stackoverflow.com/q/6034390/1260906


Running P2Pool:
-------------------------
Vertcoin: 
* Run P2Pool with the "--net vertcoin" or "--net vertcoin2" (if you want to connect to 2nd network; use --worker-port 9172 if you want different port for 2nd network workers) option.
* Run your miner program, connecting to 127.0.0.1 on port 9171 (or 9172).

GPUCcoin: 
* Run P2Pool with the "--net gpucoin" option.
* Run your miner program, connecting to 127.0.0.1 on port 9404.

Execoin: 
* Run P2Pool with the "--net execoin" option.
* Run your miner program, connecting to 127.0.0.1 on port 9173.


Sponsors:
-------------------------

Thanks to:
* The Bitcoin Foundation for its generous support of P2Pool.
* The Litecoin Project for its generous donations to P2Pool.
* The Vertcoin Community for its great contribution to P2Pool.
* Everyone contributing to the P2Pool-N repository adding new coins.

