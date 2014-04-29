from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    bitcoin=math.Object(
        PARENT=networks.nets['bitcoin'],
        SHARE_PERIOD=30, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=3, # blocks
        IDENTIFIER='fc70035c7a81bc6f'.decode('hex'),
        PREFIX='2472ef181efcd37b'.decode('hex'),
        P2P_PORT=9333,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**32 - 1,
        PERSIST=True,
        WORKER_PORT=9332,
        BOOTSTRAP_ADDRS='forre.st vps.forre.st portals94.ns01.us 54.227.25.14 119.1.96.99 204.10.105.113 76.104.150.248 89.71.151.9 76.114.13.54 72.201.24.106 79.160.2.128 207.244.175.195 168.7.116.243 94.23.215.27 218.54.45.177 5.9.157.150 78.155.217.76 91.154.90.163 173.52.43.124 78.225.49.209 220.135.57.230 169.237.101.193:8335 98.236.74.28 204.19.23.19 98.122.165.84:8338 71.90.88.222 67.168.132.228 193.6.148.18 80.218.174.253 50.43.56.102 68.13.4.106 24.246.31.2 176.31.208.222 1.202.128.218 86.155.135.31 204.237.15.51 5.12.158.126:38007 202.60.68.242 94.19.53.147 65.130.126.82 184.56.21.182 213.112.114.73 218.242.51.246 86.173.200.160 204.15.85.157 37.59.15.50 62.217.124.203 80.87.240.47 198.61.137.12 108.161.134.32 198.154.60.183:10333 71.39.52.34:9335 46.23.72.52:9343 83.143.42.177 192.95.61.149 144.76.17.34 46.65.68.119 188.227.176.66:9336 75.142.155.245:9336 213.67.135.99 76.115.224.177 50.148.193.245 64.53.185.79 80.65.30.137 109.126.14.42 76.84.63.146'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool',
        VERSION_CHECK=lambda v: 50700 <= v < 60000 or 60010 <= v < 60100 or 60400 <= v,
        VERSION_WARNING=lambda v: 'Upgrade Bitcoin to >=0.8.5!' if v < 80500 else None,
    ),

    litecoin=math.Object(
        PARENT=networks.nets['litecoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=3, # blocks
        IDENTIFIER='e037d5b8c6923410'.decode('hex'),
        PREFIX='7208c1a53ef629b0'.decode('hex'),
        P2P_PORT=9338,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=9327,
        BOOTSTRAP_ADDRS='forre.st vps.forre.st liteco.in 95.211.21.103 37.229.117.57 66.228.48.21 180.169.60.179 112.84.181.102 74.214.62.115 209.141.46.154 78.27.191.182 66.187.70.88 88.190.223.96 78.47.242.59 158.182.39.43 180.177.114.80 216.230.232.35 94.231.56.87 62.38.194.17 82.67.167.12 183.129.157.220 71.19.240.182 216.177.81.88 109.106.0.130 113.10.168.210 218.22.102.12 85.69.35.7:54396 201.52.162.167 95.66.173.110:8331 109.65.171.93 95.243.237.90 208.68.17.67 87.103.197.163 101.1.25.211 144.76.17.34 209.99.52.72 198.23.245.250 46.151.21.226 66.43.209.193 59.127.188.231 178.194.42.169 85.10.35.90 110.175.53.212 98.232.129.196 116.228.192.46 94.251.42.75 195.216.115.94 24.49.138.81 61.158.7.36 213.168.187.27 37.59.10.166 72.44.88.49 98.221.44.200 178.19.104.251 87.198.219.221 85.237.59.130:9310 218.16.251.86 151.236.11.119 94.23.215.27 60.190.203.228 176.31.208.222 46.163.105.201 198.84.186.74 199.175.50.102 188.142.102.15 202.191.108.46 125.65.108.19 15.185.107.232 108.161.131.248 188.116.33.39 78.142.148.62 69.42.217.130 213.110.14.23 185.10.51.18 74.71.113.207 77.89.41.253 69.171.153.219 58.210.42.10 174.107.165.198 50.53.105.6 116.213.73.50 83.150.90.211 210.28.136.11 86.58.41.122 70.63.34.88 78.155.217.76 68.193.128.182 198.199.73.40 193.6.148.18 188.177.188.189 83.109.6.82 204.10.105.113 64.91.214.180 46.4.74.44 98.234.11.149 71.189.207.226'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-ltc',
        VERSION_CHECK=lambda v: True,
        VERSION_WARNING=lambda v: 'Upgrade Litecoin to >=0.8.5.1!' if v < 80501 else None,
    ),

    tenfivecoin=math.Object(
        PARENT=networks.nets['tenfivecoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='a06a81c827cab9ff'.decode('hex'),
        PREFIX='7c3614a6bcdcf7ff'.decode('hex'),
        P2P_PORT=10569,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=10579,
        BOOTSTRAP_ADDRS='162.248.163.195'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-tenfive',
        VERSION_CHECK=lambda v: True,
    ),

    vertcoin=math.Object( # --> main net
        PARENT=networks.nets['vertcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='a06a81c827cab973'.decode('hex'),
        PREFIX='7c3614a6bcdcf794'.decode('hex'),
        P2P_PORT=9346,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=9171,
        BOOTSTRAP_ADDRS='q30.qhor.net seed.p2pool.etyd.org vtc.royalminingco.com p2pool.letsmine.it lovok.no-ip.com'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-vtc',
        VERSION_CHECK=lambda v: True,
    ),

    vertcoin2=math.Object( # --> middle hashrate net
        PARENT=networks.nets['vertcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='a06a81c827cab974'.decode('hex'),
        PREFIX='7c3614a6bcdcf795'.decode('hex'),
        P2P_PORT=9347,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=9172,
        BOOTSTRAP_ADDRS='lovok.no-ip.com us-east.p2pools.net us-central.p2pools.net us-west.p2pools.net vert.marcsi.ch'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-vtc',
        VERSION_CHECK=lambda v: True,
    ),
    
    vertcoin3=math.Object( # --> low hashrate net
        PARENT=networks.nets['vertcoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='a06a81c827cab975'.decode('hex'),
        PREFIX='7c3614a6bcdcf796'.decode('hex'),
        P2P_PORT=9348,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=9174,
        BOOTSTRAP_ADDRS='lovok.no-ip.com vtc.cubeconnex.com'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-vtc',
        VERSION_CHECK=lambda v: True,
    ),

    gpucoin=math.Object(
        PARENT=networks.nets['gpucoin'],
        SHARE_PERIOD=10, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=50, # blocks
        IDENTIFIER='a06a81c824bab259'.decode('hex'),
        PREFIX='7c3614a6abe3f884'.decode('hex'),
        P2P_PORT=9451,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=9404,
        BOOTSTRAP_ADDRS='gpu.qemulab.com 96.51.143.9 aforis.mooo.com 96.126.121.117 gpu.crabdance.com p2pool.letsmine.it'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-gpuc',
        VERSION_CHECK=lambda v: True,
    ),

    execoin=math.Object(
        PARENT=networks.nets['execoin'],
        SHARE_PERIOD=10, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=50, # blocks
        IDENTIFIER='657865636f696e65'.decode('hex'),
        PREFIX='65657865636f696e'.decode('hex'),
        P2P_PORT=9986,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=9173,
        BOOTSTRAP_ADDRS='exe.p2pool.info freebtc.eu p2pool.letsmine.it'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-exe',
        VERSION_CHECK=lambda v: True,
    ),
    
    rotocoin=math.Object(
        PARENT=networks.nets['rotocoin'],
        SHARE_PERIOD=30, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='726f746f726f746f'.decode('hex'),
        PREFIX='6f726f746f726f74'.decode('hex'),
        P2P_PORT=7273,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=7274,
        BOOTSTRAP_ADDRS='p2pool.letsmine.it lovok.no-ip.com rt2.hashcrop.info'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-roto',
        VERSION_CHECK=lambda v: True,
    ),

    spaincoin=math.Object(
        PARENT=networks.nets['spaincoin'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='e238d5b8c6931492'.decode('hex'),
        PREFIX='7409c1a53ef71492'.decode('hex'),
        P2P_PORT=26491,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=26490,
        BOOTSTRAP_ADDRS='p2pool2.crunchpool.com p2pool.crunchpool.com spa.boulderbtc.com p2pooleu.cloudapp.net 31.31.72.59 p2pool.letsmine.it lovok.no-ip.com'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-spa',
        VERSION_CHECK=lambda v: True,
        VERSION_WARNING=lambda v: 'Upgrade Spaincoin to >=0.8.8.0!' if v < 80800 else None,
    ),
    
    kimocoin=math.Object(
        PARENT=networks.nets['kimocoin'],
        SHARE_PERIOD=10, # seconds
        CHAIN_LENGTH=24*60*60//30, # shares
        REAL_CHAIN_LENGTH=24*60*60//30, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=15, # blocks
        IDENTIFIER='f8d4d7035c692d35'.decode('hex'),
        PREFIX='de83d31b55d8fd0e'.decode('hex'),
        P2P_PORT=2890,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=True,
        WORKER_PORT=2891,
        BOOTSTRAP_ADDRS='kmc.1js.us'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: True,
    ),

    caishen=math.Object(
        PARENT=networks.nets['caishen'],
        SHARE_PERIOD=15, # seconds
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='a06a81c827cab9e3'.decode('hex'),
        PREFIX='7c3614a6bcdcf7e4'.decode('hex'),
        P2P_PORT=2828,
        MIN_TARGET=4,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=2888,
        BOOTSTRAP_ADDRS='thepool.pw lovok.no-ip.com'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-cai',
        VERSION_CHECK=lambda v: True,
    ),

)
for net_name, net in nets.iteritems():
    net.NAME = net_name
