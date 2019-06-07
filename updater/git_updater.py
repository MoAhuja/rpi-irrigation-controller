from git import Repo
from git import RemoteProgress
from pydriller import RepositoryMining
from service.utilities.conversion import Conversions
import os

class GitUpdater(RemoteProgress):

    FIELD_DATE = "DATE"
    FIELD_MESSAGE = "MESSAGE"
    FIELD_HASH = "HASH"

    def __init__(self):
        self.repo_dir = os.getcwd()
        self.remote_repo_location = "git@bitbucket.org:MoAhuja/irrigationcontroller.git"
        # parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))

        self.local_repo = Repo(self.repo_dir)
        
        print("Checking if repo is valid!!")
        assert not self.local_repo.bare


    def getHistory(self):
        
        historyList = []

        # Fetch the latest info
        # print("Fetching from remote")
        # self.local_repo.remotes[0].fetch()
        # print("Fetch complete")    
        # Building commit history

        print("Building commit history")
        miner = RepositoryMining(self.remote_repo_location, reversed_order=True)
        for commit in miner.traverse_commits():
            historyDict = {}
            historyDict[GitUpdater.FIELD_DATE] = Conversions.convertRainDelayDateTimeToString(commit.committer_date)
            historyDict[GitUpdater.FIELD_HASH] = commit.hash 
            historyDict[GitUpdater.FIELD_MESSAGE] = commit.msg 
           
            historyList.append(historyDict)
        
        # self.getLocalGitHash()
        
        
        
        return historyList

    def updateToLatest(self):
        print("Updating from development!!")
        return self.local_repo.remotes[0].pull()

    def getLocalGitHash(self):
        return self.local_repo.head.object.hexsha

        
    


        

