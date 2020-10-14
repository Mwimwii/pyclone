import os
import sysconfig
import platform

PLATFORM = platform.uname().system
package = 'pyclone'

site_packages = sysconfig.get_path('purelib')
RCLONE_DIR_PATH = os.path.join(site_packages, package, 'rclone/')
PREFIX = ''
SHELL = True
if PLATFORM != 'Windows':
    SHELL = False
    PREFIX = './'
RCLONE_PATH = [PREFIX + 'rclone']
CONFIG = os.path.join(RCLONE_DIR_PATH, 'rclone.conf')
