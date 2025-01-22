import logging
import os
import shutil
import subprocess
import tempfile

from dotenv import load_dotenv
from dynaconf import Dynaconf

from helpers import clone_repo, process_files, update_if_needed

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    environments=True,
    settings_files=['settings.toml', '.env'],
)


def main():
    local_repo_path = settings.get('LOCAL_REPO_URL', '')
    repo_url = settings.get('REPO_URL', '')
    src_folder = settings.get('SRC_FOLDER', '')
    last_commit_hash = settings.get('LAST_COMMIT_HASH', '')
    second_repo_url = settings.get('REPO_URL_FOR_CHANGELOGS', '')
    save_results_in_repo = settings.get('SAVE_RESULT_IN_REPO', False)
    repo_user = settings.get('GIT_LOGIN', '')
    repo_pass = settings.get('GIT_PASSWORD', '')
    repo_user_changelogs = settings.get('GIT_LOGIN_CHANGELOGS', '')
    repo_password_changelogs = settings.get('GIT_PASSWORD_CHANGELOGS', '')

    if local_repo_path:
        search_dir = os.path.join(local_repo_path, src_folder)
        changelogs_dir = os.path.join(os.getcwd(), "changelogs")
        if os.path.exists(changelogs_dir):
            shutil.rmtree(changelogs_dir)
        os.makedirs(changelogs_dir, exist_ok=True)
        process_files(search_dir, local_repo_path, last_commit_hash, changelogs_dir)
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            clone_repo(repo_url, (repo_user, repo_pass), temp_dir)
            search_dir = os.path.join(temp_dir, src_folder)
            changelogs_dir = os.path.join(os.getcwd(), "changelogs")
            if os.path.exists(changelogs_dir):
                shutil.rmtree(changelogs_dir)
            os.makedirs(changelogs_dir, exist_ok=True)
            process_files(search_dir, temp_dir, last_commit_hash, changelogs_dir)
            shutil.rmtree(temp_dir)

    if save_results_in_repo:
        with tempfile.TemporaryDirectory() as temp_dir_second:
            clone_repo(second_repo_url, (repo_user_changelogs, repo_password_changelogs), temp_dir)
            second_repo_dir = temp_dir_second

            changelogs_dst_dir = os.path.join(second_repo_dir, 'changelogs')
            os.makedirs(changelogs_dst_dir, exist_ok=True)

            updated_files = update_if_needed(changelogs_dir, changelogs_dst_dir)

            if updated_files:
                os.chdir(second_repo_dir)
                subprocess.check_call(['git', 'add', '.'])
                subprocess.check_call(['git', 'commit', '-m', 'Update changelogs with new commits'])
                subprocess.check_call(['git', 'push', 'origin', 'main'])
            else:
                logger.info("No changes in changelogs to update.")


if __name__ == "__main__":
    main()
