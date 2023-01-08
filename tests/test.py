import unittest
import getextip
import os
import shutil


class TestAdd(unittest.TestCase):

    def setUp(self) -> None:
        # Set up a special config for testing getextip
        if os.path.exists('/home/musicplayer/PycharmProjects/GetExtIP/config.ini'):  # Does a config file already exist?
            os.rename("/home/musicplayer/PycharmProjects/GetExtIP/config.ini", "/home/musicplayer/PycharmProjects"
                                                                               "/GetExtIP/config.old")  # Rename it
            # for a safety backup copy
        shutil.copy2("/home/musicplayer/PycharmProjects/GetExtIP/default.ini", "/home/musicplayer/PycharmProjects"
                                                                               "/GetExtIP/config.ini")  # Create
        # default config for testing

    def tearDown(self) -> None:
        # Return to existing configuration file after testing
        shutil.copy2("/home/musicplayer/PycharmProjects/GetExtIP/config.old", "/home/musicplayer/PycharmProjects"
                                                                              "/GetExtIP/config.ini")

    def test_seconds_to_time(self):
        # Test that an int representing seconds of time is returned as a sting of
        # hours:minutes:seconds
        result: str = getextip.seconds_to_time(86399)
        self.assertEqual(result, '23:59:59')

    def test_format_phn_nbr(self):
        # Verify that a US phone number string is formatted as expected
        result: str = getextip.format_phn_nbr('2676009420')
        self.assertEqual(result, '(267) 600-9420')

    # noinspection SpellCheckingInspection
    def test_get_config_list(self):
        # Test function to verify configparser retrieve operation
        reference_config_data = {
            'NOT SET': 'not_set', 'AT&T': '@txt.att.net', 'Sprint PCS': '@messaging.sprintpcs.com',
            'Sprint': '@pm .sprint.com', 'T-Mobile': '@tmomail.net', 'Verizon': '@vtext.com',
            'Boost Mobile': '@myboostmobile.com', 'Cricket': '@sms.mycricket.com',
            'Metro PCS': '@mymetropcs.com', 'Tracfone': '@mmst5.tracfone.com',
            'US Cellular': '@email.uscc.net', 'Virgin Mobile': '@vmobl.com'
        }
        result: dict = getextip.get_config_list('SMS_GATEWAYS_LIST')
        self.assertEqual(result, reference_config_data)

    def test_get_ip(self):
        """ Ensure the correct external IP address is returned by this function.
                Note that the proper external IP address must be provided here in order
                for the test to work at your location. This should be obtained from another
                method, like speedtest.net """

        result: str = getextip.get_ip()
        self.assertEqual(result, '108.5.131.213')

    # def test_report(self):
    #     # Not yet sure how to test this function...

    def test_is_config_data_bad(self):
        result: bool = getextip.is_config_data_bad('EMAIL_INFO', 'email_address')
        self.assertEqual(result, False)  # Is config set to a valid string? False means 'NOT SET' found


if __name__ == '__main__':
    unittest.main()
