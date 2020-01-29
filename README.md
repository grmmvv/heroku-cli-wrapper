# Python wrapper for Heroku CLI

Python wrapper around, with automatic system-wide (!) installation [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

### Important

This module makes system-wide installation of Heroky CLI!

You need to setup `HEROKU_API_TOKEN` environment variable before you can start using this!

### Installation
With pip:

`$ pip install git+https://github.com/grmmvv/heroku-cli-wrapper.git`

Or with [pipenv](https://pipenv.kennethreitz.org/en/latest/):

`$ pipenv install -e git+https://github.com/grmmvv/heroku-cli-wrapper.git@master#egg=heroku-cli-wrapper`

### Usage

In case when heroku app is not exist:

```python

from heroku_cli_wrapper import HerokuCLIWrapper

if __name__ == '__main__':
    # If Heroku CLI is not installed then class initialization will install last version
    heroku_client = HerokuCLIWrapper()
    heroku_client.create_app()
    heroku_client.restart_app()

```

In case when need to work with existing app

```python

from heroku_cli_wrapper import HerokuCLIWrapper

if __name__ == '__main__':
    # If Heroku CLI is not installed then class initialization will install last version
    heroku_client = HerokuCLIWrapper('my-beautiful-heroku-app')
    heroku_client.restart_app()

```
