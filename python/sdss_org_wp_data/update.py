from os import environ
from os.path import exists, join

class Update:

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
                print("UPDATE> Nonexistent %r" % self.json)
                self.json = None
            elif self.verbose:  print("UPDATE> Found %r" % self.json)
        self.json = None
        
    def set_data_from_json(self):
        if self.json:
            self.data = None
            with open(self.json) as json_file: self.data = load(json_file)
        else: self.data = None
        
    def remove_duplicates(self):
        pass
        
    def sort_data(self):
        pass
        
    def set_checksum(self):
        self.checksum = None
        
    def export_data_to_json(self):
        pass
        
    def github_commit(self):
        pass
