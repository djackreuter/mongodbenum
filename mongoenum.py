from pymongo import MongoClient
from pprint import pprint
import sys
import cmd

if len(sys.argv) < 2:
        print("Usage: python3 ./mongoenum.py <host:port>")
        sys.exit()


host = sys.argv[1]

client = MongoClient(f"mongodb://{host}/")
cursor = client.list_databases()
print("Available Databases:")
for db in cursor:
    print(db)


class Enumdb(cmd.Cmd):
        intro = 'MongoDB Enum Tool. Type help or ? to list commands.\n'
        prompt = "mongoenum > "
        db = None
        def do_use(self, line):
                self.db = client[line]
                print("Available Collections:")
                pprint(self.db.list_collection_names())

        def do_list(self, sel):
                current_db = self.db
                collection = current_db[sel]
                for item in collection.find():
                        pprint(item)

        def do_list_one(self, sel):
                current_db = self.db
                collection = current_db[sel]
                pprint(collection.find_one())

        def do_collections(self, collections):
                print(f"DB: {self.db.name}")
                pprint(self.db.list_collection_names())

        def do_databases(self, dbs):
                print("Available Databases:")
                cursor = client.list_databases()
                for db in cursor:
                    print(db)

        def do_serverinfo(self, line):
                pprint(client.server_info())

        def do_admininfo(self, line):
                admin = client.admin
                admin_info = admin.command("serverStatus")
                pprint(admin_info)

Enumdb().cmdloop()