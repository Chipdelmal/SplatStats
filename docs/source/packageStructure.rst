
Data Structures
======================================

Player
---------------------

The uppermost level class is the `Player`. 
Most of the time we will be dealing with this class, as it is the one that encapsulates the `Battle` objects and provides with the most interfaces to handle and analyze the data.


Battle
---------------------


Team/Enemy Dataframe 
_________________________

The results of a team that was part of a battle are stored in a dataframe object.

* :code:`player name` Player's name used in the match
* :code:`player name id` Player's in-game id
* :code:`main weapon` Main weapon used
* :code:`sub weapon` Sub weapon used
* :code:`special weapon` Special weapon used
* :code:`kill` Kill count
* :code:`death` Death count
* :code:`assist` Number of assists
* :code:`special` Number of specials
* :code:`paint` Painted surface
* :code:`head name` Headgear's name
* :code:`head main` Headgear's main ability
* :code:`head sub_0` Headgear's sub ability @ slot 1
* :code:`head sub_1` Headgear's sub ability @ slot 2
* :code:`head sub_2` Headgear's sub ability @ slot 3
* :code:`shirt name` Shirtgear's name
* :code:`shirt main` Shirtgear's main ability
* :code:`shirt sub_0` Shirtgear's sub ability @ slot 1
* :code:`shirt sub_1` Shirtgear's sub ability @ slot 2
* :code:`shirt sub_2` Shirtgear's sub ability @ slot 3
* :code:`shoes name` Shoesgear's name
* :code:`shoes main` Shoesgear's main ability
* :code:`shoes sub_0` Shoesgear's sub ability @ slot 1
* :code:`shoes sub_1` Shoesgear's sub ability @ slot 2
* :code:`shoes sub_2` Shoesgear's sub ability @ slot 3
* :code:`self` Is this player the one who generated the dataset?
* :code:`win` Win (W), Lose (L) or not finished (NA)
* :code:`score` Score obtained in the match (if "Turf War", this stat is "paint"; and if the match did not finish correctly the variable takes a value of `False`)


Stats
---------------------

SplatStats can automatically calculate the some statistics from either a player object, or from the battles stored in a battle dataframe. 
In general, calculated stats revolve around the following numbers:

* **K** ills: Times you've splatted an enemy.
* **P** aint: Amount of terrain painted.
* **A** ssists: Times you've helped someone else splat an enemy.
* **D** eaths: Times an enemy has splatted you.
* **S** pecial: Times you've used your special.


With an additional metric called "kassists", that combines kills and assists in a single number following this equation:

.. math::

   kassists = kills + (0.5 * assists)


The output data structure follows this shape (either for the player, or the dataframe object):

.. code-block::

    {
        'general': {
            'total matches': Number of matches
            'win': Wins out of total matches
            'loss': Losses out of total matches
            'paint': Total painted surface
            'win ratio': Fraction of the matches that resulted in wins
            'kill ratio': Number of kills divided by deaths
            'kassists ratio': Number of kassists divided by deaths
        },
        'kpads': {
            'kills': Total kills
            'deaths': Total deaths
            'assists': Total assists 
            'kassists': Total kassists
            'special': Total specials used
            'paint': Total painted surface
        }
        'kpads avg': {
            'kills': Average kills per match
            'deaths': Average deaths per match
            'assists': Average assists per match
            'kassists': Average kassists per match
            'special': Average specials used per match
            'paint': Average painted surface per match
        }
        'kpads per min': {
            'kills': Kills per minute 
            'deaths': Deaths per minute
            'assists': Assists per minute
            'kassists': Kassists per minute
            'special': Specials used per minute
            'paint': Painted surface per minute
        }
    }

As stated in the structure's entries descriptions, the average quantities are calculated on a "per match" basis; and the "per minute" stats are calculated by dividing the aggregate quantity over the total time spent in matches.


.. Awards Dataframe

.. https://www.gamepur.com/guides/all-multiplayer-medals-in-splatoon-3-and-what-they-mean
.. * `name`: Name of the award
.. * `rank`: Gold/Silver rank
.. * `place`: Placing in top 

