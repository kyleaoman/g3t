from setuptools import setup

setup(
    name='g3t',
    version='0.1',
    description='Gadget3 read routines & other scripts.',
    url='',
    author='Antonio Ragagnin',
    author_email='antonio.ragagnin@inaf.it',
    license='',
    packages=['g3t'],
    install_requires=['numpy', 'h5py'],
    include_package_data=True,
    zip_safe=False
)
