
Plots
======================================


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


Have a look at the `function's documentation <./SplatStats.html#module-SplatStats.plots>`_ for more information.



Kill VS Deaths Distributions
____________________________________________

These paired histograms show the frequency distributions of the number of kills or kassists (top, blue), and the number of deaths (bottom, magenta) across matches.

.. image:: ../img/kdHistogram.png
  :width: 100%

The x-asis shows the number of kills/deaths per match, while the y axis is either the raw frequency or the density of the quantity in that bin (if the histogram is normalized). 
Have a look at the `function's documentation <./SplatStats.html#module-SplatStats.plots>`_ for more information.


