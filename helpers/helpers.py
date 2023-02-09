import argparse
import yaml
import os

def get_args():
    parser = argparse.ArgumentParser(
        description="""
        This script create deploy for services by release
        If you want deploy release you should create new release file in Releases directory release-$NAME_YOUR_RELEASE.yml
        then running script
        $ main.py  -e dev -r release-rnX --deploy
        GIT - https://github.com/sergey-show/teamcity-deploy

        create issues https://github.com/sergey-show/teamcity-deploy/issues/new
        """)
    parser.add_argument("-r", "--release", help="release name, filename")
    parser.add_argument("-p", "--project", help="Project")
    parser.add_argument("-e", "--environment", required=True,
                        help="Environments in servicemap")
    parser.add_argument("--deploy", help="Run deploy", action='store_true')
    parser.add_argument(
        "--buildlist", help="View build list of project", action='store_true')
    parser.add_argument(
        "--getparameters", help="View all parameters of project", action='store_true')
    parser.add_argument(
        "--getbuildparameters", help="View all builds", action='store_true')
    parser.add_argument("--view", help="View project", action='store_true')
    return parser.parse_args()

def getFile(filename):
    """
    Get content of yaml file 
    """
    try:
        with open(f'{filename}.yml', 'r') as yml_file:
            data = yaml.load(yml_file, yaml.FullLoader)
    except FileNotFoundError:
        with open(filename, 'r') as yml_file:
            data = yaml.load(yml_file, yaml.FullLoader)
    except Exception as e:
        print(e)
    return data

def joinServices(path):
    getFiles = os.listdir(path)
    services = {}
    for file in getFiles:
        if file.endswith(".yml"):
            with open(f"{path}/{file}", 'r') as yml_file:
                data = yaml.load(yml_file, yaml.FullLoader)
        services.update(data)
    return services

def collectionPrint(applied,failed,skipped):
    if applied != []:
        print(f"Applied for: {applied}")
    if failed != []:
        print(f"Failed for : {failed}")
    if skipped != []:
        print(f"Skipped for : {skipped}")

class TcMappers(object):
    serviceMap = None
    env = None

    def __init__(self, serviceMap, env):
        """Constructor"""
        self.serviceMap = serviceMap
        self.env = env


    def getProjectId(self, project):
        """
        Parser for id and build name for project
        """
        projectId = None
        buidName = None
        try:
            prefix = self.serviceMap[project]
            projectId = prefix['id']
            buidName = prefix['build_name']
        except KeyError as e:
            print(f"{e} not found in servicemap")
        return projectId, buidName

class GetEnv(object):
    cfg = None

    def __init__(self, cfg):
        """Constructor"""
        self.cfg = cfg

    def getToken(self, apiToken=None):
        if self.cfg['teamcity']['api_token'] != "":
            apiToken = self.cfg['teamcity']['api_token']
        elif os.getenv('TC_API_TOKEN') != None:
            apiToken = os.getenv('TC_API_TOKEN')
        else:
            print("""please set api token in config.yml or ENV variable $TC_API_TOKEN""")
        return apiToken

    def getUrl(self, tcUrl=None):
        if self.cfg['teamcity']['url'] != "":
            tcUrl = self.cfg['teamcity']['url']
        elif os.getenv('TC_HOST') != None:
            tcUrl = os.getenv('TC_HOST')
        else:
            print("""
            Teamcity host is undefined in config.yml or ENV variable $TC_HOST
            """)
        return tcUrl

    def checkTime(self, flag = False):
        flag = self.cfg['checkTime']
        return flag