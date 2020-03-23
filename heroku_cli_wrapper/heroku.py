import json
import logging
import os

from heroku_cli_wrapper.helper import call_cmd

logging.basicConfig(format='%(message)s', level=logging.INFO)


class HerokuCLIWrapper:
    def __init__(self, app_name: str = None):
        try:
            os.environ['HEROKU_API_KEY']
        except KeyError:
            logging.error('Unauthorized: unable to find "HEROKU_API_KEY" environment variable')
            logging.error('Please make sure that you setup "HEROKU_API_KEY" before use')
            exit(1)
        try:
            call_cmd('heroku --version')
        except SystemExit:
            self._install_heroku_cli()
        self.app_name = app_name
        if self.app_name:
            try:
                self.get_info()
            except SystemExit:
                logging.error(f'Unable to find app with name: "{self.app_name}"')
                exit(1)

    @staticmethod
    def _install_heroku_cli():
        logging.info('Install Heroku CLI')
        call_cmd('curl https://cli-assets.heroku.com/install.sh | sh')

    def get_info(self):
        cmd = f'heroku apps:info -a {self.app_name} --json'
        return json.loads(call_cmd(cmd).stdout)

    def create_app(self, app_name: str = None, team_name: str = None):
        logging.info('Create new heroku app')
        cmd = 'heroku apps:create --json'
        if app_name:
            cmd = f'{cmd} {app_name}'
        if team_name:
            cmd = f'{cmd} -t {team_name}'
        r = call_cmd(cmd)
        data = json.loads(r.stdout)
        self.app_name = data['name']
        return data

    def delete_app(self):
        logging.info(f'Destroy heroku app: "{self.app_name}"')
        cmd = f'heroku apps:destroy -a {self.app_name} -c {self.app_name}'
        return call_cmd(cmd)

    def get_addons(self):
        logging.info(f'Get addons list from app: {self.app_name}')
        cmd = f'heroku addons -a {self.app_name} --json'
        r = call_cmd(cmd)
        return json.loads(r.stdout)

    def create_addon(self, addon):
        logging.info(f'Create addon: {addon} in app: {self.app_name}')
        cmd = f'heroku addons:create {addon} -a {self.app_name} --wait --json'
        return call_cmd(cmd)

    def restore_backup_from_url(self, source_url: str):
        logging.info(f'Restore DB backup from: {source_url} to app {self.app_name}')
        cmd = f'heroku pg:backups:restore {source_url} DATABASE_URL -a {self.app_name} --confirm {self.app_name}'
        max_attempts = 5
        attempt = 0
        while attempt <= max_attempts:
            r = os.system(cmd)
            if r == 0:
                break
            else:
                logging.error(f'Command "{cmd}" returned non-zero exit status {r}.')
                attempt += 1
        else:
            logging.error(f'Unable to restore reference database to created app in {max_attempts} attempts')
            exit(1)

    def copy_database(self, src_db_name: str, dst_db_name: str, src_app_name: str = None):
        cmd = f'heroku pg:copy {src_db_name} {dst_db_name} --app {self.app_name} --confirm {self.app_name}'
        if src_app_name:
            cmd = f'heroku pg:copy {src_app_name}::{src_db_name} {dst_db_name} --app {self.app_name} --confirm {self.app_name}'
        call_cmd(cmd)

    def get_env_vars(self):
        logging.info(f'Get environment variables from app: {self.app_name}')
        cmd = f'heroku config -a {self.app_name} --json'
        r = call_cmd(cmd)
        return json.loads(r.stdout)

    def set_env_vars(self, env_vars_dict: dict):
        logging.info(f'Set environment variables for app: {self.app_name}')
        addons_data = ''
        for k, v in env_vars_dict.items():
            addons_data += f'{k}="{v}" '
        cmd = f'heroku config:set -a {self.app_name} {addons_data}'
        return call_cmd(cmd)

    def set_remote(self):
        logging.info(f'Add heroku remote for app: {self.app_name}')
        cmd = f'heroku git:remote -a {self.app_name}'
        return call_cmd(cmd)

    def add_buildpack(self, buildpack_url: str):
        logging.info(f'Add buildpack: {buildpack_url} to app: {self.app_name}')
        cmd = f'heroku buildpacks:add {buildpack_url} -a {self.app_name}'
        return call_cmd(cmd)

    def scale_app_dynos(self, dyno_dict: dict):
        dynos_data = ' '.join(f'{k}={v}' for k, v in dyno_dict.items())
        cmd = f'heroku ps:scale -a {self.app_name} {dynos_data}'
        return call_cmd(cmd)

    def restart_app(self):
        cmd = f'heroku ps:restart -a {self.app_name}'
        return call_cmd(cmd)

    def get_release_info(self, release_ver=None):
        if not release_ver:
            cmd = f'heroku releases:info -a {self.app_name} --json'
        else:
            cmd = f'heroku releases:info {release_ver} -a {self.app_name} --json'
        return json.loads(call_cmd(cmd).stdout)
