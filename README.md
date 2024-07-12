[![GitHub](https://img.shields.io/github/license/kirandesilva/sleeper-h2h-tools.svg?color=blue)](https://github.com/kirandesilva/sleeper-h2h-tools/blob/main/LICENSE)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/kirandesilva/sleeper-h2h-tools/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/kirandesilva/sleeper-h2h-tools/tree/main)


# sleeper-h2h-tools
A niche Python API for calculating head-to-head metrics in Sleeper Fantasy Football leagues and delivering them through Discord webhook requests

# Table of Contents
0. [Foreword](#foreword)
1. [Installation](#installation)
2. [Usage](#usage)
3. [Dependencies](#dependencies)
4. [Development](#development)
5. [License](#license)

<a name="foreword"></a>

# Foreword
The need to develop this library arose from the lack of native head-to-head tiebreakers offered for Sleeper Fantasy Football leagues. Years ago, my own league opted to migrate from NFL to Sleeper while preserving our entire ruleset, including the NFL-standard head-to-head tiebreaking system. After years of creating head-to-head boards and adjusted standings by hand, I decided to write this library to divest myself of the monotony. Since my league's primary mode of communication is Discord, I also opted to include some wrappers for sending image and text webhook requests.

This library serves a niche and personal purpose, therefore it may not cover all edge cases. It has been tested only on traditional 10-team leagues with tiebreakers of size <4. I have little reason to extend this API beyond the scope of my own leagues, so I cannot guarantee compatibility with alternative formats like All-Play and Guillotine.

<a name="installation"></a>

# Installation
Be sure to have `poetry` installed for build and dependency management. It is highly recommended to install this library using `pipx`. See documentation for installation instructions [here](https://pipx.pypa.io/stable/installation/).

**Note**: do not use `pipx` to install libraries other than `poetry`

```bash
pipx install poetry
poetry build
pip install dist/sleeper_h2h_tools*.whl
```

<a name="usage"></a>

# Usage

## Standings
```python
from sleeper_h2h.standings import Standings

league_id = 01234
std = Standings(league_id)
std.make_h2h_board_df()
std.make_h2h_standings_df()
```
## Graphics
```python
from sleeper_h2h import graphics

img_path = 'img.png'
graphics.draw_h2h_plot(std.h2h_board_df, img_path)
```
## Discord
```python
from sleeper_h2h import discord, utils

hook = 'https://discord.com/api/webhooks/01234/ABCDE'
discord.send_image(hook, img_path)
discord.send_text(hook, utils.stringify_h2h_df(std.h2h_standings_df))
```

<a name="dependencies"></a>

# Dependencies

## Python Version
**> 3.10** required : see below for a list of critical versioned features included in this library
- **3.10** : union type hints using pipe `|` character
- **3.7** : dataclasses
- **3.5** : type hints

**Note**: theoretically, swapping union type hints from `X | Y` to `typing.Union[X, Y]` should make this library compatible as low as Python 3.7, but 3.10 is already 3 years old so I didn't bother. Beware of versioning requirements for external dependencies.

## External Libraries

**discord-webhook** : [GitHub](https://github.com/lovvskillz/python-discord-webhook) | [PyPI](https://pypi.org/project/discord-webhook/)

**jupyter** : [Docs](https://docs.jupyter.org/en/latest/) | [GitHub](https://github.com/jupyter/jupyter) | [PyPI](https://pypi.org/project/jupyter/)

**kaleido** : [GitHub](https://github.com/plotly/Kaleido) | [PyPI](https://pypi.org/project/kaleido/)

**numpy** : [Docs](https://numpy.org/doc/stable/user/index.html#user) | [GitHub](https://github.com/numpy/numpy) | [PyPI](https://pypi.org/project/numpy/)

**pandas** : [Docs](https://pandas.pydata.org/docs/user_guide/index.html) | [GitHub](https://github.com/pandas-dev/pandas) | [PyPI](https://pypi.org/project/pandas/)

**plotly** : [Docs](https://plotly.com/python/) | [GitHub](https://github.com/plotly/plotly.py) | [PyPI](https://pypi.org/project/plotly/)

**sleeper-api-wrapper** : [GitHub](https://github.com/dtsong/sleeper-api-wrapper) | [PyPI](https://pypi.org/project/sleeper-api-wrapper/)

<a name="development"></a>

# Development
The following command installs all package dependencies and the project library:
```bash
poetry install
```
If you want to install just the dependencies and not the project itself, you can use:
```bash
poetry install --no-root
```
See the `poetry` documentation for a full list of commands [here](https://python-poetry.org/docs/).

<a name="license"></a>

# License
This project is licensed under the terms of the MIT license.
