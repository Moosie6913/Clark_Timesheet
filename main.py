import logging, os, time, sys, gui
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PyQt5 import QtCore, QtGui, QtWidgets
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

######################### CUSTOM DATA ###############################################



class Encryption:
    # This class handles tasks related to encryption and decryption
    def __init__(self):
        pass

    def write(self,item,filename):
        # Writing and storing credentials to file
        # Returns None
        logging.debug('Saving user data...')
        logging.debug('%s key: %s' % (filename, item))
        path = "./include/data/" + filename
        file = open(path, 'wb')
        file.write(item)
        file.close()

    def read(self,filename):
        # Reading credentials from stored file
        # Returns (encrypted item)
        logging.debug('Loading user data...')
        path = "./include/data/" + filename
        file = open(path, 'rb')
        item_encrypt = file.read()
        file.close()
        logging.debug('%s key: %s' % (filename, item_encrypt))
        return item_encrypt

    def clear(self):
        # Clears ALL stored data user email and password data
        # Returns None
        try:  # if it exists removed the data
            logging.info('Deleting all stored log in details.')
            os.remove("./include/data/key.key")
            os.remove("./include/data/pair1.pair")
            os.remove("./include/data/pair2.pair")
            os.remove("./include/data/pair3.pair")
            os.remove("./include/data/pair4.pair")
            logging.info('Successfully deleted.')
        except:  # if no data exists or it error proceed
            logging.error('No stored user data found... Continuing...')
            pass

    def save(self, user1, pass1, user2, pass2):
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
        user_encrypt = f.encrypt((user1).encode())
        password_encrypt = f.encrypt(pass1.encode())
        dual = False
        if user2 is not None and pass2 is not None: # Dual
            dual = True
            #print('Enter log on details for secondary authentication screen i.e for timesheet log on')
            dual_user_encrypt = f.encrypt(user2.encode())
            dual_password_encrypt = f.encrypt(pass2.encode())
        else:  # else return nulls
            dual_user_encrypt = None
            dual_password_encrypt = None
        # Store user and password pair for access next time
        Encryption().write(user_encrypt, 'pair1.pair')
        Encryption().write(password_encrypt, 'pair2.pair')
        if dual:
            Encryption().write(dual_user_encrypt, 'pair3.pair')
            Encryption().write(dual_password_encrypt, 'pair4.pair')
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
        user_encrypt = Encryption().read('pair1.pair')
        password_encrypt = Encryption().read('pair2.pair')
        try:
            dual_user_encrypt = Encryption().read('pair3.pair')
            dual_password_encrypt = Encryption().read('pair4.pair')
        except:  # else return nulls
            dual_user_encrypt = None
            dual_password_encrypt = None
        logging.info('Credentials loaded successfully')
        logging.debug('Encrypted Username: %s' % user_encrypt)
        logging.debug('Encrypted Password: %s' % password_encrypt)

        # Pass back key and pairs
        return [f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt]

class Authentication:
    # This class handles login

    def __init__(self,driver,f,user1,pass1,user2,pass2):
        self.driver = driver
        self.f = f
        self.user1 = user1
        self.pass1 = pass1
        self.user2 = user2
        self.pass2 = pass2

    def microsoftlogin(self, targetURL):
        # Microsoft log on screen with MFA/2FA
        logging.info('Microsoft Authentication required...')
        self.driver.get(targetURL)

        # Input Username
        logging.debug('Entering Email')
        user_elem = Navigate(self.driver, 'i0116', 'ID').loadelem(10)
        user_elem.send_keys(self.f.decrypt(self.user1).decode())
        Navigate(self.driver, 'idSIButton9', 'ID').click(2)

        # Input Password
        logging.debug('Entering Password')
        pass_elem = Navigate(self.driver, 'i0118', 'ID').loadelem(10)
        pass_elem.send_keys(self.f.decrypt(self.pass1).decode())
        Navigate(self.driver, 'idSIButton9', 'ID').click(2)

        # try:  # Check to see if password is incorrect/Failed
        #     pass_error = Navigate(self.driver, 'passwordError', 'ID').loadelem(1)
        #     logging.error("Password is incorrect, please enter correct credentials...")
        #     input('Press any key to close...')
        # except:  # Do nothing as it worked
        #     logging.debug("Password accepted")
        #     pass
        # if:
        #     self.driver.quit()
        #     sys.exit()
        #TODO add password incorrect if ID='passwordError' Appears

        # MFA/2FA stage
        logging.info('Waiting for you to complete authentication step on your mobile. Waiting up to 60secs.')
        #TODO add different types of MFA, not just moblie (ADD CODE)
        elem = Navigate(self.driver, 'KmsiCheckboxField', 'ID').loadelem(60)
        elem.click()
        logging.info('Authentication successful!')
        Navigate(self.driver, 'idSIButton9', 'ID').click(2)

        # TODO incorportate this check if authenticaiton is even required
        # /html/body/div/form[1]/div/div/div[1]/div[2]/div[1]/img
        # if this exists, login is required

    def worley(self):
        pass

    def ecr(self):
        pass


class Navigate:
    # Basic Web factions with handling xpath, ID, linktext

    def __init__(self,driver,item,elemtype):
        self.driver = driver
        self.item = item
        self.elemtype = elemtype

    def loadelem(self,maxtime=int(30),interact=False):
        # Waits for element to load
        # returns (element)

        try:
            if str(self.elemtype.upper()) == 'ID':
                element = WebDriverWait(self.driver,maxtime).until(
                    EC.presence_of_element_located((By.ID, self.item)))
                return element
            elif str(self.elemtype.upper()) == 'XPATH':
                pass  # TODO Set LOAD XPATH up
            elif str(self.elemtype.upper()) == 'LINKTEXT':
                pass  # TODO Set LOAD LINKTEXT up
            else:
                logging.error("Click&Load Method Failed ERROR - Element type is incorrect")
                return None
        except:
            logging.error('Click&Load Method Failed ERROR - Element did not load\n\rClosing website now')
            input('Press any key to close...')
            quit()



    def click(self,delay=int(1)):
        # Finds and clicks element based on ID, XPATH or LINKTEXT
        # returns None

        # Locate Element
        try:
            if str(self.elemtype.upper()) == 'ID':
                element = self.driver.find_element_by_id(self.item)
            elif str(self.elemtype.upper()) == 'XPATH':
                element = self.driver.find_element_by_xpath(self.item)
            elif str(self.elemtype.upper()) == 'LINKTEXT':
                element = self.driver.find_element_by_link_text(self.item)
            else:
                logging.error("Click Method Failed ERROR - Element type is incorrect")
                return None

            element.click()# Click Element
            time.sleep(delay)  # Delay before next action
        except:
            logging.error('Click Method Failed ERROR - Element did not load\n\rClosing website now')
            input('Press any key to close...')
            quit()


def getdriver():
    PATH_DRIVER = os.path.join(os.getcwd(), r'include\browser\driver\firefoxdriver.exe') # Currently using OS firefox.
    driver = webdriver.Firefox(executable_path=PATH_DRIVER)  # , firefox_binary=firefox_binary)
    return driver


def user_credentials_overwrite(user1=None, pass1=None, user2=None, pass2=None):
    if user1 is not None and pass1 is not None:
        #TODO add regex
        Encryption().clear()
        f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt = Encryption().save(user1, pass1, user2, pass2)
        return True
    else:
        logging.debug("User or password was blank")
        return False

def startupload():
    try:
        f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt = Encryption().load()
        user1 = f.decrypt(user_encrypt).decode()
        pass1 = len(f.decrypt(password_encrypt).decode()) * "*"
        if dual_user_encrypt is not None and dual_password_encrypt is not None:
            user2 = f.decrypt(dual_user_encrypt).decode()
            pass2 = len(f.decrypt(dual_password_encrypt).decode()) * "*"
        else:
            user2 = str("")
            pass2 = str("")
        return user1, pass1, user2, pass2
    except:
        user1, pass1, user2, pass2 = None, None, None, None
        return user1, pass1, user2, pass2

def launch(platform):
    if platform == "WorleyParsons":
        targetURL = 'https://ebs.worley.com/OA_HTML/OA.jsp?OAFunc=OAHOMEPAGE'
    else: #Jacobs ECR
        targetURL = 'https://sharepoint.worley.com' #TODO set up ECR pathway

    try:
        f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt = Encryption().load()
        driver = getdriver()
        Authentication(driver,f,user_encrypt,password_encrypt,dual_user_encrypt,dual_password_encrypt).microsoftlogin(targetURL)
        time.sleep(5)
        if platform == "WorleyParsons":
            pass
            #worley_stages(driver)
        #Element not loading. Try elsewhere
    except:
        logging.error("No saved data")
        pass #TODO Add popup for no saved data


def worley_stages(driver):
    print(1)
    Navigate(driver,"WP AU Time Entry", "LINKTEXT").click(1)
    print(2)
    Navigate(driver, "Time Entry", "LINKTEXT").click(1)
    print(3)
    Navigate(driver, "Create Timecard", "LINKTEXT").click(1)

def ecr_stages():
    pass
# #MAIN
# # Ask if new or current credentials
# print('Select from the following options:\n[1] - Input New Login Details\n[2] - Use Existing')
# x = input('>>> ')
#
# dual = False
#
# if x == '1':  # if new credentials are reburied
#
#     logging.info('Option 1 Selected: Override existing credentials? ')
#     x = input('Override existing credentials? [Y/N]\n')
#     if x.upper() == 'Y':  # If override confirm
#         print("Please enter your network log in details... e.g \'connor.clark@worleyparsons.com\' ")
#         Encryption().clear()
#         f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt = Encryption().save(dual)
#         # TODO: Add in confirmation of details
#     else: # abort program
#         input('Press any key to close...')
#         sys.exit()
#
# else: # if using previous credentials
#     f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt = Encryption().load(dual)
#

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #driver = getdriver()
    #Authentication(driver, f, user_encrypt, password_encrypt, dual_user_encrypt, dual_password_encrypt).microsoftlogin(targetURL)
    sys.exit(app.exec_())



