from setuptools import setup
from setuptools import find_packages


setup(
    name='python-cloudns',
    version='0.0.2',
    description="ClouDNS API Wrapper",
    author="R Franks",
    author_email='git@rf152.co.uk',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=['python-cloudns'],
    install_requires=['requests']
)