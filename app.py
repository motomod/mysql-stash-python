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

db = None
for db_name in databases:
    if db_name == args.database:
        db = databases[db_name]

if db is None:
    print('Database doesn\'t exist in config')
    quit()

databasepath = 'stashes/' + args.database
stashpath = databasepath + '/' + args.stash_name

if args.action == "create":
    if os.path.isfile(stashpath):
        choice = raw_input('File already exists, continue? (y/n)').lower()
        if choice in "n":
            quit()

    mysql = mysql.mysql(db)
    output = mysql.backup()

    if not os.path.exists(databasepath):
        os.makedirs(databasepath)

    stash = open(stashpath, 'w')
    stash.write(output)
    stash.close()

if args.action == "list":
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

    stash = open(stashpath, 'r')

    mysql = mysql.mysql(db)
    output = mysql.query(stash.read())

    print 'Stash applied'
