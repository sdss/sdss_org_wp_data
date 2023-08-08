from os import environ, utime
from os.path import exists, join
from json import load, dump, dumps
from hashlib import md5

class Update:

    duplicates = ['x.liu@ynu.edu.cn']

    def __init__(self, listname = None, listtype = None, verbose = None):
        self.list = {'name': listname, 'type': listtype} if listname and listtype else None
        self.verbose = verbose
        self.set_json_dir()
        self.set_wiki_data_dir()
        self.set_checksum_file()
        
    def set_json_dir(self):
        try: self.json_dir = environ['SDSS_ORG_WP_DATA_JSON_DIR']
        except: self.json_dir = None

    def set_wiki_data_dir(self):
        try: self.wiki_data_dir = environ['WIKI_DATA_DIR']
        except: self.wiki_data_dir = None
                
    def set_checksum_file(self):
        if self.list and self.json_dir:
            self.checksum_file = join(self.json_dir, "%(name)s.md5") % self.list
            if not exists(self.checksum_file):
                print("UPDATE> Nonexistent %s" % self.checksum_file)
                self.checksum_file = None
            elif self.verbose:  print("UPDATE> Found %s" % self.checksum_file)
        else: self.checksum_file = None
        
    def touch_github_file(self):
        if self.list and self.json_dir:
            self.github_file = join(self.json_dir, "%(name)s.push") % self.list
            with open(self.github_file, 'a'): utime(self.github_file, None)
            if self.verbose: print("UPDATE> Touch %s" % self.github_file)

    def get_checksum(self):
        if self.checksum_file:
            with open(self.checksum_file, 'r') as file: checksum = file.readline()
        else: checksum = None
        return checksum
        
    def set_wiki_json(self):
        if self.list and self.wiki_data_dir:
            self.wiki_json = join(self.wiki_data_dir, 'members', "%(type)s", "%(name)s", "%(name)s.json") % self.list
            if not exists(self.wiki_json):
                print("UPDATE> Nonexistent %s" % self.wiki_json)
                self.wiki_json = None
            elif self.verbose:  print("UPDATE> Found %s" % self.wiki_json)
        else: self.wiki_json = None
        
    def set_json(self):
        if self.list and self.json_dir:
            if exists(self.json_dir):
                self.json = join(self.json_dir, "%(name)s.json") % self.list
            else:
                print("UPDATE> Nonexistent %s" % self.json_dir)
                self.json = None
        else: self.json = None
        
    def set_data_from_json(self):
        if self.wiki_json:
            with open(self.wiki_json) as json_file: self.data = load(json_file)
        else: self.data = None
        
    def remove_disabled(self):
        self.data = [row for row in self.data if row['reason'] == 'enabled']
        
    def remove_duplicates(self):
        self.data = [row for row in self.data if row['email'] not in self.duplicates]
        
    def sort_data(self):
        self.data = sorted(self.data, key=lambda d: d['name'])
        
    def set_checksum(self):
        try: self.checksum = md5(dumps(self.data, ensure_ascii=True).encode('utf-8')).hexdigest()  if self.data else None
        except Exception as e:
            print("UPDATE> %r" % e)
            self.checksum = None
        
    def export_checksum(self):
        if self.checksum and self.checksum_file:
            if self.verbose: print("UPDATE> Export checksum=%r to %s" % (self.checksum, self.checksum_file))
            with open(self.checksum_file, 'w') as file: file.write(self.checksum)
        else: print("UPDATE> Cannot export checksum=%r to %s" % (self.checksum, self.checksum_file))
        
    def set_wiki_json(self):
        if self.list and self.wiki_data_dir:
            self.wiki_json = join(self.wiki_data_dir, 'members', "%(type)s", "%(name)s", "%(name)s.json") % self.list
            if not exists(self.wiki_json):
                print("UPDATE> Nonexistent %s" % self.wiki_json)
                self.wiki_json = None
            elif self.verbose:  print("UPDATE> Found %s" % self.wiki_json)
        else: self.wiki_json = None
        
    def export_data_to_json(self):
        if self.data and self.json:
            if self.verbose: print("UPDATE> Export to %s" % self.json)
            with open(self.json, 'w') as file: dump(self.data, file, indent=4)
        
