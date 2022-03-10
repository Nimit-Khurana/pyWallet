from configparser import ConfigParser
from getpass import getpass


class create_config_section:
    def __init__(self):
        self.config_object = ConfigParser()
        self.config_object.read("config.ini")


    def config_section_db(self):
        if not self.config_object.has_section("DATABASE"):
            print ("Need to setup your MYSQL initials for password wallet.")
            sys_name = input("Enter user for mysql database access> ")
            database = input("Name for creating a database> ")
            password = getpass("database access user's password set when mysql was installed> ")
            self.config_object["DATABASE"] = {
                "host" : "localhost",
                "user" : sys_name,
                "database" : database,
                "password" : password
            }
            print ("Access to MYSQL database for user: '{}' to database: '{}' done!".format(sys_name, database))
            return self.write_to_conf_file(self.config_object)

    def write_to_conf_file(self, conf_obj):
        with open('config.ini', 'w') as conf:
            conf_obj.write(conf)
        return True

    def config_section_dencrypt(self, key):
        if not self.config_object.has_section("DATABASE"):
            self.config_object["DENCRYPT"] = {
                "key" : key.decode("utf-8")
            }
            self.write_to_conf_file(self.config_object)