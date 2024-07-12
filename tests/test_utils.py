import random
import unittest

from sleeper_h2h import utils


class SleeperH2HTestUtils(unittest.TestCase):

    def test_dict_merger(self):

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
