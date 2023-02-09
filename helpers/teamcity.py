import requests
import json
import time

def reqGet(func):
    def getPath(*args, **kwargs):
        ws = func(*args, **kwargs)
        data = requests.get(ws[1], headers=ws[0].heads)
        return data
    return getPath


class TC:

    url = None
    token = None
    projectId = None
    buildName = None
    service = None
    branch = None

    def __init__(self, url=None, token=None, projectId=None, buildName=None, service=None, branch=None):
        """Constructor"""
        self.url = url
        self.token = token
        self.projectId = projectId
        self.buildName = buildName
        self.service = service
        self.branch = branch
        self.heads = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    def checkTC(self, status=False):
        """
        Get request to Teamcity
        """
        try:
            if requests.get(self.url, headers=self.heads).ok:
                status = True
        except requests.ConnectionError as e:
            print(f"Connection error: {e}")
        except Exception as e:
            print(f"ERROR: e")
        return status

    @reqGet
    def viewProject(self, projectId):
        """
        Getting all settings of project
        """
        return self, "%s/app/rest/projects/id:%s" % (self.url, projectId)

    @reqGet
    def getParameters(self, projectId):
        """
        Getting project parameters
        """
        return self, "%s/app/rest/projects/id:%s/parameters" % (
            self.url, projectId)

    @reqGet
    def getBuildParameters(self, projectId, buildName):
        """
        Getting all parameters of build by name
        """
        return self, "%s/app/rest/buildTypes/id:%s_%s" % (
            self.url, projectId, buildName)

    @reqGet
    def getBuildList(self, projectId, buildName):
        """
        Getting all parameters of build by name
        """
        return self, "%s/app/rest/buildTypes/id:%s_%s/builds/" % (
            self.url, projectId, buildName)

    @reqGet
    def getBuildState(self, builId):
        """
        Getting build status
        """
        return self, "%s/app/rest/buildQueue/id:%s" % (self.url, builId)

    @reqGet
    def getAgents(self, projectId, buildName):
        """
        Getting all agents for build
        """
        return self, "%s/app/rest/agents?locator=compatible:(buildType:(id:%s_%s))" % (
            self.url, projectId, buildName)

    def getBuildStatus(self, builId, service):
        """
        Monitoring for running build 
        """
        status = None
        build = "%s/app/rest/buildQueue/id:%s" % (self.url, builId)
        while status is None:
            req = requests.get(build, headers=self.heads)
            data = req.json()
            if req.ok:
                if data['state'] == "finished":
                    status = data['status']
                    print(f"{service} is {status}, see more {data['webUrl']}")
                    if status == "FAILURE":
                        print(f"-->> ERROR from log: {data['statusText']}")
                    break
            else:
                print("UNKNOWN")
            time.sleep(5)
        return status

    def runCustomBuild(self, projectId, buildName, branch):
        """
        Run custom build
        """
        buildParameters = {
            "personal": "false",
            "branchName": branch,
            "buildType": {
                "id": f"{projectId}_{buildName}"
            },
            "comment": {
                "text": "Build from REST API"
            }
        }

        buildUrl = "%s/app/rest/buildQueue" % (self.url)
        responseData = requests.post(
            buildUrl, data=json.dumps(buildParameters), headers=self.heads)
        return responseData
