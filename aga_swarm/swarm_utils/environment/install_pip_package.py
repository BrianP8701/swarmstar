import subprocess
import sys

def install_python_package(package_name):
    """
    Installs a Python package using pip.
    
    Args:
    package_name (str): The name of the package to install.
    """
    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
