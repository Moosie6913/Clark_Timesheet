import logging, os, time
import gui
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)


class Encryption:
    # This class handles tasks related to encryption and decryption
    def __init__(self, item, filename):
        self.item = item
        self.filename = filename

    def write(self):
        # Writing and storing credentials to file
        # Returns null
        logging.info('Saving user data...')
        logging.debug('%s key: %s' % (self.filename, self.item))
        path = "./include/data/" + self.filename
        file = open(path, 'wb')
        file.write(self.item)
        file.close()

    def read(self):
        # Reading credentials from stored file
        # Returns (encrypted item)
        logging.info('Loading user data...')
        path = "./include/data/" + self.filename
        file = open(path, 'rb')
        item_encrypt = file.read()
        file.close()
        logging.debug('%s key: %s' % (self.filename, item_encrypt))
        return item_encrypt

    def clear(self, pair):
        # Clears ALL stored data user email and password data
        # Returns null
        try:  # if it exists removed the data
            logging.info('Deleting all stored log in details.')
            os.remove("./include/data/key.key")
            os.remove("./include/data/pair1.pair")
            os.remove("./include/data/pair2.pair")
            os.remove("./include/data/pair3.pair")
            os.remove("./include/data/pair4.pair")
            logging.info('Successfully deleted.')
        except:  # if no data exists or it error proceed
            logging.error('No user data found... Continuing.')
            pass

    def save(self, dual=False):
        # Generates new encryption key and pairs
        # Returns 'Encrypted-(Key,Email,Pass,User2,Pass2)

        # Generate Key
        logging.info('Generating new Key')
        key = Fernet.generate_key()
        file = open('./include/data/key.key', 'wb')
        f = Fernet(key)
        file.write(key)
        file.close()

        # Generate Pairs
        user_encrypt = f.encrypt(input('Enter Worley Email: \n').encode())
        password_encrypt = f.encrypt(input('Enter Worley Password: \n').encode())
        if dual:  # If two log in screens exist
            print('Enter log on details for secondary authentication screen i.e for timesheet log on')
            dual_user_encrypt = f.encrypt(input('Enter New Username For Timesheet: \n').encode())
            dual_password_encrypt = f.encrypt(input('Enter New Password For Timesheet: \n').encode())
        else:  # else return nulls
            dual_user_encrypt = None
            dual_password_encrypt = None
        # Store user and password pair for access next time
        Encryption(user_encrypt, 'pair1.pair').write()
        Encryption(password_encrypt, 'pair2.pair').write()
        if dual:
            Encryption(dual_user_encrypt, 'pair3.pair').write()
            Encryption(dual_password_encrypt, 'pair4.pair').write()
        logging.info('Credentials stored successfully')

        logging.debug('Encrypted Username: %s' % user_encrypt)
        logging.debug('Encrypted Password: %s' % password_encrypt)

        # Pass back key and pairs
        return [f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt]

    def load(self, dual=False):
        # Loads Key and pairs from memory
        # Returns 'Encrypted-(Key,Email,Pass,User2,Pass2)

        # Load Key
        logging.info('Loading Key')
        file = open('./include/data/key.key', 'rb')
        key = file.read()
        file.close()
        f = Fernet(key)

        # Load encrypted credentials
        logging.info('Loading existing credentials...')
        user_encrypt = Encryption(None, 'pair1.pair').read()
        password_encrypt = Encryption(None, 'pair2.pair').read()
        if dual:
            dual_user_encrypt = Encryption(None, 'pair3.pair').read()
            dual_password_encrypt = Encryption(None, 'pair4.pair').read()
        else:  # else return nulls
            dual_user_encrypt = None
            dual_password_encrypt = None
        logging.info('Credentials loaded successfully')
        logging.debug('Encrypted Username: %s' % user_encrypt)
        logging.debug('Encrypted Password: %s' % password_encrypt)

        # Pass back key and pairs
        return [f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt]

class Authentication:

    def __init__(self):
        pass

class Navigate:
    # Basic Web fuctions with handleing xpath, ID, linktext
    def __init__(self,driver,elem):

        self.driver = driver
        self.elem = elem
        #click & wait time
        #click & wait for element


# make driver as a normal function then pass into navigate
def pagedriver():
    PATH_DRIVER = os.path.join(os.getcwd(), r'include\browser\driver\firefoxdriver.exe') # Currently using OS firefox.
    driver = webdriver.Firefox(executable_path=PATH_DRIVER)  # , firefox_binary=firefox_binary)
    return driver
