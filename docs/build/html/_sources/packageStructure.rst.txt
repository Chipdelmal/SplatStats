Code Structure
======================================

Player
---------------------

The uppermost level class is the `Player`. 
Most of the time we will be dealing with this class, as it is the one that encapsulates the `Battle` objects and provides with the most interfaces to handle and analyze the data.


Battle
---------------------


Team Dataframe 
_________________________

The results of a team that was part of a battle are stored in a dataframe object.

* `player name:` Player's name used in the match
* `player name id:` Player's in-game id
* `main weapon:` Main weapon used
* `sub weapon:` Sub weapon used
* `special weapon:` Special weapon used
* `kill:` Kill count
* `death:` Death count
* `assist:` Number of assists
* `special:` Number of specials
* `paint:` Painted surface
* `head name:` Headgear's name
* `head main:` Headgear's main ability
* `head sub_0:` Headgear's sub ability @ slot 1
* `head sub_1:` Headgear's sub ability @ slot 2
* `head sub_2:` Headgear's sub ability @ slot 3
* `shirt name:` Shirtgear's name
* `shirt main:` Shirtgear's main ability
* `shirt sub_0:` Shirtgear's sub ability @ slot 1
* `shirt sub_1:` Shirtgear's sub ability @ slot 2
* `shirt sub_2:` Shirtgear's sub ability @ slot 3
* `shoes name:` Shoesgear's name
* `shoes main:` Shoesgear's main ability
* `shoes sub_0:` Shoesgear's sub ability @ slot 1
* `shoes sub_1:` Shoesgear's sub ability @ slot 2
* `shoes sub_2:` Shoesgear's sub ability @ slot 3
* `self:` Is this player the one who generated the dataset?
* `win:` Win (W), Lose (L) or not finished (NA)
* `score:` Score obtained in the match (if "Turf War", this stat is "paint"; and if the match did not finish correctly the variable takes a value of `False`)



.. Awards Dataframe

.. https://www.gamepur.com/guides/all-multiplayer-medals-in-splatoon-3-and-what-they-mean
.. * `name`: Name of the award
.. * `rank`: Gold/Silver rank
.. * `place`: Placing in top 


Auxiliary Routines
---------------------
