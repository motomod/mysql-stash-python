import subprocess
import os
import datetime


class mysql:
    def __init__(self, config):
        self.hostname = config["hostname"]
        self.database = config["database"]
        self.username = config["username"]
        self.password = config["password"]
        self.port = config["port"]

    def backup(self):
        command = "export MYSQL_PWD={}; mysqldump -h {} -P {} -u {} {};".format(self.password, self.hostname, self.port, self.username, self.database)
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = process.communicate()

        if err:
            print err

        return output

    def restore(self, stashpath):
        command = "export MYSQL_PWD={}; mysql -h {} -P {} -u {} {} < {};".format(self.password, self.hostname, self.port, self.username, self.database, stashpath)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (output, err) = process.communicate()

        if err:
            print err

        return output
