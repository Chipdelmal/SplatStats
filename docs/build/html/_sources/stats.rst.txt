
Stats
======================================


* **K** ills:
* **P** aint:
* **A** ssists:
* **D** eaths:
* **S** pecial:


With an additional metric called "kassists", that combines kills and assists in a single number following this equation:

.. math::

   kassists = kills + (0.5 * assists)



.. code-block::

    {
        'general': {
            'total matches':
            'win':
            'loss':
            'paint':
            'win ratio':
            'kill ratio':
            'kassists ratio':
        },
        'kpads': {
            'kills':
            'deaths':
            'assists':
            'kassists':
            'special':
            'paint':
        }
        'kpads avg': {
            'kills':
            'deaths':
            'assists':
            'kassists':
            'special':
            'paint':
        }
        'kpads per min': {
            'kills':
            'deaths':
            'assists':
            'kassists':
            'special':
            'paint':
        }
    }