# Backend Change Logger

## Project Description

**Backend Change Logger** is a tool for automatically collecting changes from repositories and maintaining change logs. It analyzes commits, extracts information about code modifications, and records them in log files.

### Key Features:

- Automatic collection of changes from Git repositories
- Creation and updating of log files
- Support for multiple projects and services
- Flexible configuration via configuration files

## Installation and Setup

### Requirements

- Python 3.10+
- Poetry (for dependency management)
- Access to Git repositories

## Running the Project

1. Install Poetry using pip:
   ```bash
   pip install poetry
   ```
2. Start the virtual environment:
   ```bash
   poetry shell
   ```
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Set environment variables:
   Example for MacOS and Linux:

   ```sh
   export DYNACONF_GIT_LOGIN=<Git repository login for fetching information>
   export DYNACONF_GIT_PASSWORD=<Git repository password for fetching information>
   export DYNACONF_GIT_LOGIN_CHANGELOGS=<Git repository login for pushing changelogs>
   export DYNACONF_GIT_PASSWORD_CHANGELOGS=<Git repository password for pushing changelogs>
   export DYNACONF_REPO_URL=<Git repository URL>
   export DYNACONF_SRC_FOLDER=<Repository folder where the script is executed>
   export DYNACONF_SAVE_RESULT_IN_REPO=<Parameter to save changelogs to a remote repository. True to save, False otherwise. Default is False>
   export DYNACONF_REPO_URL_FOR_CHANGELOGS=<Git repository URL for pushing changelogs>
   export DYNACONF_SRC_FOLDER_FOR_CHANGELOGS=<Folder in the remote repository where changelogs will be stored. Default is 'changelogs'>
   export DYNACONF_LAST_COMMIT_HASH=<Commit hash from which git log should start. If not set, all commits are considered>
   export DYNACONF_LOCAL_REPO_PATH=<Absolute path to the local repository. If not set, the script works with the remote repository>
   ```

   Example for Windows:

   ```sh
   setx DYNACONF_GIT_LOGIN "<Git repository login for fetching information>"
   setx DYNACONF_GIT_PASSWORD "<Git repository password for fetching information>"
   setx DYNACONF_GIT_LOGIN_CHANGELOGS "<Git repository login for pushing changelogs>"
   setx DYNACONF_GIT_PASSWORD_CHANGELOGS "<Git repository password for pushing changelogs>"
   setx DYNACONF_REPO_URL "<Git repository URL>"
   setx DYNACONF_SRC_FOLDER "<Repository folder where the script is executed>"
   setx DYNACONF_SAVE_RESULT_IN_REPO "<Parameter to save changelogs to a remote repository. True to save, False otherwise. Default is False>"
   setx DYNACONF_REPO_URL_FOR_CHANGELOGS "<Git repository URL for pushing changelogs>"
   setx DYNACONF_SRC_FOLDER_FOR_CHANGELOGS "<Folder in the remote repository where changelogs will be stored. Default is 'changelogs'>"
   setx DYNACONF_LAST_COMMIT_HASH "<Commit hash from which git log should start. If not set, all commits are considered>"
   setx DYNACONF_LOCAL_REPO_PATH "<Absolute path to the local repository. If not set, the script works with the remote repository>"
   ```

   Alternatively, settings can be defined in `settings.toml`:

   ```toml
   [default]
   REPO_URL = "https://git.effectivetrade.ru/EFTR/EFTR2.git"
   SRC_FOLDER = "tools/"
   LOCAL_REPO_PATH = ""
   REPO_URL_FOR_CHANGELOGS = ""
   SRC_FOLDER_FOR_CHANGELOGS = ""
   LAST_COMMIT_HASH = ""
   SAVE_RESULTS_IN_REPO = "False"
   ```

   Authentication credentials for the repository can also be specified in the `.env` file:

   ```sh
   DYNACONF_GIT_LOGIN=<Git repository login for fetching information>
   DYNACONF_GIT_PASSWORD=<Git repository password for fetching information>
   DYNACONF_GIT_LOGIN_CHANGELOGS=<Git repository login for pushing changelogs>
   DYNACONF_GIT_PASSWORD_CHANGELOGS=<Git repository password for pushing changelogs>
   ```

   Environment variables set via `export` or `setx` take precedence over values defined in configuration files.

5. Run the script `get_commits.py`:
   ```bash
   python get_commits.py
   ```

A `changelogs` folder will be created in the project root containing all the commit logs.
