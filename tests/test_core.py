"""
Unit tests which depend on instantiating a Standings object
"""

import os
import unittest

from sleeper_h2h import graphics, utils
from sleeper_h2h.standings import Standings
from .utils import read_metadata_from_signed_pickle


class SleeperH2HTestDependsClass(unittest.TestCase):

    """
    TestCase for module tests requiring a `setUpClass()` method which
    instantiates a `Standings` object
    """

    @classmethod
    def setUpClass(cls) -> None:

        """
        Prepare the TestCase with a Standings object, initialized by reading
        mock_data.pkl after verifying its HMAC signature
        """

        cls.metadata = read_metadata_from_signed_pickle(
            "tests/mock_data.pkl",
            b"sleeper-h2h-mock-data"
        )
        cls.standings = Standings(
            cls.metadata._Metadata__league_id, # pylint: disable=W0212
            cls.metadata
        )
        cls.standings.make_h2h_standings_df()

    def test_draw_h2h_plot_figure_instance(self):

        """
        Test if newly generated plot image is an instance of a Plotly Figure
        """

        fig = graphics.draw_h2h_plot(self.standings.h2h_board_df)

        self.assertIsInstance(fig, graphics.Figure)

    def test_draw_h2h_plot_image_reflectivity(self):

        """
        Test if newly generated plot image matches the reference used in
        README.md
        """

        img_path = "tests/test-img.png"

        graphics.draw_h2h_plot(
            self.standings.h2h_board_df,
            img_path
        )

        with open("examples/h2h_plot-example.png", "rb") as img:
            ref_img = img.read()

        with open("tests/test-img.png", "rb") as img:
            new_img = img.read()
        os.remove(img_path)

        self.assertEqual(ref_img, new_img)

    def test_stringify_h2h_standings_df(self) -> None:

        """
        Test if mock data produces the expected h2h standings string

        Since the expected output contains
        '1. <1st place> ... 2. <2nd place> ...' we can enumerate the team
        column in the mock data and subtest assert each leaderboard position
        """

        out = utils.stringify_h2h_standings_df(self.standings.h2h_standings_df)
        for ind, team in enumerate(self.standings.h2h_standings_df["team"]):

            with self.subTest():

                standing_row = str(ind + 1) + ". " + team
                self.assertIn(standing_row, out)
