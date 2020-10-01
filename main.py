from github import Github
import autopep8
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


number = 0

def main():
    token = os.getenv('GIT_HUB_TOKEN')
    g = Github(token)
    username = os.getenv('GIT_HUB_USERNAME')

    for repo in g.search_repositories("language:Python pugs pushed:>2020-08-28"):
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        print(g.rate_limiting)
        print(g.rate_limiting_resettime)
        analyze_repo(repo)

def analyze_repo(repo):
    global number
    for file_text in get_files_text(repo, ".py"):
        origin = file_text.decoded_content.decode()
        new = autopep8.fix_code(origin)
        if new != origin:
            print("COMMIT fix to file", file_text.path)

def commit_change(repo, file, new_data, commit):
    print(repo.url)
    print("file.path", file.path)
    print("file.sha", file.sha)
    repo.update_file("/" + file.path, commit, new_data, file.sha)


def get_files_text(repo, end):
    end_len = len(end)
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            if len(file_content.path) > end_len:
                file_end = file_content.path[len(file_content.path) - end_len:]
                if file_end == end:
                    yield file_content

if __name__ == '__main__':
    main()
