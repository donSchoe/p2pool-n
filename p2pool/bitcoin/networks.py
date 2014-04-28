import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack, jsonrpc
from operator import *

def get_tenfivesubsidy(bnHeight):
    if bnHeight == 1:
        nSubsidy = 105000
    elif bnHeight <= 1050:
        nSubsidy = 1.57079632
    elif bnHeight <= 3150:
        nSubsidy = 3.14159265
    elif bnHeight <= 4000:
        nSubsidy = 9.8596
    else:
        nSubsidy = 3.14159265

    return int(nSubsidy * 1000000)

SPASUBSIDY = [ 0, 940, 3492, 6069, 8673, 11304, 13963, 16650, 19366, 22112, 24887, 27694, 30532, 33402, 36305, 39241, 42213, 45219, 48262, 51342, 54459, 57616, 60812, 64050, 67329, 70652, 74018, 77430, 80889, 84396, 87952, 91559, 95218, 98930, 102698, 106523, 110407, 114351, 118358, 122429, 126566, 130773, 135051, 139402, 143830, 148336, 152924, 157597, 162358, 167210, 172157, 177203, 182351, 187607, 192974, 198457, 204062, 209794, 215659, 221663, 227813, 234116, 240581, 247215, 254027, 261028, 268229, 275641, 283276, 291149, 299275, 307671, 316355, 325347, 334672, 344353, 354420, 364904, 375841, 387273, 399246, 411814, 425039, 438994, 453765, 469451, 486176, 504084, 523359, 544224, 566966, 591957, 619690, 650844, 686380, 727739, 777208, 838764, 920291, 1041340, 1281967 ];
def spa_sub(n):
    i, a, b = 0, 1, 100
    if n == 1:
        return 25000000
    if n >= SPASUBSIDY[100]: return 0
    while b >= a:
        i = (a+b)>>1
        if n < SPASUBSIDY[i] and n >= SPASUBSIDY[i-1]:
            break
        if SPASUBSIDY[i] <= n:
            a = i+1
        else:
            b = i-1

    return 101-i

def get_caishensubsidy(bnHeight):
    nSubsidy = 28

    if bnHeight == 0:
        nSubsidy = 1
    elif bnHeight < 2:
        nSubsidy = 560000
    elif bnHeight > 3583630:
        nSubsidy = 1
    elif bnHeight > 2150178:
        nSubsidy = 3
    elif bnHeight > 1075089:
        nSubsidy = 5
    elif bnHeight > 358363:
        nSubsidy = 10

    return int(nSubsidy * 100000000)

def get_subsidy(nCap, nMaxSubsidy, bnTarget):
    bnLowerBound = 0.01
    bnUpperBound = bnSubsidyLimit = nMaxSubsidy
    bnTargetLimit = 0x00000fffff000000000000000000000000000000000000000000000000000000

    while bnLowerBound + 0.01 <= bnUpperBound:
        bnMidValue = (bnLowerBound + bnUpperBound) / 2
        if pow(bnMidValue, nCap) * bnTargetLimit > pow(bnSubsidyLimit, nCap) * bnTarget:
            bnUpperBound = bnMidValue
        else:
            bnLowerBound = bnMidValue

    nSubsidy = round(bnMidValue, 2)

    if nSubsidy > bnMidValue:
        nSubsidy = nSubsidy - 0.01

    return int(nSubsidy * 1000000)

@defer.inlineCallbacks
def check_genesis_block(bitcoind, genesis_block_hash):
    try:
        yield bitcoind.rpc_getblock(genesis_block_hash)
    except jsonrpc.Error_for_code(-5):
        defer.returnValue(False)
    else:
        defer.returnValue(True)

nets = dict(
    bitcoin=math.Object(
        P2P_PREFIX='f9beb4d9'.decode('hex'),
        P2P_PORT=8333,
        ADDRESS_VERSION=0,
        RPC_PORT=8332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            (yield check_genesis_block(bitcoind, '000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f')) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//210000,
        POW_FUNC=data.hash256,
        BLOCK_PERIOD=600, # s
        SYMBOL='BTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Bitcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Bitcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.bitcoin'), 'bitcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='https://blockchain.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='https://blockchain.info/address/',
        TX_EXPLORER_URL_PREFIX='https://blockchain.info/tx/',
        SANE_TARGET_RANGE=(2**256//2**32//1000 - 1, 2**256//2**32 - 1),
        DUMB_SCRYPT_DIFF=1,
        DUST_THRESHOLD=0.001e8,
    ),

    litecoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=9333,
        ADDRESS_VERSION=48,
        RPC_PORT=9332,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'litecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('ltc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='LTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Litecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Litecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.litecoin'), 'litecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.litecoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

    tenfivecoin=math.Object(
        P2P_PREFIX='fabfb5da'.decode('hex'),
        P2P_PORT=10511,
        ADDRESS_VERSION=66,
        RPC_PORT=10510,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'tenfivecoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: get_tenfivesubsidy(height),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=90, # s
        SYMBOL='105',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Tenfivecoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Tenfivecoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.tenfivecoin'), 'tenfivecoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

    vertcoin=math.Object(
        P2P_PREFIX='fabfb5da'.decode('hex'),
        P2P_PORT=5889,
        ADDRESS_VERSION=71,
        RPC_PORT=5888,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'vertcoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=150, # s
        SYMBOL='VTC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Vertcoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Vertcoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.vertcoin'), 'vertcoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.vertcoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    
    gpucoin=math.Object(
        P2P_PREFIX='fbc0b6db'.decode('hex'),
        P2P_PORT=8623,
        ADDRESS_VERSION=38,
        RPC_PORT=9026,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'gpucoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 20000*100000000 >> (height + 1)//250000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='GPUC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'],
            'Gpucoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Gpucoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.gpucoin'), 'gpucoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer2.sancrypto.info/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer2.sancrypto.info/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer2.sancrypto.info/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

    execoin=math.Object(
        P2P_PREFIX='fabfb5da'.decode('hex'),
        P2P_PORT=9989,
        ADDRESS_VERSION=33,
        RPC_PORT=9988,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'execoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 50*100000000 >> (height + 1)//840000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=45, # s
        SYMBOL='EXE',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'],
            'execoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/execoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.execoin'), 'execoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.execoin.net/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.execoin.net/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.execoin.net/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
       
    rotocoin=math.Object(
        P2P_PREFIX='fabfb5da'.decode('hex'),
        P2P_PORT=28820,
        ADDRESS_VERSION=61,
        RPC_PORT=28800,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'rotocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: 2*100000000 >> (height + 1)//18000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=288, # s
        SYMBOL='Rt2',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'],
            'rotocoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/rotocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.rotocoin'), 'rotocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://cryptexplorer.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://cryptexplorer.com/address/',
        TX_EXPLORER_URL_PREFIX='http://cryptexplorer.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),                                                                                                                                                                      

    spaincoin=math.Object(
        P2P_PREFIX='fb149200'.decode('hex'),
        P2P_PORT=11492,
        ADDRESS_VERSION=63,
        RPC_PORT=11491,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'spaincoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: spa_sub(height), 
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=120, # s
        SYMBOL='SPA',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Spaincoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Spaincoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.spaincoin'), 'spaincoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.spaincoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.spaincoin.org/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.spaincoin.org/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

    kimocoin=math.Object(
        P2P_PREFIX='6b696d6f'.decode('hex'),
        P2P_PORT=1889,
        ADDRESS_VERSION=46,
        RPC_PORT=1988,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'kimocoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda h: int(h+1 if h < 100e3 else 100e3-((h-99999)//10e3)*10e3 if h < 150e3 else 50e3-((h+1)-150e3) if h < 195e3 else 5e3)*100000000,
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='KMC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'kimocoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/kimocoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.kimocoin'), 'kimocoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://explorer.kimocoin.com/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://explorer.kimocoin.com/address/',
        TX_EXPLORER_URL_PREFIX='http://explorer.kimocoin.com/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),

    caishen=math.Object(
        P2P_PREFIX='fabfb5da'.decode('hex'),
        P2P_PORT=14260,
        ADDRESS_VERSION=28,
        RPC_PORT=14261,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'caishenaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: get_caishensubsidy(height),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('vtc_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=88, # s
        SYMBOL='CAI',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'Caishen') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/Caishen/') if platform.system() == 'Darwin' else os.path.expanduser('~/.caishen'), 'caishen.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://greekpool.eu:29000/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://greekpool.eu:29000/address/',
        TX_EXPLORER_URL_PREFIX='http://greekpool.eu:29000/tx/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
        DUMB_SCRYPT_DIFF=2**16,
        DUST_THRESHOLD=0.03e8,
    ),
    
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
