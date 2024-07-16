"""
Unit tests which do not depend on any class instatiation
"""

import random
import string
import unittest

from sleeper_h2h import discord, utils


class SleeperH2HTestDiscord(unittest.TestCase):

    """
    TestCase for the `discord` module
    """

    @classmethod
    def setUpClass(cls) -> None:

        cls.bad_webhook = "https://discord.com/api/webhooks/abcd1234"
        cls.img_location = "examples/h2h_plot-example.png"

    def test_invalid_webhook_send_text(self):

        """
        Test if a bad webhook results in a 405 status code
        """

        response = discord.send_text(self.bad_webhook, "Hello World!")

        self.assertEqual(response.status_code, 405)

    def test_invalid_webhook_send_image(self):

        """
        Test if a bad webhook results in a 405 status code
        """

        response = discord.send_image(self.bad_webhook, self.img_location)

        self.assertEqual(response.status_code, 405)


class SleeperH2HTestUtils(unittest.TestCase):

    """
    TestCase for the `utils` module
    """

    def test_merge_users_and_teams(self) -> None:

        """
        Test if a dict merged with a copy of itself where keys and values swap
        results in a dict where keys and values are identical
        """

        d1 = {"a": 1, "b": 2, "c": 3, "d": 4}
        d2 = {v: k for k, v in d1.items()}

        l = list(d2.items())
        random.shuffle(l)
        d2_shuffled = dict(l)

        merged_d = utils.merge_users_and_teams(d1, d2_shuffled)

        self.assertEqual(
            list(merged_d.keys()),
            list(merged_d.values())
        )

    def test_remove_emojis(self) -> None:

        """
        Test if a random string inserted with emojis at random can be ASCII
        encoded after removing emojis
        """

        emojis = ["😊", "🚀", "🌟", "🎉", "🔥", "🤖", "👾", "🌈", "🍕", "🎸"]
        test_string = ''.join(
            random.choices(
                string.ascii_letters +\
                    string.digits +\
                    string.whitespace +\
                    ''.join(emojis),
                k=128
                )
            )

        self.assertIsNot(utils.remove_emojis(test_string), UnicodeEncodeError)
