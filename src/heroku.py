import json
import os
import subprocess


def call_cmd(cmd: str):
    print(f'Calling: {cmd}')
    response = subprocess.run(cmd, shell=True, capture_output=True, universal_newlines=True)
    if response.returncode != 0:
        print(f'Command "{cmd}" returned non-zero exit status {response.returncode}.')
        print(response.stderr)
        exit(response.returncode)
    return response


class HerokuCLIWrapper:
    def __init__(self):
        try:
            call_cmd('heroku --version')
        except SystemExit:
            self._install__heroku_cli()

    def auth_with_token(self, token: str):
        os.environ['HEROKU_API_KEY'] = token

    def _install__heroku_cli(self):
        print('Install Heroku CLI')
        call_cmd('curl https://cli-assets.heroku.com/install.sh | sh')

    def create_app(self, app_name: str = None, team_name: str = None):
        print('Create new heroku app')
        cmd = 'heroku apps:create --json'
        if app_name:
            cmd = f'{cmd} {app_name}'
        if team_name:
            cmd = f'{cmd} -t {team_name}'
        r = call_cmd(cmd)
        data = json.loads(r.stdout)
        return data

    def delete_app(self, app_name: str):
        cmd = f'heroku apps:destroy -a {app_name} -c {app_name}'
        return call_cmd(cmd)

    def get_addons(self, app_name: str):
        print(f'Get addons list from app: {app_name}')
        cmd = f'heroku addons -a {app_name} --json'
        r = call_cmd(cmd)
        data = json.loads(r.stdout)
        return data

    def create_addon(self, app_name, addon):
        print(f'Create addon: {addon} in app: {app_name}')
        cmd = f'heroku addons:create {addon} -a {app_name} --wait --json'
        r = call_cmd(cmd)
        return r

    def restore_backup_from_url(self, app_name: str, source_url: str):
        print(f'Restore DB backup from: {source_url} to app {app_name}')
        cmd = f'heroku pg:backups:restore {source_url} DATABASE_URL -a {app_name} --confirm {app_name}'
        max_attempts = 5
        attempt = 0
        while attempt <= max_attempts:
            r = os.system(cmd)
            if r == 0:
                break
            else:
                print(f'Command "{cmd}" returned non-zero exit status {r}.')
                attempt += 1
        else:
            print(f'Unable to restore reference database to created app in {max_attempts} attempts')
            exit(1)

    def copy_database(self, src_db_name: str, dst_app_name: str, dst_db_name: str, src_app_name: str = None):
        cmd = f'heroku pg:copy {src_db_name} {dst_db_name} --app {dst_app_name} --confirm {dst_app_name}'
        if src_app_name:
            cmd = f'heroku pg:copy {src_app_name}::{src_db_name} {dst_db_name} --app {dst_app_name} --confirm {dst_app_name}'
        call_cmd(cmd)


    def get_env_vars(self, app_name: str):
        print(f'Get environment variables from app: {app_name}')
        cmd = f'heroku config -a {app_name} --json'
        r = call_cmd(cmd)
        data = json.loads(r.stdout)
        return data

    def set_env_vars(self, app_name: str, env_vars_dict: dict):
        print(f'Set environment variables for app: {app_name}')
        addons_data = ''
        for k, v in env_vars_dict.items():
            addons_data += f'{k}="{v}" '
        cmd = f'heroku config:set -a {app_name} {addons_data}'
        r = call_cmd(cmd)
        return r

    def set_remote(self, app_name: str):
        print(f'Add heroku hemote for app: {app_name}')
        cmd = f'heroku git:remote -a {app_name}'
        r = call_cmd(cmd)
        return r

    def add_buildpack(self, app_name: str, buildpack_url: str):
        print(f'Add buildpack: {buildpack_url} to app: {app_name}')
        cmd = f'heroku buildpacks:add {buildpack_url} -a {app_name}'
        r = call_cmd(cmd)
        return r

    def scale_app_dynos(self, app_name: str, dyno_dict: dict):
        dynos_data = ' '.join(f'{k}={v}' for k, v in dyno_dict.items())
        cmd = f'heroku ps:scale -a {app_name} {dynos_data}'
        r = call_cmd(cmd)
        return r

    def restart_app(self, app_name: str):
        cmd = f'heroku ps:restart -a {app_name}'
        r = call_cmd(cmd)
        return r
