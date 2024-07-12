"""
Utility functions that support sleeper-h2h-tools
"""

import re

from pandas import DataFrame

def remove_emojis(data: str) -> str:

    """
    Removes emojis and other symbols from a string, then strips whitespace

    PARAMETERS
    ----------
    data : str
        string to be stripped of emojis

    RETURNS
    -------
    stripped : str
        input string stripped of emojis then of whitespace
    """

    emojis = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        re.UNICODE)
    return re.sub(emojis, '', data).strip()

def merge_users_and_teams(dict_1: dict, dict_2: dict) -> dict:

    """
    Left joins 2 dictionaries where the values of the first and the keys of the
    second are the attribute to merge on; uses DataFrames to accomplish this

    PARAMETERS
    ----------
    dict_1 : dict
        dictionary to reference in left join; the keys will be preserved in the
        output

    dict_2 : dict
        dictionary to merge with in left join; the values will be preserved in
        the output

    RETURNS
    -------
    merged : dict
        dictionary where the keys and values correspond to `dict_1` and
        `dict_2` respectively; the merged column is not preserved
    """

    df_1 = DataFrame(dict_1.items(), columns=["keys", "merge"])
    df_2 = DataFrame(dict_2.items(), columns=["merge", "values"])

    return df_1.merge(df_2, on="merge").set_index("keys")["values"]\
        .apply(remove_emojis).to_dict()

def stringify_h2h_df(df: DataFrame) -> str:

    """
    Parses an h2h DataFrame from a Standings object into a pretty string
    for delivery via Discord webhook request

    PARAMETERS
    ----------
    df : DataFrame
        DataFrame from Standings.h2h_standings_df, which comes from
        Standings.make_h2h_adjusted_standings_df()

    RETURNS
    -------
    output : str
        A pretty string representation of `df` to send via Discord webhook
        request
    """

    week = int(df.iloc[0]["wins"]) + int(df.iloc[0]["losses"]) + 1
    output = f"Here are your Week {week}" +\
        " H2H-adjusted standings:\n\n"

    for ind, row in df.iterrows():
        out = f"{int(ind)+1}. {row['team']}"
        if row["h2h_delta"] != 0:
            out += f" ({row['h2h_delta']:+})"

        out += "\n"
        output += out

    return output
