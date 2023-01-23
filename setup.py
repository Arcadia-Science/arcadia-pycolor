from setuptools import setup

setup(
    name='arcadia_pycolor',
    url='https://github.com/Arcadia-Science/arcadia-pycolor',
    author='Dennis Sun',
    author_email='dennis.sun@arcadiascience.com',
    packages=['arcadia_pycolor'],
    install_requires=['numpy', 'matplotlib', 'scipy'],
    version='0.1',
    license='MIT',
    description='An example of a python package from pre-existing code',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)