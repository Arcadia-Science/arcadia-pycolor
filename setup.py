from setuptools import setup
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 9:
    print("This package requires Python version 3.9 or above.")
    sys.exit(1)

setup(
    name='arcadia_pycolor',
    url='https://github.com/Arcadia-Science/arcadia-pycolor',
    author='Dennis Sun',
    author_email='dennis.sun@arcadiascience.com',
    packages=['arcadia_pycolor'],
    install_requires=['numpy', 'matplotlib', 'plotly', 'colorspacious', 'ipython'],
    version='0.3.1',
    license='MIT',
    description="A Python package to distribute Arcadia's color and style guidelines for figures.",
    package_dir={
        "arcadia_pycolor": "arcadia_pycolor"
    },
    package_data={
        "arcadia_pycolor": ["mplstyles/arcadia_basic.mplstyle"]
    },
    include_package_data = True
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
