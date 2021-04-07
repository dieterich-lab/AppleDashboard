# AppleDashboard
This project provides a dashboard for visualization data from Apple Watch. The tool allow to load and analyze data from 
multiple users at the same time.
It was created to enable faster analysis of longitudinal data from Apple Watch without the need for programming skills.


## Download data from Apple Watch ##
Export "Health data" from Apple watch:
1. Go to Heath app
2. Press user icon<br/>
3. Scroll down to the bottom of Health profile and press on "Export All Health data" <br/>
4. Press on "Export" to confirm that you want export data <br/>
5. Choose the method how you want save or share data <br/>
![](./images/apple_watch.png)

## Setup ##
We highly recommend the setup via docker-compose. The installation via pip is only recommended for developers.

### Docker Setup Instructions ###
Currently setup for deployment and not development

#### Requirements ####
* [Docker-CE](https://docs.docker.com/install/) >= 20.10.2
* [docker-compose](https://docs.docker.com/compose/overview/) >= 1.27.0

#### Usage ####
* `docker-compose up`

### Setup Instructions Development ### 
Not recommended for pure deployment.

#### Requirements ####
* [Python](https://www.python.org/) >= 3.7
* [pipenv](https://docs.pipenv.org/en/latest/) >= 19.2.3
* [Docker-CE](https://docs.docker.com/install/) >= 20.10.2
* [docker-compose](https://docs.docker.com/compose/overview/) >= 1.27.0
* Linux/MacOS

#### Usage ####
* `pipenv install` installs the latest dependencies
* `pipenv shell` enters the virtual environment
* `docker-compose up` necessary for creating container for PostgreSQL database
* `./scripts/start.sh`
* Develop


## Data Import ##
* To add new data, add the `export.xml` files and `electrocardiogram` directories downloaded from iPhone to the `.import` folder.

In case of load data from more than one device, each `export.xml` file and `electrocardiogram` directory should be 
numbered at the end, example:
* `export1.xml`,`export2.xml`,`export3.xml` etc.
* `eclectrocardiogram1`,`electrocardiogram2`,`electrocardiogram3` etc.

To work the files should have the same format as the current example files that are already in the `dataset_examples` directory.
The examples files look like the files downloaded from Apple Watch without any modifications.


