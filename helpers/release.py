from helpers.teamcity import TC
from helpers.checkers import ProdTime
from helpers.helpers import collectionPrint, TcMappers
from threading import Thread


class Release(object):

    mapping = None
    deploy = False
    env = None
    servicemap = None
    url = None
    token = None
    checkTime = bool

    def __init__(self, env, mapping, deploy, servicemap, url, token, checkTime):
        """Constructor"""
        self.mapping = mapping
        self.deploy = deploy
        self.env = env
        self.servicemap = servicemap
        self.url = url
        self.token = token
        self.checkTime = checkTime

    def applyRelease(self):
        threads = []
        ready = []
        skipped = []
        applied = []
        failed = []
        pt = ProdTime(self.env)
        tm = TcMappers(self.servicemap, self.env)
        tc = TC(self.url, self.token)

        # Generate builds for services in release file
        try:
            rn = self.mapping['components']
            for service in rn:
                projectId = tm.getProjectId(service)
                if projectId[0] != None:
                    branch = rn[service]
                    check = tc.getBuildParameters(
                        projectId[0], projectId[1])
                    if check.ok:
                        print("%s: ready for deploy with %s branch" %
                              (service, branch))
                        ready.append(service)
                        if self.checkTime == True:
                            toProd = pt.timeValidate()
                        else:
                            toProd = True
                        if self.deploy is True and toProd is True:
                            createBuild = tc.runCustomBuild(
                                projectId[0], projectId[1], branch).json()
                            if createBuild['id']:
                                req = tc.getBuildState(
                                    createBuild['id']).json()
                                if req['state'] in ("running", "queued"):
                                    print(
                                        f"Build is {req['state']}: {service} {createBuild['webUrl']}")
                                    applied.append(service)
                                    thread = Thread(target=tc.getBuildStatus, args=(
                                        createBuild['id'], service))
                                    thread.start()
                                    threads.append(thread)
                                else:
                                    print(
                                        f"Build is not started: {service} { createBuild['webUrl']}")
                                    failed.append(service)
                    else:
                        print("%s: not ready for deploy || >  %s " %
                              (service, check.text))
                        skipped.append(service)
                else:
                    skipped.append(service)

            if self.deploy is True and toProd is False:
                print(
                    f"""-->> For {self.env} is not maintenance window - MW for PROD 20.00-23.00""")

            if self.deploy is False and ready != []:
                print(f"Ready for deploy: {ready}")
                print(f"""For deploy services, you must be use '--deploy' parameter""")
            
            if threads != []:
                print("Please wait for finished all running builds")
                for thread in threads:
                    thread.join()
                collectionPrint(applied, failed, skipped)
        except KeyError:
            print('Syntax of release file is wrong')

