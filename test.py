from github import Github
import time
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()
# todo:
# make tests
# clean the exixing code
# module that save rp repos
# logs
# better search (by time or shit)
# max reqwest per hour
# make profile for the bot

g = Github(os.getenv('GIT_HUB_TOKEN'))
user_name = os.getenv('GIT_HUB_USERNAME')

class Change:
    def __init__(self, file, commit, change):
        self.file = file
        self.commit = commit
        self.change = change

def make_pr(repo_path: str, title: str, body: str, changes: List[Change]):
    if len(changes) < 1:
        return
    origin_repo = g.get_repo(repo_path)
    github_user = g.get_user()
    myfork = github_user.create_fork(origin_repo)

    for change in changes:
        while True:
            try:
                file = myfork.get_contents(change.file)
                break
            # TODO: check loop with real exception
            except Exception as e:
                print(e)
                time.sleep(3)

        myfork.update_file(change.file, change.commit, change.change, file.sha)

    # TODO get the master branch name (maybe it not named "master")
    # '{}'.format(origin_repo.master_branch), '{}:{}'.format(user_name, myfork.master_branch)
    origin_repo.create_pull(title, body, '{}'.format("master"), '{}:{}'.format(user_name, "master"), True)
    return True

changes = []
changes.append(Change("README.md", "make a test file", "Test context"))
make_pr("jacobggman/videos", "TEST PR2", "this is a test pr", changes)
