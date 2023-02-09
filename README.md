# This script for automatic deploy

This script can deploy multi components release

For examle, you should deploy 10 or more services via teamcity. You can write one file with services and applying release

```yaml
components:
  MyApp: master
  MyApp1: master
  MyApp2: master
  MyApp3: master
  ...
```

For working you need get API token of teamcity, then next added in file ```config.yml``` for key ```teamcity.api_token``` or you can use env variable ```TC_API_TOKEN```

### All releases stored in "Releases" directory

```yaml
components:
  # Format name of your application and branch or tag
  MyApp: master
```

#### Mapping rule for your service and environment

In directory ```env``` included dirs with you envs. 

file for mapping ```*.yml```, you can use multiple teams design

How parse URL

ex: https://teamcity.local/buildConfiguration/Team_Dev_MyApp_BuildDeploy?mode=builds

where: (id)```Team_Dev_MyApp```_(build_name)```BuildDeploy```

for ex:

> env/dev/project-team1.yml

```yaml
MyApp:
  id: Team_Dev_MyApp
  build_name: BuildDeploy
MyApp1:
  id: Team_Dev_MyApp1
  build_name: Build
```

> env/dev/project-team2.yml

```yaml
TeamApp:
  id: Team_Dev_TeamApp
  build_name: Build
TeamApp1:
  id: Team_Dev_TeamApp1
  build_name: Build
```

Script gets all files amd merged in one dictionary

### Check rule for maintenance window

If your company use maintenance window for deploy you can set boolean value is 'True' in ```config.yml``` for key ```checkTime```
and change your time in ```helpers/checkers.py```

```python
start_time = now.replace(hour=20, minute=0, second=0, microsecond=0) # Your start tMW
end_time = now.replace(hour=23, minute=0, second=0, microsecond=0) # Your end time MW
Msk = now + timedelta(hours=3) # TZ in delta
```

### Running

Running script

```bash
python3 main.py -e DEV -r release-rnX # Validation all url path for running deploy jobs
python3 main.py -e DEV -r release-rnX --deploy # Apply release to environmemnt
```

### in feature 
running one service in cli
set maintenance window time in config

you can create tickets for asuggestions for improvement)) welcome)) 
