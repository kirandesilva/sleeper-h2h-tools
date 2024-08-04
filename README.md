[![License](https://img.shields.io/github/license/kirandesilva/sleeper-h2h-tools.svg?color=blue)](https://github.com/kirandesilva/sleeper-h2h-tools/blob/main/LICENSE)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/kirandesilva/sleeper-h2h-tools/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/kirandesilva/sleeper-h2h-tools/tree/main)
![Tests](https://raw.githubusercontent.com/kirandesilva/sleeper-h2h-tools/badges/badges/tests.svg)
![Coverage](https://raw.githubusercontent.com/kirandesilva/sleeper-h2h-tools/badges/badges/coverage.svg)

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

**Note**: Do not use `pipx` to install libraries other than `poetry` unless you know what you are doing.

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
std.make_h2h_standings_df()

# default Sleeper standings
std.standings_df
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>team</th>
      <th>wins</th>
      <th>losses</th>
      <th>points</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Foxes</td>
      <td>12</td>
      <td>3</td>
      <td>1650.94</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Echidnas</td>
      <td>11</td>
      <td>4</td>
      <td>1819.82</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Beavers</td>
      <td>9</td>
      <td>6</td>
      <td>1614.42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Giraffes</td>
      <td>8</td>
      <td>7</td>
      <td>1610.38</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Aardvarks</td>
      <td>7</td>
      <td>8</td>
      <td>1631.98</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Iguanas</td>
      <td>7</td>
      <td>8</td>
      <td>1556.74</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Dingos</td>
      <td>7</td>
      <td>8</td>
      <td>1532.60</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Hyenas</td>
      <td>5</td>
      <td>10</td>
      <td>1533.02</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Cicadas</td>
      <td>4</td>
      <td>10</td>
      <td>1532.28</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Jackals</td>
      <td>4</td>
      <td>10</td>
      <td>1426.38</td>
    </tr>
  </tbody>
</table>
</div>

```python
# head-to-head winrate board
std.h2h_board_df
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Foxes</th>
      <th>Echidnas</th>
      <th>Beavers</th>
      <th>Giraffes</th>
      <th>Aardvarks</th>
      <th>Iguanas</th>
      <th>Dingos</th>
      <th>Hyenas</th>
      <th>Cicadas</th>
      <th>Jackals</th>
      <th>points</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Foxes</th>
      <td>NaN</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1650.94</td>
    </tr>
    <tr>
      <th>Echidnas</th>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1819.82</td>
    </tr>
    <tr>
      <th>Beavers</th>
      <td>1.0</td>
      <td>0.5</td>
      <td>NaN</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>1614.42</td>
    </tr>
    <tr>
      <th>Giraffes</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>1610.38</td>
    </tr>
    <tr>
      <th>Aardvarks</th>
      <td>1.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>1631.98</td>
    </tr>
    <tr>
      <th>Iguanas</th>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>1556.74</td>
    </tr>
    <tr>
      <th>Dingos</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>1532.60</td>
    </tr>
    <tr>
      <th>Hyenas</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>1533.02</td>
    </tr>
    <tr>
      <th>Cicadas</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>0.5</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>1532.28</td>
    </tr>
    <tr>
      <th>Jackals</th>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.5</td>
      <td>1.0</td>
      <td>NaN</td>
      <td>1426.38</td>
    </tr>
  </tbody>
</table>
</div>

```python
# head-to-head adjusted standings
std.h2h_standings_df
```
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>team</th>
      <th>h2h_delta</th>
      <th>wins</th>
      <th>losses</th>
      <th>points</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Foxes</td>
      <td>0</td>
      <td>12</td>
      <td>3</td>
      <td>1650.94</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Echidnas</td>
      <td>0</td>
      <td>11</td>
      <td>4</td>
      <td>1819.82</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Beavers</td>
      <td>0</td>
      <td>9</td>
      <td>6</td>
      <td>1614.42</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Giraffes</td>
      <td>0</td>
      <td>8</td>
      <td>7</td>
      <td>1610.38</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Iguanas</td>
      <td>1</td>
      <td>7</td>
      <td>8</td>
      <td>1556.74</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Aardvarks</td>
      <td>-1</td>
      <td>7</td>
      <td>8</td>
      <td>1631.98</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Dingos</td>
      <td>0</td>
      <td>7</td>
      <td>8</td>
      <td>1532.60</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Hyenas</td>
      <td>0</td>
      <td>5</td>
      <td>10</td>
      <td>1533.02</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Jackals</td>
      <td>1</td>
      <td>4</td>
      <td>10</td>
      <td>1426.38</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Cicadas</td>
      <td>-1</td>
      <td>4</td>
      <td>10</td>
      <td>1532.28</td>
    </tr>
  </tbody>
</table>
</div>

## Graphics
```python
from sleeper_h2h import graphics

img_path = 'img.png'
graphics.draw_h2h_plot(std.h2h_board_df, img_path).show()
```
![h2h_plot-example](https://raw.githubusercontent.com/kirandesilva/sleeper-h2h-tools/main/examples/h2h_plot-example.png)

It should be read like a DataFrame, where each row represents a team's winrate against other teams. Green indicates a winrate above .500 for a given head-to-head matchup, red indicates below .500, and yellow indicates exactly .500.

In this example, Foxes have a perfect winrate against all other teams except Beavers and Aardvarks.

### Known Limitation

The color map supplied by `draw_h2h_plot()` maps green, yellow, and red to winrates of 1.000, 0.500, and 0.000, respectively. Since most league formats prevent more than 2 occurences of unique matchups per season, this was left alone. With 3+ occurrences, winrates of 0.000 - 0.250 and 0.750 - 1.000 are possible and would not render properly.

## Discord
```python
from sleeper_h2h import discord, utils

hook = 'https://discord.com/api/webhooks/01234/ABCDE'
msg = utils.stringify_h2h_standings_df(std.h2h_standings_df)

discord.send_image(hook, img_path)
discord.send_text(hook, msg)
```
Below is how the message would appear in a Discord server or Python's `print()` output:
```md
Here are your Week 16 H2H-adjusted standings:

1. Foxes
2. Echidnas
3. Beavers
4. Giraffes
5. Iguanas (+1)
6. Aardvarks (-1)
7. Dingos
8. Hyenas
9. Jackals (+1)
10. Cicadas (-1)
```

<a name="dependencies"></a>

# Dependencies

## Python Version
**>= 3.10** required : see below for a list of critical versioned features included in this library
- **3.10** : union type hints using pipe `|` character
- **3.7** : dataclasses
- **3.5** : type hints

**Note**: theoretically, swapping union type hints from `X | Y` to `typing.Union[X, Y]` should make this library compatible as low as Python 3.7, but 3.10 is already 3 years old so I didn't bother. Beware of versioning requirements for external dependencies.

## Core Dependencies

**discord-webhook** : [GitHub](https://github.com/lovvskillz/python-discord-webhook) | [PyPI](https://pypi.org/project/discord-webhook/)

**kaleido** : [GitHub](https://github.com/plotly/Kaleido) | [PyPI](https://pypi.org/project/kaleido/)

**numpy** : [Docs](https://numpy.org/doc/stable/user/index.html#user) | [GitHub](https://github.com/numpy/numpy) | [PyPI](https://pypi.org/project/numpy/)

**pandas** : [Docs](https://pandas.pydata.org/docs/user_guide/index.html) | [GitHub](https://github.com/pandas-dev/pandas) | [PyPI](https://pypi.org/project/pandas/)

**plotly** : [Docs](https://plotly.com/python/) | [GitHub](https://github.com/plotly/plotly.py) | [PyPI](https://pypi.org/project/plotly/)

**sleeper-api-wrapper** : [GitHub](https://github.com/dtsong/sleeper-api-wrapper) | [PyPI](https://pypi.org/project/sleeper-api-wrapper/)

## Testing Dependencies

**coverage** : [Docs](https://coverage.readthedocs.io/en/latest/) |  [GitHub](https://github.com/nedbat/coveragepy) | [PyPI](https://pypi.org/project/coverage/)

**genbadge** : [Docs](https://smarie.github.io/python-genbadge/) | [GitHub](https://github.com/smarie/python-genbadge) | [PyPI](https://pypi.python.org/pypi/genbadge/)

**pytest** : [Docs](https://docs.pytest.org/en/stable/contents.html) | [GitHub](https://github.com/pytest-dev/pytest/) | [PyPI](https://pypi.org/project/pytest/)

<a name="development"></a>

# Development
The following command installs all core package dependencies and the project library:
```bash
poetry install
```
To avoid installing the project library, use the `--no-root` flag, for example:
```bash
poetry install --no-root
```
To install testing dependencies, supply `--with test` to the `install` command, for example:
```bash
poetry install --with test
```
This is typically all that is required to continue to testing. Otherwise, see the `poetry` documentation for a full list of commands [here](https://python-poetry.org/docs/).

After installing testing dependencies, check out the `Makefile` for some handy `make` invocations.

## OS Compatibility

This project is being developed on Apple M2 architechture. All local testing occurs on both macOS arm64 and Ubuntu 22.04 arm64. The Linux machine is provisioned using [Vagrant](https://www.vagrantup.com/) and [VMware Fusion](https://www.vmware.com/products/desktop-hypervisor.html), using the latest `bento/ubuntu-22.04` arm64 [image](https://app.vagrantup.com/bento/boxes/ubuntu-22.04). I have used VirtualBox for years and tried to make it work, but their arm64 support is lackluster. VMware Fusion personal licenses are free.

In the CircleCI pipeline, testing occurs on an Ubuntu 22.04 amd64 Linux machine, running the `cimg/python:3.10.14` image. See image specifics at [CircleCI docs](https://circleci.com/developer/images/image/cimg/python) and [Docker Hub](https://hub.docker.com/r/cimg/python).

There is currently no testing in Windows environments, as I do not interface with it casually nor do I expect many Fantasy Football users to.

<a name="license"></a>

# License
This project is distributed under the terms of the [MIT license](https://github.com/kirandesilva/sleeper-h2h-tools/blob/main/LICENSE).
