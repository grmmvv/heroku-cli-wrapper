# Python wrapper for Heroku CLI

This python module contains wrapper that allows to automatically install last version of [Allure 2](https://github.com/allure-framework/allure2) framework and make reports.

### Installation
With pip:

`$ pip install git+https://github.com/grmmvv/heroku-cli-wrapper.git

Or with [pipenv](https://pipenv.kennethreitz.org/en/latest/):

`$ pipenv install -e git+https://github.com/grmmvv/heroku-cli-wrapper.git@master#egg=heroku-cli-wrapper`

### Usage

```python

from heroku_cli_wrapper import HerokuCLIWrapper

if __name__ == '__main__':
    heroku_client = HerokuCLIWrapper()
    heroku_client.auth_with_token('HEROKU_API_TOKEN')
    heroku_client.create_app('my-beautiful-app')

```
