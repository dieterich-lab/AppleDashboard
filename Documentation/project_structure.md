Apple Watch Dashboard
=======================

Project Structure
-----------------
This is a description of the project structure

The project contains the following directories:
0. `AppleDashboard`
1. `apps`
2. `assets`
3. `AppleWatch`
4. `Comparison`
5. `ECG_analyze`
6. `Workout`
7. `dataset_examples`
8. `documentation`
9. `import`
10. `modules`
11. `scripts`

AppleDashboard
---------------

This is the main directory of the app. It contains:
- `app.py` file which is the main app file.
- `db.py`file contains a function to connect to the database.
- `index.py` loads different apps/tabs from different urls.

More about Multi-Page apps with Plotly you can find here https://dash.plotly.com/urls.  

The directory contains also `docker-compose.yml` and `Dockerfile` for building docker image for application. The `docker-compose.yml` is a tool for
defining and running multi-container Docker application, more details https://docs.docker.com/compose/. In our case docker application consists container for database
and for web frontend. Docker build image by reading the instructions from a `Dockerfile`, more details https://docs.docker.com/engine/reference/builder/.

Pipfile specify packages requirements for our application. This file contain all necessary libraries for application working. If we need some new library for working
application pipfile need to be update accordingly.

`AppleDashboard/apps`
---------------------

This directory contains apps/tabs with layout and callbacks for each app/tab:
- `AppleWatch.py`
- `Comparison.py`
- `ECG.py`
- `Workouts.py`

This files have to be imported to `index.py`

A separate folder with the same name is created for each application with additional files/functions for calculations 
and chart creation.


`AppleDashboard/assets`
-----------------------

Contains static files, e.g. external js libraries, images or css
More  about assets you can find here https://dash.plotly.com/dash-enterprise/static-assets.

`AppleDashboard/AppleWatch`
---------------------------

This directory contains files with functions to create graphs and calculations for the AppleWatch tab.
These files must be imported into `AppleWatch.py`. 

`AppleDashboard/Comparison`
---------------------------

This directory contains files with functions to create graphs and calculations for the Comparison tab.
These files must be imported into `Comparison.py`. 

`AppleDashboard/ECG_analyze`
----------------------------

This directory contains files with functions to create graphs and calculations for the ECG tab.
These files must be imported into `ECG.py`. 

`AppleDashboard/Workout`
------------------------

This directory contains files with functions to create graphs and calculations for the Workout tab.
These files must be imported into `Workouts.py`. 

`AppleDashboard/modules`
------------------------

 This directory contains files for creating a database, importing data into a database and querying data from database into an application.


`AppleDashboard/scripts`
------------------------

This directory contain start.sh file (Bourne shell script). The start.sh file contain commands which export 
database environmental variables and flask environmental variables and command for running flask application for developers.  

`AppleDashboard/dataset_examples`
---------------------------------

The directory contains example files. The files with data in import folder should look like example files. 

`AppleDashboard/import`
------------------------

This folder should contain data files that will be imported into the application. 
These files should look like sample files in the `dataset_examples` directory. 

`AppleDashboard/documentation`
------------------------------

The directory contains documentation files related to the project.
This is documentation for the developers, not for the end users. Therefor, all the technical details regarding 
implementation should be documented here. Each file contains a small piece of information. 
It is again *STRONGLY* recommended to separate the documentation into multiple files and do not use one for everything.

