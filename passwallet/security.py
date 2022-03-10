from configparser import ConfigParser
from cryptography.fernet import Fernet
import bcrypt


def hashed(pwd):
    password = bytes(pwd, encoding='utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed
    
def validate_pwd(pwd):
    if bcrypt.checkpw(password, hashed):
        print("It Matches!")
    else:
        print("It Does not Match :(")


class DEncrypt:
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        info = config_object["DENCRYPT"]
        if not config_object.has_option("DENCRYPT","key"):
            self.key = Fernet.generate_key()

            config_object["DENCRYPT"] =  {
                "key" : self.key.decode("utf-8")
            }
            with open('config.ini', 'w') as conf:
                config_object.write(conf)
        else:
            self.key = bytes(config_object["DENCRYPT"]["key"], encoding="utf-8")
        

    def encrypt(self, pwd):
        self.password = pwd
        p = Fernet(self.key).encrypt(bytes(self.password, encoding="utf-8"))
        return p
    
    
    def decrypt(self, pwd):
        decMessage = Fernet(self.key).decrypt(pwd).decode()
        return (decMessage)