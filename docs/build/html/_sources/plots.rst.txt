
Plots
======================================

Being able to plot Splatoon data was the initial motivation on creating this package and I'll try to keep adding useful data visualizations as much as I can.


Matches History Panel
____________________________________________

This panel is constructed as a panel composed of two different figures. The top one is a detailed breakdown of the statistics of each battle.
Each column on the x axis represents a single battle; where the left y axis shows the number of kills, deaths, assists and specials; and the right y axis the turf painted over the match (bars on the plot).

.. image:: ../img/bHistory.png
  :width: 100%

Where the main vertical line between kills and deaths is colored blue for when the number of kills was equal or higher than deaths, and magenta for the other case.
Kills, deaths, assists and specials are encoded with the following symbols:

.. image:: ../img/LegendA.png
  :width: 15%


The bottom panel of the figure is subdivided into three lines. The top one represents the win/lose status of the battle, with the second one showing if the battle resulted in a KO:


.. image:: ../img/LegendB.png
  :width: 15%


Finally, the bottom row shows the type of match played:

.. image:: ../img/LegendC.png
  :width: 15%


Have a look at the `function's documentation <./SplatStats.html#module-SplatStats.plots>`_ for more information, and our `demo <https://github.com/Chipdelmal/SplatStats/tree/main/SplatStats/demos>`_  for an example on how to generate it.


Polar Barcharts
____________________________________________


These plots show the breakdown of a given statistic by category shown in a polar barchart. 
In the following examples we show kills+1/2*assists (kassists) by main weapon.


.. image:: ../img/polarKillsA.png
  :width: 49%

.. image:: ../img/polarKillsB.png
  :width: 49%



Stats By Match-Type and Stage
____________________________________________

These barcharts show the frequency of a given statistic broken down by match-type and stage.

.. image:: ../img/MatchesWin.png
  :width: 100%

.. image:: ../img/MatchesKill.png
  :width: 100%


Numbers in the barcharts show the true frequency (if the statistic is a fraction), and the main number in each panel shows the aggregate score amongst all the stages.


Stage/Weapon Stats Treemaps
____________________________________________

These plots are designed to show which stages are the ones in which the player performs best on any given stage with respect to a selected metric.
Auxiliary provided functions generate the statistics dataframe required for these plots, which includes: kills, deaths, win ratio, paint, total matches; amongst many others.
These statistics can be also generated for a specific match type (Rainmaker, Turf War, Tower Control, etc), or for a combination of them.

.. image:: ../img/treemapA.png
  :width: 50%

.. image:: ../img/treemapB.png
  :width: 50%


The functions to generate these treemaps were ultimately extended, so it is also possible to aggregate the stats by other keys such as weapons:

.. image:: ../img/treemapC.png
  :width: 50%

.. image:: ../img/treemapD.png
  :width: 50%


Have a look at the `function's documentation <./SplatStats.html#module-SplatStats.plots>`_ for more information, and our `demo <https://github.com/Chipdelmal/SplatStats/tree/main/SplatStats/demos>`_  for an example on how to generate these plots.


Kill VS Deaths Distributions
____________________________________________

These paired histograms show the frequency distributions of the number of kills or kassists (top, blue), and the number of deaths (bottom, magenta) across matches.

.. image:: ../img/kdHistogram.png
  :width: 100%

The x-asis shows the number of kills/deaths per match, while the y axis is either the raw frequency or the density of the quantity in that bin (if the histogram is normalized).  Have a look at the `function's documentation <./SplatStats.html#module-SplatStats.plots>`_ for more information, and our `demo <https://github.com/Chipdelmal/SplatStats/tree/main/SplatStats/demos>`_  for an example on how to generate these histograms.



Matches Ranks
____________________________________________


These plots show the player's results as compared to the other players in the match (left) and on the player's team (right).

.. image:: ../img/rankF.png
  :width: 49%

.. image:: ../img/rankA.png
  :width: 49%


The x axis is the rank, and the y axis is either the raw frequency of the player being rated that specific rank, or the frequency as a fraction of the total.


Awards BarChart
____________________________________________

A simple bar chart of the times awards have been given to the player.

.. image:: ../img/awards.png
  :width: 100%



Waffle Plot
____________________________________________


Shows the contributions of given categories to a certain stat. 
In this example, we show the total number of (kills+1/2*assists) broken down by weapon.

.. image:: ../img/waffle.png
  :width: 100%




Kill to Deaths Iris
____________________________________________

Similar to the `matches history panel <./plots.html#matches-history-panel>`_, these plots show the kill to death ratios as bars but this time they are arranged in a circular pattern to keep it more compact.

.. image:: ../img/IrisA.png
  :width: 33%

.. image:: ../img/IrisC.png
  :width: 33%

.. image:: ../img/IrisB.png
  :width: 33%

The radial axis is log-scaled by default with the kill+assist to deaths ratio highlighted at the center of the plot. 
The first 5 circles in the radial axis are spaced in increments of 1, while the latter ones are spaced in intervals of 10 by default.

