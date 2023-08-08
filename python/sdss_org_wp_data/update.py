from os import environ
from os.path import exists, join
from json import load, dump

class Update:

    duplicates = ['x.liu@pku.edu.cn']

    def __init__(self, listname = None, listtype = None, verbose = None):
        self.list = {'name': listname, 'type': listtype} if listname and listtype else None
        self.verbose = verbose
        self.set_wiki_data_dir()
        
    def set_wiki_data_dir(self):
        try: self.wiki_data_dir = environ['WIKI_DATA_DIR']
        except: self.wiki_data_dir = None
        
    def get_checksum(self):
        return None
        
    def set_json(self):
        if self.list and self.wiki_data_dir:
            self.json = join(self.wiki_data_dir, 'members', "%(type)s", "%(name)s", "%(name)s.json") % self.list
            if not exists(self.json):
                print("UPDATE> Nonexistent %s" % self.json)
                self.json = None
            elif self.verbose:  print("UPDATE> Found %s" % self.json)
        else: self.json = None
        
    def set_data_from_json(self):
        if self.json:
            with open(self.json) as json_file: self.data = load(json_file)
        else: self.data = None
        
    def remove_disabled(self):
        self.data = {row for row in self.data if row['reason'] != 'enabled'}
        
    def remove_duplicates(self):
        self.data = {row for row in self.data if row['email'] not in self.duplicates}
        
    def sort_data(self):
        pass
        
    def set_checksum(self):
        self.checksum = None
        
    def export_data_to_json(self):
        pass
        
    def github_commit(self):
        pass
