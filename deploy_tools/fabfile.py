from fabric.contrib.files import append, exists, sed
from fabric.api import cd, env, local, run
import random

REPO_URL = 'https://github.com/hjwp/book-example.git'  

def deploy():
    site_folder = f'/home/{env.user}/flirtjar'  
    run(f'mkdir -p {site_folder}')  
    with cd(site_folder):  
        _get_latest_source()
        _update_settings(env.host)  
        _update_virtualenv()
        _update_static_files()
        _update_database()


def _get_latest_source():
    if exists('.git'):  
        run('git fetch')  
    else:
        run(f'git clone {REPO_URL} .')  
    current_commit = local("git log -n 1 --format=%H", capture=True)  
    run(f'git reset --hard {current_commit}')


def _update_settings(site_name):
    pass


def _update_database():
	pass

	
def _update_settings():
	pass
	
	
