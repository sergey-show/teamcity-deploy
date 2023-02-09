from helpers.teamcity import TC
from helpers.helpers import get_args, getFile, joinServices, TcMappers, GetEnv
from helpers.release import Release
import os

args = get_args()
project = args.project
deploy = args.deploy
buildlist = args.buildlist
getparameters = args.getparameters
getbuildparameters = args.getbuildparameters
env = args.environment.upper()
view = args.view
workdir = os.path.abspath(os.path.dirname(__file__))

try:
    dirFiles = f"{workdir}/env/{env.lower()}"
    serviceMap = joinServices(dirFiles)
except Exception as e:
    print(e)
    quit()

try:
    cfg = getFile(f"{workdir}/config.yml")
except Exception as e:
    print(e)
    quit()

ge = GetEnv(cfg)

TcUrl = ge.getUrl()
TcToken = ge.getToken()
checkTime = ge.checkTime()
tm = TcMappers(serviceMap, env)
tc = TC(TcUrl,TcToken)
if tc.checkTC():
    print("""
    Authentication is Success
    """)
else:
    print("""
    Authentication is failed
    """)
    quit()

if args.release is None:
    try:
        if project:
            projectId = tm.getProjectId(project)
            if projectId[0] is None:
                print("%s: is not exist in servicemap" % project)
            elif view is True:
                req = tc.viewProject(projectId[0])
                print(req.text)
            elif getparameters is True:
                req = tc.getParameters(projectId[0])
                print(req.text)
            elif getbuildparameters is True:
                req = tc.getBuildParameters(projectId[0])
                print(req.text)
            elif buildlist is True:
                req = tc.getBuildList(
                    projectId[0], projectId[1])
                print(req.text)
                ws = req.json()
                print(
                    f"Last build is {ws['build'][0]['status']} with {ws['build'][0]['branchName']}")
            else:
                print("Please use additional parameters for project")
    except NameError as e:
        print(e)
    except Exception as e:
        print(e)
else:
    try:
        mapping = getFile(f"{workdir}/Releases/{args.release}")
        rl = Release(env, mapping, deploy, serviceMap, TcUrl, TcToken, checkTime )
        rl.applyRelease()
    except Exception as e:
        print(e)