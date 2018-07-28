# MySQL-Stash

MySQL-Stash is a small, light-weight utility for quickly backing up and restoring your MySQL database with data. This has helped me with testing new features during development where I can easily switch between datasets.

## Features
  - Create database stashes
  - Apply database stashes
  - List database stashes
  - View database stashes
  - Multiple database support

## Requirements
  - Python 2.7 (may work on later versions, but untested)
  - Python packages (yaml, subprocess, MySQLDB)

## Installation

### Ubuntu
```sh
$ sudo apt install python2.7 python-pip python-mysqldb libmysqlclient-dev
```

## Configuration

Databases need to be configured before running the app. Databases need to be configured in the databases.yml file in the root directory. See the example for help.

## Usage
```sh
$ python app.py [-h] database [action] stash_name
```
database - The name given to the database in the databases.yml file.
action - 'create'/'apply'/'view'/'list'

#### Creating a stash

To make a stash of the current database with the name of "feature2" you would run:
```sh
$ python app.py exampledb create feature2
```

#### List stashes

View a list of previously created stashes
```sh
$ python app.py exampledb list
```

#### Apply a stash

To apply a created stash you would run:
```sh
$ python app.py exampledb apply feature2
```

#### View a stash

View a previously created stash, doing this will show you the SQL required to recreate your database:
```sh
$ python app.py exampledb view feature2
```

## Thoughts

My original version of this made a system call to 'mysqldump', which saves a lot of work, however I wanted this to be as cross-platform friendly as possible.
