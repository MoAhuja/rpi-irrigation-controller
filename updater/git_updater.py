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
        # parentDir = os.path.abspath(os.path.join(currentDir, os.pardir))

        self.repo = Repo(self.repo_dir)
        
        print("Checking if repo is valid!!")
        assert not self.repo.bare


    def getHistory(self):
        
        historyList = []

        miner = RepositoryMining(self.repo_dir, reversed_order=True)
        for commit in miner.traverse_commits():
            historyDict = {}
            historyDict[GitUpdater.FIELD_DATE] = Conversions.convertRainDelayDateTimeToString(commit.committer_date)
            historyDict[GitUpdater.FIELD_HASH] = commit.hash 
            historyDict[GitUpdater.FIELD_MESSAGE] = commit.msg 

            # print("{} - {}".format(commit.committer_date,  commit.msg))
            historyList.append(historyDict)
        
        
        
        return historyList

    def updateToLatest(self):
        print("Updating from development!!")
        return self.repo.remotes[0].pull()


        
    


        

