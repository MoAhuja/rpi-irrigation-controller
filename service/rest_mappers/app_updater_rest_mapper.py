from service.rest_mappers.base_rest_mapper import BaseRestMapper
from updater.git_updater import GitUpdater


class AppUpdaterRestMapper(BaseRestMapper):

    def __init__(self):
        self.updater = GitUpdater()

    def getUpdateHistory(self):
        responseData = {}
        commitHistory = self.updater.getHistory()
        responseData["remote_commits"] = commitHistory
        responseData["local_commit"] = self.updater.getLocalGitHash()
        responseData["latest_commit"] = commitHistory[0]["HASH"]
        return self.returnSuccessfulResponse(responseData)
    
    def updateApp(self):
        responseData = {}

        if self.updater.updateToLatest():
            return self.returnSuccessfulResponse()
        

    
    