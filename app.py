#!/usr/bin/env python2.7

import yaml
import subprocess
import os
import mysql
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument("database")
parser.add_argument("action", nargs='?', default="list")
parser.add_argument("stash_name", default="?!")

args = parser.parse_args()

database = args.database

with open("databases.yml", 'r') as ymlfile:
    databases = yaml.load(ymlfile)

if args.database == "all":
    dbs = databases
else:
    dbs = {}
    for db_name in databases:
        if db_name == args.database:
            dbs[db_name] = databases[db_name]

if dbs is None:
    print('Database doesn\'t exist in config')
    quit()

for db in dbs:
    databasepath = 'stashes/' + db
    stashpath = databasepath + '/' + args.stash_name
    database = dbs[db]

    if args.action == "create":
        if os.path.isfile(stashpath):
            choice = raw_input('Stash '+stashpath+' already exists, continue? (y/n)').lower()
            if choice in "n":
                quit()

        mysqlInstance = mysql.mysql(database)
        output = mysqlInstance.backup()

        if not os.path.exists(databasepath):
            os.makedirs(databasepath)

        stash = open(stashpath, 'w')
        stash.write(output)
        stash.close()

        print 'Stash created'

    if args.action == "list":
        if os.path.isdir(databasepath) == False:
            print 'No stashes for this database'
            quit()

        files = os.listdir(databasepath)
        for file in files:
            print(file)

    if args.action == "view":
        if os.path.isfile(stashpath) is False:
            print 'Stash doesn\'t exist'
            quit()

        stash = open(stashpath, 'r')
        print stash.read()

    if args.action == "apply":
        if os.path.isfile(stashpath) is False:
            print 'Stash doesn\'t exist'
            quit()

        choice = raw_input('Applying stash will overwrite your current database, continue? (y/n)').lower()
        if choice in "n":
            quit()

        mysqlInstance = mysql.mysql(database)
        mysqlInstance.restore(stashpath)

        print 'Stash applied'
