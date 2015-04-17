from setuptools import setup, find_packages

"""
setup file to be used for setting up metrics calculation module
only (i.e. no spatial/network libraries)

This can be used for running standalone metrics calc script or
for use in other libraries that only need metrics calculations
"""

with open('requirements-metrics.txt') as f:
    required = list(f.read().splitlines())

setup(
    name='networkplanner-metrics',
    version='0.9.7',
    description='Network planning metrics calculations',
    url='http://networkplanner.modilabs.org',
    install_requires=required,
    packages=find_packages()
    )
