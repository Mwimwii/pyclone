#!/usr/bin/env python
import re
import sysconfig
import time
import sys
import platform
import zipfile
import shutil
import os
from setuptools import setup, find_packages
import urllib.request
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    
    def run(self):
        install.run(self)
        self.install()

    def install(self):
        # Locations for configs, package installation, etc
        site_packages = sysconfig.get_path("purelib")
        package = 'pyclone'
        package_dir = os.path.join(site_packages, package + '/')
        rclone_zip = os.path.join(package_dir, 'rclone.zip')
        rclone_dir = os.path.join(package_dir, 'rclone')

        is_OS_support, is_Machine_support = self.is_support()

        if not (is_OS_support and is_Machine_support):
            print(f'OS or OS type is not supported. Terminating..')
            sys.exit()

        # Download Rclone
        import time
        # time.sleep(300)
        os.makedirs(rclone_dir, exist_ok=True)
        download_link = f'https://github.com/rclone/rclone/releases/download/v1.53.1/rclone-v1.53.1-{is_OS_support}-{is_Machine_support}.zip'
        urllib.request.urlretrieve(download_link, rclone_zip)
        # Install Rclone in the site packages
        self.install_rclone(rclone_dir, rclone_zip)

        if platform.uname().system != 'Windows':
            self.set_write_permissions(rclone_dir)

    def is_support(self):
        Supported_OS = {'Windows': 'windows', 'Linux': 'linux', 'FreeBSD': 'freebsd',
                        'NetBSD': 'netbsd', 'OpenBSD': 'openbsd', 'Darwin': 'osx'}
        Supported_Machine = {'x86_64': 'amd64',
                             'amd64': 'amd64', 'x86': '386', 'aarch64': 'arm64'}
        system = platform.uname().system
        machine = platform.uname().machine.lower()

        is_OS_support = Supported_OS.get(system, 0)
        is_Machine_support = Supported_Machine.get(machine, 0)
        if 'arm' in machine:
            is_Machine_support = 'arm'
        if (re.match(r'i\d86', machine)):
            is_Machine_support = '386'

        return is_OS_support, is_Machine_support

    def install_rclone(self, rclone_dir, rclone_zip, rclone_conf='rclone.conf'):
        with zipfile.ZipFile(rclone_zip, 'r') as zip_ref:
            for name in zip_ref.namelist()[1:]:
                member = zip_ref.open(name)
                with open(os.path.join(rclone_dir, os.path.basename(name)), 'wb') as outfile:
                    shutil.copyfileobj(member, outfile)
            # Create Rclone config in the same diretory, that will be preferred over the global config
            with open(os.path.join(rclone_dir, rclone_conf), 'w') as create_rclone_config:
                pass

    def set_write_permissions(self, rclone_dir):
        # Set permissions
        # If POSIX then give 777 permission
        for root, dirs, files in os.walk(rclone_dir):
            for d in dirs:
                os.chmod(os.path.join(root, d), 0o777)
            for f in files:
                os.chmod(os.path.join(root, f), 0o777)


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyclone-module',
    version='1.53.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mwimwii/pyclone',

    author='Mwila Nyirongo',
    author_email='mpnyirongo@gmail.com',
    include_package_data=True,
    packages=['pyclone'],
    # packages=find_packages(),
    # py_modules=['pyclone'],
    python_requires='>=3.2',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: SunOS/Solaris',
        'Operating System :: Unix',
        'Topic :: Communications :: File Sharing',
        'Topic :: Internet',
        'Topic :: Utilities',

    ],
    description='Python interface for rclone',
    entry_points={
        'console_scripts': [
            'pyclone=pyclone.cli:execute_from_commandline',
        ],
    },
    license='MIT license',
    keywords='pyclone',
    cmdclass={
        'install': CustomInstallCommand
    },
    extras_require={
        'dev': [
            'pytest>=3.7'
        ]
    },
)
