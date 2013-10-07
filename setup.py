from setuptools import setup, find_packages

setup(
    name='mediagoblin_picscout',
    author='Artem Popov (Commons Machinery)',
    author_email='artfwo@commonsmachinery.se',
    version='0.1',
    packages=['mediagoblin_picscout'],
    include_package_data=True,
    license='AGPLv3',
    install_requires=['requests'],
)
