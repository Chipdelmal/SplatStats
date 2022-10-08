# SplatStats

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/SplatStats)](https://pypi.org/project/SplatStats)
[![PyPI version](https://badge.fury.io/py/SplatStats.svg)](https://badge.fury.io/py/SplatStats)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Chipdelmal/MGSurvE)

**UNDER DEVELOPMENT** 

This codebase works in tandem with the [s3s package](https://github.com/frozenpandaman/s3s) to refactor and analayze [Splatoon 3](https://en.wikipedia.org/wiki/Splatoon_3)'s data. When finished, it will be able to load [s3s package](https://github.com/frozenpandaman/s3s) `json` files, re-shape them, and visualize the data from battles history.


![](./docs/img/playerDF.png)

Have a look at our [documentation](https://chipdelmal.github.io/SplatStats/) for more information on how to install and use this package!

<hr>

## [Matches History Panel](https://chipdelmal.github.io/SplatStats/build/html/plots.html#matches-history-panel)

![](./docs/img/bHistory.png)

This panel is constructed as a panel composed of two different figures. The top one is a detailed breakdown of the statistics of each battle. Each column on the x axis represents a single battle; where the left y axis shows the number of kills, deaths, assists and specials; and the right y axis the turf painted over the match (bars on the plot).

## [Kills VS Deaths Distributions](https://chipdelmal.github.io/SplatStats/build/html/plots.html#matches-history-panel)

![](./docs/img/kdHistogram.png)

These paired histograms show the frequency distributions of the number of kills or kassists (top, blue), and the number of deaths (bottom, magenta) across matches.

## [Stage/Weapons Stats Treemaps](https://chipdelmal.github.io/SplatStats/build/html/plots.html#stats-treemaps)

<img src="./docs/img/treemapA.png" width="50%" align="middle"><img src="./docs/img/treemapB.png" width="50%" align="middle">

These plots are designed to show which stages are the ones in which the player performs best on any given stage with respect to a selected metric. Auxiliary provided functions generate the statistics dataframe required for these plots, which includes: kills, deaths, win ratio, paint, total matches; amongst many others. These statistics can be also generated for a specific match type (Rainmaker, Turf War, Tower Control, etc), or for a combination of them.

<!-- <img src="./docs/img/treemapD.png" width="50%" align="middle"><img src="./docs/img/treemapC.png" width="50%" align="middle"> -->

Moreover, these plots can be generated for any arbitrary key in the dataframe: main weapon, sub weapon, head gear, etc.

## [Kill/Death Iris](https://chipdelmal.github.io/SplatStats/build/html/plots.html#kill-to-deaths-iris)

<img src="./docs/img/IrisA.png" width="33%" align="middle"><img src="./docs/img/IrisC.png" width="33%" align="middle"><img src="./docs/img/IrisB.png" width="33%" align="middle">

Similar to the [matches history panel](https://chipdelmal.github.io/SplatStats/build/html/plots.html#matches-history-panel), these plots show the kill to death ratios as bars but this time they are arranged in a circular pattern to keep it more compact. The radial axis is log-scaled by default with the kill+assist to deaths ratio highlighted at the center of the plot.

## Coming Soon!

<img src="./docs/img/waffle.png" width="99%" align="middle"><br>


# Author

I'll be writing a [blogpost on my website](http://chipdelmal.github.io) with more information about the development, planned features, and some analyses on my own Splatoon matches data!

<img src="./docs/img/chip.jpg" height="250px" align="middle">

[Héctor M. Sánchez C.](http://chipdelmal.github.io)
