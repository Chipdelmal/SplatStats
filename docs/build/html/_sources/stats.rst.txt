
Stats
======================================

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