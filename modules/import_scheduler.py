from modules import import_data as id
from configparser import ConfigParser
import os
import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class ImportSettings():
    """
    Class which create file dev_import necessary to import data.
    Inside the file we have two unique cods for files dataset and entities.
    The codes change every time we change anything in the files dataset and entites.
    If the codes has been changed the program loads new data.
    More about th code : https://www.computerhope.com/unix/sha512sum.htm
    """
    def __init__(self):
        self.path = './import/dev_import.ini'
        self.config = ConfigParser()
        self.config.read(self.path)
        if 'hashes' not in self.config.sections():
            self.create()

    def create(self):
        self.config.add_section('hashes')
        self.config.set('hashes', 'dataset', "")
        self.config.set('hashes', 'date', "")

    def update(self, files):
        self.config['hashes']['dataset'] = self.get_hash(files)
        self.config['hashes']['date'] = str(datetime.now())

    def save(self):
        with open(self.path, 'w+') as cnfFile:
            self.config.write(cnfFile)

    def get_hash(self, path):
        return os.popen(f"sha512sum {path}").read() \
            .split(' ')[0]

    def is_dataset_changed(self, files):
        hash = self.get_hash(files)
        return self.config['hashes']['dataset'] != hash

    def is_empty(self):
        if self.config['hashes']['dataset']:
            return False
        return True


def start_import(rdb):
    """ Import data from entities and dataset files"""
    files = []
    directories = []
    settings = ImportSettings()

    print('starting import', datetime.now().strftime('%H:%M:%S'))
    for r, d, f in os.walk('./import'):
        if d:
            directories = d
        for file in f:
            if '.xml' in file:
                files.append(file)

    if not files:
        print(files)
        return print("Could not import to database missing export file", file=sys.stderr)
    elif not settings.is_dataset_changed('./import/'+files[0]):
        return print("Data set not changed", file=sys.stderr)
    else:
        print(files)
        # use function from import_dataset to create tables in database
        print("Start import data")
        id.create_database_data(rdb)
        id.insert_data(rdb, files)
        id.load_ecg_data_to_database(rdb, directories)
        id.alter_tables(rdb)
        path = './import/' + files[0]
        settings.update(files=path)
        settings.save()
        print("End load data")


class Scheduler():
    """
    BackgroundScheduler runs in a thread inside existing application.
    Importing data check the data. Import data every day at 05.05 if the program see any changes.
    """

    def __init__(self,rdb, day_of_week, hour, minute):
        self.bgs = BackgroundScheduler()
        start_import(rdb)
        self.bgs.add_job(start_import,'cron',[rdb], day_of_week=day_of_week, hour=hour, minute=minute)

    def start(self):
        self.bgs.start()

    def stop(self):
        print('exit scheduler')
        self.bgs.shutdown()