#/usr/bin/python3.7
"""
new_repo script to automate project creation

Usage:
new_repo <name>
new_repo <name> --public
new_repo <name> --cpp

The script defaults to creating a *private* *python* project.

The actions performed are:

- Log into github
- Create new repository called `<user>/<name>`
  (if i run `new_repo blah` it would create github.com/dwillmer/blah.git
- Clone the github repo locally into current_dir/<name>
- Add .gitignore, readme.md, main folder
  (named the same as the project), `tests` folder, .travis-ci.yml
- Add other files specific to the project type
- Add (but not commit) main.py in the <name> directory
- Open main.py in favourite editor (PyCharm).

"""

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from git import Repo
from github import Github
import requests
from tqdm import tqdm


@dataclass
class RepoConfig:
    user: str = ''
    token: str = ''
    public: bool = False
    language: str = 'python'
    name: Optional[str] = None
    github_obj: Optional[Github] = None


def log_into_github(config):
    g = Github(config.token)
    config.github_obj = g


def create_new_repo(config):
    user_id = config.user
    g = config.github_obj
    user = g.get_user(user_id)
    user.create_repo(config.name)


def new_repo_url(config):
    base = Path("https://github.com/")
    return base / config.user / config.name


def clone_repo_locally(config):
    url = new_repo_url(config)
    local = f'./{config.name}'
    Repo.clone_from(str(url), local)


def add_standard_files(config): pass


def add_language_specific_files(config): pass


def open_main_file(config): pass


def composition():
    sequence = [
        log_into_github,
        create_new_repo,
        clone_repo_locally,
        add_standard_files,
        add_language_specific_files,
        open_main_file
    ]
    return sequence


def main(config):
    funcs = tqdm(composition())
    for func in funcs:
        funcs.set_description(func.__name__)
        funcs.refresh()
        func(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str,
                        help='The new project name')
    parser.add_argument('--public', action='store_const',
                        const=True, default=False,
                        help='Make the repo public (default: False)')
    parser.add_argument('--cpp', action='store_const',
                        dest='language', const='cpp', default='python',
                        help='The language for the project (default: python)')

    args = parser.parse_args()

    config = RepoConfig(
        user='dwillmer',
        public=args.public,
        language=args.language,
        name=args.name
    )

    main(config)