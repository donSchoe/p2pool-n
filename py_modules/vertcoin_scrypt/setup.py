from distutils.core import setup, Extension

vtc_scrypt_module = Extension('vtc_scrypt',
                               sources = ['scryptmodule.c',
                                          'scrypt.c'],
                               include_dirs=['.'], extra_compile_args=['-O2'])

setup (name = 'vtc_scrypt',
       version = '1.0',
       description = 'Bindings for scrypt proof of work used by Vertcoin',
       ext_modules = [vtc_scrypt_module])
