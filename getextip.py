# V0.2, still works with Pythonista...
# V0.3, still works with Pythonista...
# V0.4, need to change 'import keyring' to 'import keychain' in iOS
# V0.5, Hello Kivy, no longer works in Pythonista...
# V0.6, Basic Kivy operation working
# V0.7, Refining all functions and operation
# V0.7 now copies a default file into config.ini if it is missing...
# V0.8, File names changed for packaging, config file now properly dealt with on start up, visual changes
# V0.9, Many bug fixes and changes related to py2app
# V1.0, Added help screen, packaged for macOS
# V1.1, Removed all Kivy code and rebuilt as a Qt5 app
import socket
import urllib.request
import smtplib
from typing import Match
import dns.resolver
import re as re
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import configparser
import phonenumbers
import keyring.backends.kwallet
import keyring.backends.macOS
import keyring.backends.SecretService
import keyring.backends.Windows
import keyring
import sys
import logger_color

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QPushButton, QLineEdit,
    QComboBox, QSpinBox
)
from PyQt5.QtCore import QTimer
from main_window import Ui_MainWindow
from setup import Ui_DialogSetup
from about import Ui_DialogAbout
from help import Ui_DialogHelp

# Text strings
version = "V1.1"
about_get_ext_ip_1 = version + ' ©2021 - 2023 Advanced Design and Manufacturing, LLC'

# Global Variables
tmr: int = 0  # Timer variable

Logger = logger_color
Logger.start_logging(filename="log.txt", level="debug")
default = configparser.ConfigParser(allow_no_value=True,
                                    inline_comment_prefixes="#")  # Create instance of the config file parser
default.optionxform = str

try:
    default.read_file(open('default.ini', 'r'))  # Verify default file exists...
except FileNotFoundError as error:
    Logger.error(f'GetExtIP: read default file open: {error}')
    quit()  # Quit, any error here is too severe to continue
try:
    default.read('default.ini')  # Read the default file into memory
except ValueError as error:  # Here to fish for odd exceptions
    Logger.error(f'GetExtIP: reading default file to memory: {error}')
    quit()  # Quit, any error here is too severe to continue

# Setup config.ini ********************************************************************************
config: any = ''
try:
    config = configparser.ConfigParser(allow_no_value=True,
                                       inline_comment_prefixes="#")  # Create instance of the config file parser
    config.optionxform = str
except ValueError as error:  # Here to fish for odd exceptions
    Logger.error(f'GetExtIP: configparser setup: {error}')
    quit()  # Quit, any error here is too severe to continue
try:
    config.read_file(open('config.ini', 'r'))  # Verify config file exists...
except FileNotFoundError as error:
    Logger.error(f'GetExtIP: read config file open: {error}')
    shutil.copyfile('default.ini', 'config.ini')  # Copy from default config file to restore a missing config file
    bad_config = True  # Set the flag to halt checking IP until config file is complete
    Logger.info(f'GetExtIP: Copying default.ini to config.ini')
try:
    config.read('config.ini')  # Read the config file into memory
except ValueError as error:  # Here to fish for odd exceptions
    Logger.error(f'GetExtIP: reading config file to memory: {error}')
    quit()  # Quit, any error here is too severe to continue
config['INFO']['version'] = version  # Add version data to configuration
with open('config.ini', 'w') as configFile:  # Write the new config file with this updated information
    config.write(configFile)
# Setup config.ini ends****************************************************************************


# Functions ***************************************************************************************
def seconds_to_time(seconds: int) -> str:
    minutes: int
    minutes, seconds = divmod(seconds, 60)
    hours: int
    hours, minutes = divmod(minutes, 60)
    return str(f'{hours}:{minutes:0>2}:{seconds:0>2}')


def format_phn_nbr(number: str) -> str:
    phone_number: str = config.get('SMS_INFO', 'phone_number')  # Get the information from the config file
    if 'NOT SET' not in phone_number:
        return phonenumbers.format_number(phonenumbers.parse(number, 'US'), phonenumbers.PhoneNumberFormat.NATIONAL)
    else:
        return ''  # Return w/empty string when config file entry is not found


def ts():
    time_stamp: str = f'{datetime.datetime.now():%Y-%b-%d %H:%M:%S}'  # Get timestamp from Python
    return time_stamp  # Return with the formatted Python timestamp


def get_config_list(section: str) -> dict:  # Send section name in config to get all values as a dict
    dict1: dict[str, str | None] = {}
    options: list[str] = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                pass
        except ValueError as gcl_error:  # Here to fish for odd exceptions
            Logger.error(f'GetExtIP: get_config_list function: {gcl_error}')
            dict1[option] = None
    return dict1


def get_ip() -> str:
    result: bytes = b''
    url: str = config.get('URL', 'url')  # Get the selected "get IP" service URL from the config file
    try:
        result = urllib.request.urlopen(url).read()  # Get external IP address from service
    except ValueError as gi_error:  # Here to fish for odd exceptions
        Logger.error(f'GetExtIP: get_ip function: {gi_error}')
        quit()
    str_result: str = result.decode()  # Change received data from byte to string
    config['USER_INFO']['current_ip_addr'] = str_result  # Add user data to configuration
    with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
        config.write(config_file)
    return str_result  # Return IP address as a string


def report(ip_address: str):
    server = ''  # Not sure how to type this
    phone_number = config.get('SMS_INFO', 'phone_number')  # Get the information from the config file
    if 'NOT SET' in phone_number:
        return
    smtp_server = config.get('SMS_INFO', 'smtp_server')  # Get the information from the config file
    if 'NOT SET' in smtp_server:
        return
    email_address = config.get('EMAIL_INFO', 'email_address')  # Get the information from the config file
    if 'NOT SET' in email_address:
        return
    sms_gw_key = config.get('SMS_INFO', 'selected')  # Get the information from the config file
    if 'NOT SET' in sms_gw_key:
        return
    gateway = config.get('SMS_GATEWAYS_LIST', sms_gw_key)  # Use the key to retrieve the correct gateway from config
    from_name = config.get('USER_INFO', 'from_name')  # Get the information from the config file
    if 'NOT SET' in from_name:
        return
    email_password = ''
    try:
        email_password = keyring.get_password("getextip.py", email_address)  # Get password from OS keyring
    except Exception as e:
        Logger.error(f'GetExtIP: in report - {e}')
    try:
        server = smtplib.SMTP_SSL(smtp_server, 465)
    except ValueError as ssl_error:
        Logger.error(f'GetExtIP: report function: {ssl_error}')
        quit()
    try:
        server.ehlo()
    except ValueError as ehlo_error:  # Here to fish for odd exceptions
        Logger.error(f'GetExtIP: report function: {ehlo_error}')
        quit()
    try:
        server.login(email_address, email_password)
    except smtplib.SMTPAuthenticationError as login_error:
        Logger.error(f'GetExtIP: report function: {login_error}')
        msg_box = QMessageBox()  # Show popup error window *** NOT TESTED ***
        msg_box.ButtonRole(QMessageBox.AcceptRole)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText('Email username or password is incorrect or missing')
        msg_box.setInformativeText('')  # Details...
        msg_box.setWindowTitle('GetExtIP Error')
        msg_box.setStandardButtons(QMessageBox.Ok)
        result = msg_box.exec_()  # Display the message box and return when Ok button is clicked
        if result == msg_box.Ok:
            return
    msg = MIMEMultipart()  # Start to build the message string using MIME
    msg['email_address'] = email_address
    phone_address = phone_number + gateway  # Create the remote SMS address string here
    msg['phone_address'] = phone_address
    msg['subject'] = f'From GetExtIP'  # Includes name of site being monitored
    message = f'The {from_name} External IP address is now: {ip_address}'
    msg.attach(MIMEText(message, 'plain'))
    message = msg.as_string()
    try:
        server.sendmail(email_address, phone_address, message)
    except ValueError as r_error:  # Here to fish for odd exceptions
        Logger.error(f'GetExtIP: report function: {r_error}')


def compare(old_ip: str, new_ip: str) -> str:
    if old_ip == new_ip:  # Compare stored and new addresses
        config['USER_INFO']['previous_ip_addr'] = old_ip  # Add user data to configuration
        config['USER_INFO']['current_ip_addr'] = new_ip  # Add user data to configuration
        with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
            config.write(config_file)
        return new_ip
    else:
        config['USER_INFO']['previous_ip_addr'] = config['USER_INFO']['current_ip_addr']  # Update config's data
        config['USER_INFO']['current_ip_addr'] = new_ip  # Add user data to configuration
        with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
            config.write(config_file)
        report(new_ip)  # Report IP change to stored phone
        return new_ip


def is_config_data_bad(section: str, option: str) -> bool:  # Checks for 'NOT SET' in config file, flag if true
    Logger.debug(f'GetExtIP: is_config_data_bad: Started')
    config_data = config.get(section, option)
    if 'NOT SET' in config_data:
        Logger.debug(
            f'GetExtIP: is_config_data_bad {section}->{option}: Config data is: {config_data}')
        return True  # Is config set properly? NO!
    else:
        Logger.debug(
            f'GetExtIP: is_config_data_bad {section}->{option}: Config data is: {config_data}')
        return False  # Is config set properly? YES!


def check_file() -> bool:  # Opens config.ini and looks for instances of 'NOT SET'
    Logger.debug(f'GetExtIP: check_file: Started')  # if any found, configuration is incomplete
    with open('config.ini') as f:
        text = f.readlines()
    for line in text:
        if 'NOT SET' in line:
            return True  # String found
        else:
            config['INFO']['mode'] = 'configured'  # Add config flag showing everything is configured
            with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
                config.write(config_file)
            return False
# Functions end ***********************************************************************************


# Main window class *******************************************************************************
class Window(QMainWindow, Ui_MainWindow):
    timer: QTimer | QTimer

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connect_signals_slots()
        Logger.debug(f'GetExtIP: MainWindow: Started')
        self.timer = QTimer()
        # noinspection PyUnresolvedReferences
        self.timer.timeout.connect(self.check_timer)
        self.timer.start(1000)

        # Handle Buttons ***************************************************************
        self.check_now_button = self.findChild(QPushButton, 'pushButtonCheckNow')  # Get handle Check Now QPushButton
        self.check_now_button.clicked.connect(self.update_ip)  # Connect signal to method
        # Handle Buttons ends **********************************************************

    def connect_signals_slots(self):
        self.actionGetExtIP_Setup.triggered.connect(self.get_ext_ip_setup)
        self.actionGetExtIP_Help.triggered.connect(self.get_ext_ip_help)
        self.actionAbout_GetExtIP.triggered.connect(self.about)

    def get_ext_ip_setup(self):
        dialog: GetExtIPSetupDialog = GetExtIPSetupDialog(self)
        dialog.exec()

    def get_ext_ip_help(self):
        dialog: GetExtIPHelpDialog = GetExtIPHelpDialog(self)
        dialog.exec()

    def about(self):
        dialog: GetExtIPAboutDialog = GetExtIPAboutDialog(self)
        dialog.exec()

    def check_config(self):  # Look for first run flag in config and force setup
        Logger.debug(f'GetExtIP: SetupWindow: check_config: Started')
        if config.get('INFO', 'mode') == 'startup':
            if check_file():  # Check the config file to see if any items remain un-configured
                Logger.debug(f'GetExtIP: Class MainWindow: Config flag is \'startup\'')
                MsgBox.message_box(str(f'Configuration is incorrect or missing, ' f'please complete setup'), '')
                self.get_ext_ip_setup()  # Open the setup dialog here
        else:
            Logger.info(f'GetExtIP: Class MainWindow: Config file Ok')

    def update_ip(self):  # Definition for Check Now button, also called by check_timer
        Logger.debug(f'GetExtIP: SetupWindow: update_ip: Started')
        global tmr
        self.check_config()  # Make sure config is complete
        tmr = int(config['USER_INFO']['sleep_time'])  # Reset countdown timer to value from config file
        result = get_ip()  # Call getIP function
        Logger.info(f'GetExtIP: Class MainWindow: Function update_ip: External IP is: {result}')
        old_ip = config['USER_INFO']['previous_ip_addr']  # Get user data from configuration
        new_ip = config['USER_INFO']['current_ip_addr']  # Get user data from configuration
        result = compare(old_ip, new_ip)  # Compare new IP address to stored one in config file
        self.labelCurrentIP.setText('<font color="blue">' + str(result) + '</font>')
        self.labelPreviousIP.setText('<font color="blue">' + str(old_ip) + '</font>')

    def check_timer(self) -> None:  # Updates IP info periodically
        global tmr  # Access global timer variable
        if tmr == 0:  # If timer expired...
            tmr = int(config['USER_INFO']['sleep_time'])  # Set countdown timer to value from config file
            self.update_ip()  # Update external IP address
        tmr = tmr - 1  # Decrement timer every second
        time_secs: str = seconds_to_time(tmr)  # Convert seconds to "normal" time for display
        self.labelTimeToNextCheck.setText('<font color="blue">' + str(time_secs) + '</font>')
        return
# Main window class ends **************************************************************************


# Setup window ************************************************************************************
class GetExtIPSetupDialog(QDialog, Ui_DialogSetup):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Handle Buttons **************************************************************************
        self.test_button = self.findChild(QPushButton, 'pushButtonTest')  # Get handle for Check Now QPushButton
        self.test_button.clicked.connect(self.test_reporting)

        #  Need to call each input processor separately
        self.line_edit_phone_number = self.findChild(QLineEdit, 'lineEditPhoneNumber')
        self.line_edit_phone_number.editingFinished.connect(
            self.phone_number_input)  # Get editing finished event from lineEdit

        self.line_edit_smtp_server = self.findChild(QLineEdit, 'lineEditSMTPServer')
        self.line_edit_smtp_server.editingFinished.connect(
            self.smtp_server_input)

        self.line_edit_email_address_input = self.findChild(QLineEdit, 'lineEditEmailAddress')
        self.line_edit_email_address_input.editingFinished.connect(
            self.email_address_input)

        self.line_edit_email_password_input = self.findChild(QLineEdit, 'lineEditEmailSendingAccountPassword')
        self.line_edit_email_password_input.editingFinished.connect(
            self.email_password_input)

        self.line_edit_from_name = self.findChild(QLineEdit, 'lineEditNameToUseWhenTextsAreSent')
        self.line_edit_from_name.editingFinished.connect(
            self.text_from_name_input)

        self.combo_box_selected_sms_gateway = self.findChild(QComboBox, 'comboBoxSelectedSMSGateway')
        self.combo_box_selected_sms_gateway.activated.connect(
            self.select_sms_server)  # Get activated event from comboBox

        self.spin_box_time_between_checks = self.findChild(QSpinBox, 'spinBoxTimeIntervalBetweenIPChecks')
        self.spin_box_time_between_checks.valueChanged.connect(
            self.select_time_between_checks)  # Get valueChanged event from spinBox
        # Handle Buttons ends *********************************************************************

        # Get data from config.ini and display it *************************************************
        phone_number: str = config.get('SMS_INFO', 'phone_number')  # Get from the config file
        if 'NOT SET' in phone_number:
            Logger.warning(f'GetExtIP: phone_number not set')
            self.lineEditPhoneNumber.setStyleSheet("color: red;")
            self.lineEditPhoneNumber.setText(phone_number)
        else:
            phone_number = format_phn_nbr(phone_number)  # Format for display
            self.lineEditPhoneNumber.setStyleSheet("color: green;")
            self.lineEditPhoneNumber.setText(phone_number)

        smtp_server: str = config.get('SMS_INFO', 'smtp_server')
        if 'NOT SET' in smtp_server:
            Logger.warning(f'GetExtIP: email_address not set')
            self.lineEditSMTPServer.setStyleSheet("color: red;")
            self.lineEditSMTPServer.setText(smtp_server)
        else:
            self.lineEditSMTPServer.setStyleSheet("color: green;")
            self.lineEditSMTPServer.setText(smtp_server)

        email_address: str = config.get('EMAIL_INFO', 'email_address')
        if 'NOT SET' in email_address:
            Logger.warning(f'GetExtIP: email_address not set')
            self.lineEditEmailAddress.setStyleSheet("color: red;")
            self.lineEditEmailAddress.setText(email_address)
        else:
            self.lineEditEmailAddress.setStyleSheet("color: green;")
            self.lineEditEmailAddress.setText(email_address)

        password: str = config.get('EMAIL_INFO', 'password')  # Show text for password entry button
        if 'NOT SET' in password:
            Logger.warning(f'GetExtIP: password is not set')
            self.lineEditEmailSendingAccountPassword.setStyleSheet("color: red;")
            self.lineEditEmailSendingAccountPassword.setText(password)
        else:
            self.lineEditEmailSendingAccountPassword.setStyleSheet("color: green;")
            self.lineEditEmailSendingAccountPassword.setText(password)

        sms_list: dict = get_config_list('SMS_GATEWAYS_LIST')  # Get all values from config section
        self.comboBoxSelectedSMSGateway.addItems(sms_list.keys())  # Populate the spinner list with values from config
        gateway = config.get('SMS_INFO', 'selected')
        if 'NOT SET' in gateway:
            Logger.warning(f'GetExtIP: gateway is not selected')
            self.comboBoxSelectedSMSGateway.setStyleSheet("color: red;")
        else:
            self.comboBoxSelectedSMSGateway.setStyleSheet("color: green;")
            gateway = config.get('SMS_INFO', 'selected')
            self.comboBoxSelectedSMSGateway.setCurrentText(gateway)  # Restore the user's setting

        from_name: str = config.get('USER_INFO', 'from_name')  # Get data from config.ini and display it
        if 'NOT SET' in from_name:
            Logger.warning(f'GetExtIP: from_name not set')
            self.lineEditNameToUseWhenTextsAreSent.setStyleSheet("color: red;")
            self.lineEditNameToUseWhenTextsAreSent.setText(from_name)
        else:
            self.lineEditNameToUseWhenTextsAreSent.setStyleSheet("color: green;")
            self.lineEditNameToUseWhenTextsAreSent.setText(from_name)
        # Get data from config.ini and display it ends ********************************************

    def phone_number_input(self) -> None:  # Parse, format, verify and store user input
        if self.line_edit_phone_number.isModified():  # editingFinished is triggered by selecting the window...
            Logger.debug(f'Line was modified')  # moving the window, etc. Need to check if user really modified
            Logger.debug(f'GetExtIP: PhoneNbrInput: process: Started')  # the input or not
            raw_text: str = self.line_edit_phone_number.text()  # Get input from user
            Logger.debug(f'GetExtIP: PhoneNbrInput: process: Get input: {raw_text}')
            # parse the info...
            clean_text: str = ''.join(
                i for i in raw_text if i.isdigit())  # Remove non-numeric chars that user may have entered
            try:
                phone_number = phonenumbers.parse(clean_text, 'US')  # Verify input is a phone number (US only)
                Logger.info(f'GetExtIP: Phone number entered by user is: {phone_number}')
            except phonenumbers.NumberParseException as pni_error:
                Logger.error(f'GetExtIP: Class PhoneNbrInput: Function process: {pni_error}')
                MsgBox.message_box('Please correct the phone number', '')
                self.lineEditPhoneNumber.setStyleSheet("color: red;")  # Make it red
                self.lineEditPhoneNumber.setText(raw_text)  # Stick it in the lineEdit box
                return  # Do not store bad data
            # If it's a phone number, refresh the QLineEdit box with the user's sanitized info in green
            config['SMS_INFO']['phone_number'] = clean_text  # Add user data to configuration
            with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
                config.write(config_file)
            phone_number = format_phn_nbr(clean_text)  # Format for display
            self.lineEditPhoneNumber.setStyleSheet("color: green;")  # Make it green
            self.lineEditPhoneNumber.setText(phone_number)  # Stick it in the lineEdit box
            return
        else:
            Logger.debug(f'Line was NOT modified')  # Do not process if user has not changed the line
            return

    def smtp_server_input(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: SmtpServerInput: process: Started')
        if self.line_edit_smtp_server.isModified():
            raw_text: str = self.line_edit_smtp_server.text()  # Get input from user
            smtp_server: str = raw_text  # Verify input is a valid SMTP server
            try:
                server = smtplib.SMTP_SSL(smtp_server, 465)
            except socket.gaierror as ssi_error:
                Logger.error(f'GetExtIP: SmtpServerInput: process: ssi_error {ssi_error}')
                MsgBox.message_box(str(f'Please check your SMTP address and try again'), '')
                self.lineEditSMTPServer.setStyleSheet("color: red;")  # Make it red
                self.lineEditSMTPServer.setText(raw_text)  # Stick it in the lineEdit box
                return  # Do not store bad data
            try:
                server.ehlo()
            except smtplib.SMTPException as ehlo_error:
                Logger.error(f'GetExtIP: SmtpServerInput: process: ehlo_error {ehlo_error}')
                MsgBox.message_box(str(f'Please check your SMTP address and try again'), '')
                self.lineEditSMTPServer.setStyleSheet("color: red;")  # Make it red
                self.lineEditSMTPServer.setText(raw_text)  # Stick it in the lineEdit box
                return  # Do not store bad data
            config['SMS_INFO']['smtp_server'] = smtp_server  # Add user data to configuration
            with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
                config.write(config_file)
            self.lineEditSMTPServer.setStyleSheet("color: green;")  # Make it green
            self.lineEditSMTPServer.setText(raw_text)  # Stick it in the lineEdit box
            return
        else:
            return

    def email_address_input(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: EmailAddressInput: process: Started')
        if self.line_edit_email_address_input.isModified():
            email_address: str = self.line_edit_email_address_input.text()  # Get input from user
            # Verify input is a valid email address
            match: Match[str] | None = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)'
                                                r'*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email_address)
            if match is None:
                Logger.error(
                    f'GetExtIP: Class EmailAddressInput: Function process: Bad email address entered by user')
                MsgBox.message_box(
                    str(f'Please check your email address for illegal or missing characters and try again'),
                    '')
                self.lineEditEmailAddress.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailAddress.setText(email_address)  # Stick it in the lineEdit box
                return  # Do not store bad data
            try:
                domain_name: str = email_address.split('@')[1]  # Get the domain name out of the address
            except Exception as e:
                Logger.error(f'GetExtIP: Class EmailAddressInput: Function process: {e}')
                MsgBox.message_box(str(f'Please check your email address and try again. {e}'), '')
                self.lineEditEmailAddress.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailAddress.setText(email_address)  # Stick it in the lineEdit box
                return  # Do not store bad data
            try:
                records: dict = dns.resolver.resolve(domain_name, 'MX')  # Get MX record see if domain name is good
            except Exception as e:  # Here to fish for odd exceptions
                Logger.error(f'GetExtIP: Class EmailAddressInput: Function resolve MX: {e}')
                MsgBox.message_box(str(f'Please check your email address and try again. {e}'), '')
                self.lineEditEmailAddress.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailAddress.setText(email_address)  # Stick it in the lineEdit box
                return  # Do not store bad data
            try:
                mx_record = records[0].exchange
                mx_record = str(mx_record)
                Logger.info(f'GetExtIP: Class EmailAddressInput: Function process: {mx_record}')
            except ValueError as eai_error:  # Here to fish for odd exceptions
                Logger.error(f'GetExtIP: Class EmailAddressInput: Function process: {eai_error}')
                MsgBox.message_box(str(f'Please check your email address and try again. {eai_error}'), '')
                self.lineEditEmailAddress.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailAddress.setText(email_address)  # Stick it in the lineEdit box
                return  # Do not store bad data
            config['EMAIL_INFO']['email_address'] = email_address  # Add user data to configuration
            with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
                config.write(config_file)
            self.lineEditEmailAddress.setStyleSheet("color: green;")  # Make it green
            self.lineEditEmailAddress.setText(email_address)  # Stick it in the lineEdit box
            return
        else:
            return

    def email_password_input(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: process: on_enter: Started')
        if self.line_edit_email_password_input.isModified():
            email_address: str = config.get('EMAIL_INFO', 'email_address')  # Need for keyring
            password: str = self.line_edit_email_password_input.text()  # Get input from user
            # if 'NOT SET' in config.get('EMAIL_INFO', 'password'):
            #     Logger.warning(f'GetExtIP: EmailAddressInput function: password is not set (blank)')
            #     app.email_password_input_bad_data = True  # TODO: And then???
            # else:
            #     app.email_password_input_bad_data = False

            # noinspection PyUnresolvedReferences
            try:
                keyring.set_password("getextip.py", email_address,
                                     password)  # Store user's email password in local keychain
            except keyring.errors.PasswordSetError as epi_error:
                Logger.error(f'GetExtIP: Class EmailPasswordInput: Function process: {epi_error}')
                self.lineEditEmailSendingAccountPassword.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailSendingAccountPassword.setText(password)  # Stick it in the lineEdit box
                # noinspection PyUnresolvedReferences
                MsgBox.message_box(str(f'Can\'t store password on keychain, please try again'), '')
                return
            email_password: str = ''
            # noinspection PyUnresolvedReferences
            try:
                email_password = keyring.get_password("getextip.py", email_address)  # Get password from OS keyring
            except keyring.errors.KeyringError as k_error:
                Logger.error(f'GetExtIP: Class EmailPasswordInput: Function process: {k_error}')
                self.lineEditEmailSendingAccountPassword.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailSendingAccountPassword.setText(password)  # Stick it in the lineEdit box
                MsgBox.message_box(str(f'Errors reading from keychain, please try again'), '')
            if password != email_password:  # Compare new password against what is in keychain to see if it worked
                Logger.error(f'GetExtIP: Class EmailPasswordInput: Function process: Password not stored correctly')
                self.lineEditEmailSendingAccountPassword.setStyleSheet("color: red;")  # Make it red
                self.lineEditEmailSendingAccountPassword.setText(password)  # Stick it in the lineEdit box
                MsgBox.message_box(str(f'Password not stored correctly, please try again'), '')
            else:
                config['EMAIL_INFO'][
                    'password'] = ''  # Clear the data in the config file, password securely stored in OS
                with open('config.ini',
                          'w') as config_file:  # Write the new config file with this updated information
                    config.write(config_file)
                Logger.info(f'GetExtIP: Class EmailPasswordInput: Function process: Password stored in keychain')
                self.lineEditEmailSendingAccountPassword.setStyleSheet("color: green;")  # Make it green
                self.lineEditEmailSendingAccountPassword.setText(password)  # Stick it in the lineEdit box, all Ok
                return
        else:
            return

    def text_from_name_input(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: TextFromNameInput: process: Started')
        if self.line_edit_from_name.isModified():
            text: str = self.lineEditNameToUseWhenTextsAreSent.text()  # Get input from user
            from_name: str = text  # Verify input has no unusual characters
            match: Match[str] | None = re.match(r'\w+', from_name)
            if match is None:
                Logger.error(
                    f'GetExtIP: Class TextFromNameInput: Function process: Illegal characters entered by user')
                self.lineEditNameToUseWhenTextsAreSent.setStyleSheet("color: red;")  # Make it red
                self.lineEditNameToUseWhenTextsAreSent.setText(text)  # Stick it in the lineEdit box
                MsgBox.message_box(str(f'Please check your email address for illegal characters and try again'),
                                   '')
                return  # Do not store bad data
            config['USER_INFO']['from_name'] = from_name  # Add user data to configuration
            with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
                config.write(config_file)
            self.lineEditNameToUseWhenTextsAreSent.setStyleSheet("color: green;")  # Make it green
            self.lineEditNameToUseWhenTextsAreSent.setText(from_name)  # Stick it in the lineEdit box
            Logger.info(f'GetExtIP: TextFromNameInput: From Name Saved')
            return
        else:
            return

    def select_sms_server(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: SelectSmsServer: process: Started')
        value: str = self.comboBoxSelectedSMSGateway.currentText()  # Get input from user
        selected_gateway: str = value
        config['SMS_INFO']['selected'] = selected_gateway  # Add user data to configuration
        with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
            config.write(config_file)
        # Reload comboBox to reset coloring
        self.comboBoxSelectedSMSGateway.clear()  # Clear existing list first
        sms_list: dict = get_config_list('SMS_GATEWAYS_LIST')  # Get all values from config section
        self.comboBoxSelectedSMSGateway.addItems(sms_list.keys())  # Populate the spinner list with values from config
        gateway: str = config.get('SMS_INFO', 'selected')
        self.comboBoxSelectedSMSGateway.setCurrentText(gateway)  # Restore the user's setting
        if 'NOT SET' in gateway:
            Logger.warning(f'GetExtIP: gateway is not selected')
            self.comboBoxSelectedSMSGateway.setStyleSheet("color: red; font-size: 10pt;")
        else:
            self.comboBoxSelectedSMSGateway.setStyleSheet("color: green; font-size: 10pt;")
            pass

    def select_time_between_checks(self) -> None:  # Parse, format, verify and store user input
        Logger.debug(f'GetExtIP: SelectTimeBetweenChecks: process: Started')
        value: int = self.spin_box_time_between_checks.value()  # Get user input from spinBox
        scaled_value: int = value * 3600  # Scale hours to seconds
        selected_gateway: str = str(scaled_value)
        config['USER_INFO']['sleep_time'] = selected_gateway  # Add user data to configuration
        with open('config.ini', 'w') as config_file:  # Write the new config file with this updated information
            config.write(config_file)
        return

    @staticmethod
    def test_reporting() -> None:
        Logger.debug(f'GetExtIP: SetupWindow: test_reporting: Started')
        report(get_ip())
        return
# Setup window ends *******************************************************************************


# Help window *************************************************************************************
class GetExtIPHelpDialog(QDialog, Ui_DialogHelp):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
# Help window ends ********************************************************************************


# About window ************************************************************************************
class GetExtIPAboutDialog(QDialog, Ui_DialogAbout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
# About window ends *******************************************************************************


# Message Box window ******************************************************************************
class MsgBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def message_box(text: str, informative_text: str) -> int:
        msg_box: QMessageBox | QMessageBox = QMessageBox()  # Show popup error window
        msg_box.setStyleSheet('QLabel{'
                              'font-family: Noto Sans; '
                              'font-size: 10pt; '
                              'font-weight: bold; '
                              'color: black;'
                              '}'
                              'QPushButton{'
                              'font-family: Noto Sans; '
                              'font-size: 10pt; '
                              'font-weight: normal; '
                              'color: black;'
                              '}'
                              )
        msg_box.ButtonRole(QMessageBox.AcceptRole)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(text)
        msg_box.setInformativeText(informative_text)  # Details...
        msg_box.setWindowTitle('GetExtIP Error')
        msg_box.setStandardButtons(QMessageBox.Ok)
        result: int = msg_box.exec_()  # Display the message box and return when Ok button is clicked
        return result
# Message Box window ends *************************************************************************


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win: Window = Window()
    win.show()
    sys.exit(app.exec())
