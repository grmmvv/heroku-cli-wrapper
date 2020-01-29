from setuptools import setup

PACKAGE = 'heroku-cli-wrapper'
VERSION = '0.0.5'

setup(
    name=PACKAGE,
    version=VERSION,
    packages=['heroku_cli_wrapper'],
    package_dir={'heroku_cli_wrapper': 'src'},
    url='https://github.com/grmmvv/heroku-cli-wrapper',
    author='Max Gribennikov',
    author_email='grmmvv@gmail.com',
    description='Heroku CLI Wrapper'
)
