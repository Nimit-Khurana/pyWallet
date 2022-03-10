import MySQLdb
from db import initiate_database
from security import hashed, DEncrypt
from getpass import getpass
import sys


success = "[SUCCESS] "
fail = "[FAILURE] "
error = "[ERROR] "


class Wallet:
    def __init__(self, user):
        self.walletUser = user.upper()
        getID = initiate_database(comm = "select user from users where username = '{}'".format(self.walletUser), fetch="one")
        
        if getID != None:
            self.user_id = getID[0]  
        else :
            print ("user doesn't exist!!")
            inp = input("Do you want to create user: {}(y/n)?".format(user))
            if inp == "y" or "Y":
                self.create_user()
                sys.exit("User '{}' created successfully!".format(user))
            else:
                sys.exit("New user not registered! Exiting")

    def create_user(self):
        #comm_create_user = "insert into users (username,wallet_pass) values ('{}','{}')".format(self.walletUser, "")
        #ret = initiate_database(comm=comm_create_user)
        #print (ret)
        initiate = MySQLdb.connect("localhost", "richie", "army", "wallet")
        cursor = initiate.cursor()
        command = "insert into users (username) values (%s)"
        value = (
            self.walletUser,
        )
        cursor.execute(command, value)
        initiate.commit()
        initiate.close()
        return success

    def __check_duplicate(self, site, username):
        acc_check = initiate_database(comm= "select site, username from passwords where site = '{}' and username = '{}'".format(site, username), fetch="all")
        return len(acc_check)


    def search(self, site):
        try:
            command = "select * from passwords where site = '{}' and user = {}".format( str(site).upper(), self.user_id)
            ret = initiate_database(comm=command, fetch="all")
            return ret
        except MySQLdb._exceptions.OperationalError as e:
            message = 'Oops! You did not register any "{}" account here.\n'.format(
                inp.upper()
            )
            return sys.exit(message + error + str(e))

    def make_new_entry(self):
        self.acc_hold = self.user_id
        self.account_input = input("site name >")
        self.username_input = input("username >")
        check_ret = self.__check_duplicate(site=self.account_input, username=self.username_input)

        if check_ret > 1:
            return "Account already exists!"
        else:
            self.url = input("url >")
            self.password_input = getpass("password >")
            self.retype_password_input = getpass("retype password >")
            if self.retype_password_input == self.password_input:
                pwd_instance = DEncrypt()
                secure_pwd = pwd_instance.encrypt(self.password_input)

                self.add_info = input("Any additional info.> ")
                initiate = MySQLdb.connect("localhost", "richie", "army", "wallet")
                cursor = initiate.cursor()
                command = "insert into passwords (user, site, username, password, url, additional_info) values(%s,%s,%s,%s,%s,%s)"
                value = (
                    self.acc_hold,
                    self.account_input.upper(),
                    self.username_input,
                    secure_pwd.decode("utf-8"),
                    self.url,
                    self.add_info,
                )
                cursor.execute(command, value)
                initiate.commit()
                initiate.close()
    
                #####acc_dic.update({self.account_input: [self.username_input, self.password_input]})
                message = success + "added {}: {} to your wallet".format(
                    self.acc_hold, self.account_input, self.username_input
                )
                return message
            else:
                message = fail + "password unmatch!"
                return message

    def update(self, **kwargs):
        new_dic = {}
        account = kwargs[acc]
        del kwargs[acc]
        for key,value in kwargs.items():
            if value == "":
                del kwargs[key]
        if "username" and "pwd" in new_dic.keys():
            comm = "update passwords set username = '{0}', password = '{1}' where site='{acc}' and user = {id}".format(kwargs[username], kwargs[pwd], acc=account, id=self.user_id)
        else:
            key = kwargs.keys()[0]
            comm = "update passwords set {0} = '{1}' where site = '{acc}' and user = {id}".format(key, kwargs[key], acc=account, id=self.user_id)
        initiate_database(comm= comm, fetch=None)
        return success + "updated!"

    def delete_record(self):
        self.account_input = input(">Account: ")
        #initiate = MySQLdb.connect("localhost", "richie", "army", "wallet")
        #cursor = initiate.cursor()
        #check if more than one acc exists for same site
        ret = initiate_database(comm= "select * from passwords where site = '{}' and user = {}".format(self.account_input, self.user_id), fetch="all")
        #cursor.execute(command)
        #result = cursor.fetchall()
        if len(ret) > 1:
            username = input("enter username for account: ")
            command = "DELETE FROM passwords WHERE site = '{}' and username = '{}'".format(self.account_input, username)
        else:
            command = "DELETE FROM passwords WHERE site = '{}'".format(self.account_input)
        delete_confirm = initiate_database(comm= command)
        return success + "deleted!!"

    def exportDatatoJson(self):
        myresult = initiate_database(comm="select * from passwords where user = '{}'".format(self.user_id), fetch="all")
        return myresult

    def importDatafromJson(self, json_data):
        pwd_instance = DEncrypt()
        data = json_data
        
        initiate = MySQLdb.connect("localhost", "richie", "army", "wallet")
        cursor = initiate.cursor()
        for i in data:
            pwd = data[i]["password"]
            secure_pwd = pwd_instance.encrypt(pwd)
            
            command = "insert into passwords (user, site, username, password, url, additional_info) values (%s,%s,%s,%s,%s,%s)"
            values = ( self.user_id, i, data[i]["username"], data[i]["url"], secure_pwd, data[i]["additional_info"] )
            cursor.execute(command, values)
            print (success + "Inserted account for {}".format(i) )
            initiate.commit()
        initiate.close()
        return 1