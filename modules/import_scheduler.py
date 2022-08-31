from modules import models, import_data
from configparser import ConfigParser
import os
import sys
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import tzlocal
from os import listdir
from os.path import isfile, join


class ImportSettings:
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
        self.config.set('hashes', 'exports', "")
        self.config.set('hashes', 'json', "")
        self.config.set('hashes', 'electrocardiograms', "")
        self.config.set('hashes', 'date', "")

    def update(self, exports, ecgs_dict, files_json):
        hash_dict_exports = ''
        for i in exports:
            hash_dict_exports += self.get_hash('./import/' + i)

        hash_dict_json = ''
        for i in files_json:
            hash_dict_json += self.get_hash('./import/'+i)

        hash_ecg = 0
        for directory in ecgs_dict:
            number_of_ecg_files = len([f for f in listdir('./import/{}/'.format(directory))
                                       if isfile(join('./import/{}/'.format(directory), f))])
            hash_ecg += number_of_ecg_files

        self.config['hashes']['exports'] = hash_dict_exports
        self.config['hashes']['json'] = hash_dict_json
        self.config['hashes']['electrocardiograms'] = str(hash(hash_ecg))
        self.config['hashes']['date'] = str(datetime.now())

    def save(self):
        with open(self.path, 'w+') as cnfFile:
            self.config.write(cnfFile)

    @staticmethod
    def get_hash(path):
        return os.popen(f"sha512sum {path}").read().split(' ')[0]

    def is_export_files_changed(self, files):
        hash_dict = ''
        for i in files:
            hash_dict += self.get_hash('./import/'+i)
        return self.config['hashes']['exports'] != hash_dict

    def is_json_files_changed(self, files):
        hash_dict_json = ''
        for i in files:
            hash_dict_json += self.get_hash('./import/'+i)
        return self.config['hashes']['json'] != hash_dict_json

    def is_electrocardiogram_changed(self, ecgs_dict):
        hash_ecg = 0
        for directory in ecgs_dict:
            number_of_ecg_files = len([f for f in listdir('./import/{}/'.format(directory))
                                       if isfile(join('./import/{}/'.format(directory), f))])
            hash_ecg += number_of_ecg_files
        return self.config['hashes']['electrocardiograms'] != str(hash(hash_ecg))

    def is_empty(self):
        if self.config['hashes']['exports'] and self.config['hashes']['electrocardiograms']:
            return False
        return True


def start_import(rdb):
    """ Import data from entities and dataset files"""

    settings = ImportSettings()
    print('starting import', datetime.now().strftime('%H:%M:%S'))
    dict_ecg, files, files_json = get_export_files_and_ecg_files()
    print(dict_ecg, files)

    if not files and not dict_ecg and not files_json:
        models.check_if_tables_exists(rdb)
        return print("Could not import to database missing export file", file=sys.stderr)
    elif not settings.is_export_files_changed(files) \
            and not settings.is_electrocardiogram_changed(dict_ecg) and not settings.is_export_files_changed(files):
        return print("Data set not changed", file=sys.stderr)
    else:
        print("Start import data")
        models.drop_tables(rdb)
        models.create_tables(rdb)
        if files:
            import_data.insert_data(rdb, files)
        if dict_ecg:
            import_data.load_ecg_data_to_database(rdb, dict_ecg)
        if files_json:
            import_data.load_json_data_to_database(rdb, files_json)
        import_data.create_tables_type(rdb)
        settings.update(exports=files, ecgs_dict=dict_ecg, files_json=files_json)
        settings.save()
        print("End load data")


def get_export_files_and_ecg_files():
    files_xml, files_json, dict_ecg = [], [], []
    for r, d, f in os.walk('./import'):
        if d:
            dict_ecg = [directories for directories in d if directories.startswith('electrocardiograms')]
        for file in f:
            if '.xml' in file:
                files_xml.append(file)
            elif '.json' in file:
                files_json.append(file)

    return dict_ecg, files_xml, files_json


class Scheduler:
    """
    BackgroundScheduler runs in a thread inside existing application.
    Importing data check the data. Import data every day at 05.05 if the program see any changes.
    """

    def __init__(self, rdb, day_of_week, hour, minute):
        self.bgs = BackgroundScheduler(timezone=str(tzlocal.get_localzone()))
        start_import(rdb)
        self.bgs.add_job(start_import, 'cron', [rdb], day_of_week=day_of_week, hour=hour, minute=minute)

    def start(self):
        self.bgs.start()

    def stop(self):
        print('exit scheduler')
        self.bgs.shutdown()
