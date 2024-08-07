"""
Dataclasses supporting head-to-head tiebreaker calculations for Sleeper
Fantasy Football leagues
"""

from dataclasses import dataclass, field

import numpy as np
from pandas import DataFrame, concat, get_dummies
from sleeper_wrapper import League

from . import utils


@dataclass
class Metadata:

    """
    Stores metadata for the Standings class in order to reduce attribute burden

    ATTRIBUTES
    ----------
    __league_id : int | str
        the ID of the Sleeper Fantasy Football league

    league : League, default=None
        `League` object instance

    __rosters : list[dict], default=[]
        `League.get_rosters()` instance

    __users : list[dict], default=[]
        `League.get_users()` instance

    standings : list[tuple], default=[]
        `League.get_standings()` instance; the return type hint provided by
        the sleeper_wrapper library is incorrect, but its docstring is

    user_id_team_map : dict, default={}
        Dictionary mapping user ID to team name; essentially merges the returns
        of `League.map_rosterid_to_ownerid()` and
        `League.map_users_to_team_name()`

    week : int, default=None
        the current week of the season; simply wins + losses + 1 for the first
        place team
    """

    __league_id: int | str
    league: League = field(init=False, default=None)
    __rosters: list[dict] = field(init=False, default_factory=list)
    __users: list[dict] = field(init=False, default_factory=list)
    standings: list[tuple] = field(init=False, default_factory=list)
    user_id_team_map: dict = field(init=False, default_factory=dict)
    week: int = field(init=False, default_factory=int)

    def __post_init__(self) -> None:

        """
        Initialize League metadata attributes
        """

        self.league = League(self.__league_id)
        self.__rosters = self.league.get_rosters()
        self.__users = self.league.get_users()
        self.standings = self.league.get_standings(
            self.__rosters,
            self.__users
        )
        self.user_id_team_map = utils.merge_users_and_teams(
            self.league.map_rosterid_to_ownerid(self.__rosters),
            self.league.map_users_to_team_name(self.__users)
        )


@dataclass
class Standings:

    """
    A class representing a League's standings according to head-to-head
    tiebreaker rules

    ATTRIBUTES
    ----------
    league_id : int | str
        the ID of the Sleeper Fantasy Football league

    _metadata : Metadata, default=None
        `Metadata` object instance

    _standings_df : DataFrame, default=DataFrame()
        DataFrame of the current standings, sorted by wins then points; this is
        generated entirely by the `sleeper_wrapper` library which uses rounding
        for points

    standings_df : DataFrame, default=DataFrame()
        DataFrame of the current standings, sorted by wins then points; this
        uses `_standings_df` as a reference but instead calculates points by
        iterating over weekly matchups, resulting in no rounding

    h2h_board_df : DataFrame, default=DataFrame()
        DataFrame of the head-to-head winrate board; read rowwise, each cell
        represents the winrate of the row index's team against teams in the
        columns; points are in the last column

    h2h_standings_df : DataFrame, default=DataFrame()
        DataFrame of the current standings, sorted by wins, then head-to-head
        rules, then points; copy of `standings_df` and modified it according to
        `h2h_board_df`
    
    METHODS
    -------
    __get_standings_df_rounded_points(standings)
        returns a DataFrame of the current standings with rounded points;
        assigns `_standings_df`

    _get_standings_df_exact_points()
        returns a DataFrame of the current standings with exact points;
        assigns `standings_df`

    make_h2h_board_df()
        generates head-to-head winrate DataFrame from class instance;
        assigns `h2h_board_df`

    make_h2h_standings_df()
        generates a DataFrame of the current standings with head-to-head
        adjustments applied; assigns `h2h_standings_df`

    """

    league_id: int | str
    _metadata: Metadata = field(default=None)
    _standings_df: DataFrame = field(init=False, default_factory=DataFrame)
    standings_df: DataFrame = field(init=False, default_factory=DataFrame)
    h2h_board_df: DataFrame = field(init=False, default_factory=DataFrame)
    h2h_standings_df: DataFrame = field(init=False, default_factory=DataFrame)

    def __post_init__(self) -> None:

        """
        Initialize the Metadata object and rounded standings generated purely
        by `sleeper_wrapper`
        """

        if not self._metadata:
            self._metadata = Metadata(self.league_id)
        self._standings_df = self.__get_standings_df_rounded_points(
            self._metadata.standings
        )

    def __get_standings_df_rounded_points(
            self,
            standings: list[tuple]
        ) -> DataFrame:

        """
        Returns a DataFrame directly from `League.get_standings()` which
        uses integer rounding for point calculations

        This method should only be internally called by `__post_init__()` and
        it assigns the attribute `self._standings_df`
        """

        df = DataFrame(standings, columns=["team", "wins", "losses", "points"])
        df["team"] = df["team"].apply(utils.remove_emojis)

        self._metadata.week = int(df.iloc[0]["wins"]) +\
            int(df.iloc[0]["losses"]) + 1

        return df

    def _get_standings_df_exact_points(self) -> DataFrame:

        """
        Returns a DataFrame representation of `League.get_standings()` but
        without any rounding for point calculations; achieved by iterating over
        weekly matchups

        This is internally called by `self.make_h2h_board_df()`
        """

        user_id_df = DataFrame(
            self._metadata.user_id_team_map,
            index=["team"]
        ).T.reset_index(names="user_id")

        standings_df = self._standings_df.copy(deep=True)\
            .merge(user_id_df, how="left", on="team")\
            .drop(columns="points").set_index("user_id")

        tot_pts = DataFrame(index=standings_df["team"])

        for j in range(1, self._metadata.week):
            d = {}

            for i in self._metadata.league.get_matchups(j):
                d.update(
                    {
                        self._metadata.user_id_team_map[i["roster_id"]]:
                        (i["matchup_id"], i["points"])
                    }
                )

            weekly_scores_df = DataFrame(
                [
                    {
                        "team": team,
                        "matchup": matchup,
                        f"wk_{j}_score": score
                    }
                    for team, (matchup, score) in d.items()
                ]
            ).set_index("team")

            tot_pts = tot_pts.merge(
                weekly_scores_df.drop(columns="matchup"),
                right_index=True,
                left_index=True
            )

        tot_pts = tot_pts.iloc[:,].sum(axis=1).reset_index(drop=False)
        tot_pts.columns = ["team", "points"]
        tot_pts = tot_pts.merge(
            standings_df.reset_index(drop=True),
            on="team"
        )

        return tot_pts[["team", "wins", "losses", "points"]]

    def make_h2h_board_df(self) -> None:
        # pylint: disable=E1136,E1137
        # disable unsubscriptable and unsupported assignment pylint errors

        """
        Generates a DataFrame representing the head-to-head breakdown of a
        Standings object

        The DataFrame shows an `(n)`x`(n+1)` matrix where `n` = league size

        The rows, labeled by the index, represent a given team's head-to-head
        winrate against all other teams

        Assigns attributes `self.standings_df` and `self.h2h_board_df`
        """

        if self.standings_df.empty:
            self.standings_df = self._get_standings_df_exact_points()

        wr_df = DataFrame(columns=["winners", "losers"])

        for j in range(1, self._metadata.week):
            d = {}

            for i in self._metadata.league.get_matchups(j):
                d.update(
                    {
                        self._metadata.user_id_team_map[i["roster_id"]]:
                        (i["matchup_id"], i["points"])
                    }
                )

            weekly_scores_df = DataFrame(
                [
                    {
                        "team": team,
                        "matchup": matchup,
                        f"wk_{j}_score": score
                    }
                    for team, (matchup, score) in d.items()
                ]
            ).set_index("team")

            is_winner = weekly_scores_df.groupby('matchup')[f"wk_{j}_score"]\
                .transform('max') == weekly_scores_df[f"wk_{j}_score"]

            weekly_scores_df['result'] = np.where(
                is_winner.values,
                'beat',
                'lost'
            )

            matchup_pairs_df = weekly_scores_df[["result", "matchup"]]\
                .query("result == 'beat'").reset_index(drop=False)\
                .merge(weekly_scores_df[["matchup", "result"]]\
                .query("result == 'lost'").reset_index(drop=False)\
                .drop(columns="result"), on="matchup")\
                .drop(columns=["matchup", "result"])\
                .rename(columns={"team_x": "winners", "team_y": "losers"})

            wr_df = concat(
                [
                    wr_df,
                    matchup_pairs_df
                ],
                ignore_index=True
            ).reset_index(drop=True)

        teams = self.standings_df["team"].to_list()

        bools = wr_df.pivot(columns=['losers'], values=['winners'])\
            .droplevel(0, axis=1).reindex(teams, axis=1).notna()
        bools.index = bools.index.map(wr_df['winners'])

        summed_on_idx = bools.groupby(bools.index).sum()
        summed_on_idx = summed_on_idx.reindex(teams).fillna(0)

        matrix = summed_on_idx/summed_on_idx.add(summed_on_idx.T)
        matrix.columns.name = None

        out = matrix.merge(
            self.standings_df.set_index("team"),
            left_index=True,
            right_index=True
        ).drop(columns=["wins", "losses"])

        self.h2h_board_df = out

    def make_h2h_standings_df(self) -> None:

        """
        Generates new head-to-head adjusted standings from existing 
        `self.h2h_board_df` and `self.standings_df` attributes, with an
        additional column noting the leaderboard deltas for affected teams

        Assigns attribute `self.h2h_standings_df`
        """

        if self.h2h_board_df.empty:
            self.make_h2h_board_df()

        h2h_board_df = self.h2h_board_df.copy(deep=True)
        standings_df = self.standings_df.copy(deep=True)

        h2h_board_df = h2h_board_df.T.iloc[:-1]
        tiebreaks = []

        for team in h2h_board_df:
            tiebreaks.append(
                [
                    ind for ind, row in h2h_board_df[[team]].iterrows() if
                    row[team] == 1
                ]
            )

        standings_df["tiebreaks"] = tiebreaks
        out = []

        for _, row in standings_df.iterrows():
            team = row["team"]
            if team not in out:
                wins = row["wins"]
                ties = standings_df.query(f"wins == '{wins}'").copy(deep=True)

                if len(ties) > 1:
                    dummies = get_dummies(ties["tiebreaks"].explode()).\
                        groupby(level=0).sum()
                    tie_dummies = ties.merge(
                        dummies,
                        left_index=True,
                        right_index=True
                    )

                    for team in tie_dummies["team"]:
                        if team not in tie_dummies.columns:
                            tie_dummies[team] = [0] * len(tie_dummies)

                    sorted_ties = tie_dummies.sort_values(
                        by=tie_dummies["team"].to_list(),
                        ascending=[False]*len(tie_dummies)
                    )["team"].to_list()
                    out += sorted_ties

                else:
                    out.append(team)

        out_df = DataFrame(out, columns=["team"])
        out_df["h2h_delta"] = [
            standings_df[standings_df["team"] == team].\
                index.values.astype(int)[0] -\
            out_df[out_df["team"] == team].\
                index.values.astype(int)[0]
            for team in out_df["team"]
        ]

        self.h2h_standings_df = out_df.merge(
            standings_df[["team", "wins", "losses", "points"]],
            on="team"
        )
