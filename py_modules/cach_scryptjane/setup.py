from distutils.core import setup, Extension

yac_scrypt_module = Extension('yac_scrypt',
                               sources = ['scryptmodule.c',
                                          './scrypt-jane/scrypt-jane.c'],
                               include_dirs=['.', './scrypt-jane', './scrypt-jane/code'])

setup (name = 'yac_scrypt',
       version = '1.0',
       description = 'Bindings for scrypt proof of work used by yacoin',
       ext_modules = [yac_scrypt_module])
