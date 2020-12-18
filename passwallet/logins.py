import sys
import json
import MySQLdb
from getpass import getpass
from terminaltables import AsciiTable

from dbcredentials import HOST, USER, PASS, DATABASE

success = "[SUCCESS] "
fail = "[FAILURE] "
error = "[ERROR] "


class Wallet:
    def __init__(self, user):
        self.walletUser = user.upper()
        self.db_host = HOST
        self.db_user = USER
        self.db_password = PASS
        self.db_database = DATABASE

    def __execute_db_command(self, db_command, db_value=None, fetchall=False):
        initiate = MySQLdb.connect(
            self.db_host, self.db_user, self.db_password, self.db_database
        )
        cursor = initiate.cursor()
        try:
            cursor.execute(db_command, db_value)
            initiate.commit()
            if fetchall == True:
                fetch_result = cursor.fetchall()
                initiate.close()
                return fetch_result
            else:
                return success
        except MySQLdb._exceptions.OperationalError as e:
            initiate.close()
            return sys.exit(error + "in command" + str(db_command))

    def update(self, **kwargs):
        account = kwargs[acc]
        del kwargs[acc]
        for key, value in kwargs.items():
            if value == "":
                del kwargs[key]
        if "username" and "pwd" in new_dic.keys():
            command = "update passwords set username = '{0}', password = '{1}' where site='{acc}'".format(
                kwargs[username], kwargs[pwd], acc=account
            )
        else:
            key = kwargs.keys()[0]
            command = "update passwords set {0} = '{1}' where site = '{acc}'".format(
                key, kwargs[key], acc=account
            )
        __execute_db_command(command)
        return success + "updated!"

    def search(self):
        print("Enter name of the account")
        inp = input("> ")

        command = "select * from passwords where site = '{}'".format(str(inp).upper())
        myresult = __execute_db_command(db_command=command, fetchall=True)
        return myresult

    def make_new_entry(self):
        self.acc_hold = self.walletUser
        self.account_input = input(">account :")
        self.username_input = input(">username :")
        self.password_input = getpass(">password :")
        self.retype_password_input = getpass(">retype password :")
        if self.retype_password_input == self.password_input:

            command = "insert into passwords (user, site, username, password) values(%s,%s,%s,%s)"
            value = (
                self.acc_hold.upper(),
                self.account_input.upper(),
                self.username_input,
                self.password_input,
            )
            __execute_db_command(db_command=command, db_value=value)

            message = success + "added {}: {} to your wallet".format(
                self.acc_hold, self.account_input, self.username_input
            )
            return message
        else:
            message = fail + "password unmatch! Improve your typing skills."
            return message

    def delete_record(self):
        self.account_input = input(">Account: ")
        # check if more than one acc exists for same site
        check_command = "select * from passwords where site = '{}'".format(self.account_input)
        fetch_result = __execute_db_command(db_command=check_command, fetchall=True)
        
        if len(fetch_result) > 1:
            username = input("enter username for account: ")
            command = (
                "DELETE FROM passwords WHERE site = '{}' and username = '{}'".format(
                    self.account_input, username
                )
            )
        else:
            command = "DELETE FROM passwords WHERE site = '{}'".format(
                self.account_input
            )
        result = __execute_db_command(db_command=command)
        return result + "deleted!!"

    def exportDatatoJson(self):
        command = "select * from passwords where user = '{}'".format(self.walletUser)
        fetch_result = __execute_db_command(db_command=command, fetchall=True)
        return fetch_result

    def importDatafromJson(self, json_data):
        data = json.loads(json_data)

        initiate = MySQLdb.connect(
            self.db_host, self.db_user, self.db_password, self.db_database
        )
        cursor = initiate.cursor()
        for i in data:
            command = "insert into passwords (user, site, username, password) values (%s,%s,%s,%s)"
            values = (self.walletUser, i, data[i]["username"], data[i]["password"])
            cursor.execute(command, values)
            print(success + "Inserted account for {}".format(i))
            initiate.commit()
        initiate.close()
        return success


def tablify(data):
    table_data = [["id", "user", "site", "username", "password"]]
    for d in data:
        table_data.append(list(d))
    table = AsciiTable(table_data)
    return table.table


def intro():
    print("Welcome to your digital wallet!\n")

    print("[PASSWORD HINT] <Your Security Question>: ")
    i = 0
    while i < 3:
        login = getpass("[" + str(i + 1) + "/3 attempts]" + " password> ")
        if login == "YourWalletPassword":
            print(success + "Entered Wallet!")
            user = input("user's name> ")
            wallet_instance = Wallet(user)
            while True:
                print(
                    "*Enter a command to access the features. \
                    \n[g]et the credentials \
                    \n[c]reate a new account entry \
                    \n[u]pdate an existing entry \
                    \n[d]elete an entry \
                    \n[i]mport from json \
                    \n[e]xport to json"
                )

                i = input("> ")
                if i == "g":
                    data_list = wallet_instance.search()
                    print(tablify(data_list))

                elif i == "c":
                    print("Making a new entry!")
                    result = wallet_instance.make_new_entry()
                    print(result)

                elif i == "u":
                    print("press enter if keep unchanged")
                    acc_inp = input("Edit account> ")
                    username_inp = input("Edit username> ")
                    pass_inp = getpass("password>")
                    print(
                        wallet_instance.update(
                            acc=acc_inp, username=username_inp, pwd=pass_inp
                        )
                    )

                elif i == "d":
                    print(wallet_instance.delete_record())

                elif i == "e":
                    json_data = {}
                    data = wallet_instance.exportDatatoJson()
                    for item in data:
                        json_data.update(
                            {item[2]: {"username": item[3], "password": item[4]}}
                        )
                    with open("passwords.txt", "w+") as f:
                        f.write(json.dumps(json_data, indent=4, sort_keys=True))
                        f.close()

                elif i == "i":
                    with open("import.txt", "r") as f:
                        data = wallet_instance.importDatafromJson(f.read())
                    if data is True:
                        print(success + "IMPORTED")
                    else:
                        print(error + "No IMPORT")

                else:
                    message = error + "Wrong input! Exiting..."
                    return sys.exit(message)
        else:
            i += 1
            continue


if __name__ == "__main__":
    intro()