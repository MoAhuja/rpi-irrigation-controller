from git import Repo
from git import RemoteProgress
from pydriller import RepositoryMining
import os

class GitUpdater(RemoteProgress):


    def __init__(self):
        self.repo_dir = os.getcwd()
        # parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))

        self.repo = Repo(self.repo_dir)
        
        print("Checking if repo is valid!!")
        assert not self.repo.bare
    
    def getHistory(self):
        print("Get History called")
        self.fetch()


    def getCommits(self):
        miner = RepositoryMining(self.repo_dir)
        for commit in miner.traverse_commits():
            print("{} - {}".format(commit.committer_date,  commit.msg))
    
    # def fetch(self):
    #     for remote in self.repo.remotes:
    #         fetchResult = remote.fetch()

    #         for info in fetchResult:
    #             print(info.ref)
    #             print(info.flags)
    #             print(info.note)

    def updateToLatest(self):
        print("Updating from development!!")
        print(self.repo.remotes[0].pull())


        
    


        

