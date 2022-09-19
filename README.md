# SplatStats

**UNDER DEVELOPMENT** 

This codebase is meant to work in tandem with the [s3s package](https://github.com/frozenpandaman/s3s) to refactor and analayze [Splatoon 3](https://en.wikipedia.org/wiki/Splatoon_3)'s data. When finished, it will be able to take exported `json` files, re-shape them, and visualize the data from battles history.

## Instructions

**Downloading data**: Install s3s as explained [here](https://github.com/frozenpandaman/s3s), then download stats jsons by running: `python s3s.py -o`

## Data Structures

### Battle Object

#### Teams Dataframe

* `player name`: Player's name used in the match
* `player name id`: Player's in-game id
* `main weapon`: Main weapon used
* `sub weapon`: Sub weapon used
* `special weapon`: Special weapon used
* `kill`: Kill count
* `death`: Death count
* `assist`: Number of assists
* `special`: Number of specials
* `paint`: Painted surface
* `head name`: Headgear's name
* `head main`: Headgear's main ability
* `head sub_0`: Headgear's sub ability @ slot 1
* `head sub_1`: Headgear's sub ability @ slot 2
* `head sub_2`: Headgear's sub ability @ slot 3
* `shirt name`: Shirtgear's name
* `shirt main`: Shirtgear's main ability
* `shirt sub_0`: Shirtgear's sub ability @ slot 1
* `shirt sub_1`: Shirtgear's sub ability @ slot 2
* `shirt sub_2`: Shirtgear's sub ability @ slot 3
* `shoes name`: Shoesgear's name
* `shoes main`: Shoesgear's main ability
* `shoes sub_0`: Shoesgear's sub ability @ slot 1
* `shoes sub_1`: Shoesgear's sub ability @ slot 2
* `shoes sub_2`: Shoesgear's sub ability @ slot 3
* `self`: Is this player the one who generated the dataset?
* `win`: Win (W), Lose (L) or not finished (NA)
* `score`: Score obtained in the match (if "Turf War", this stat is "paint"; and if the match did not finish correctly, it is `False`)

#### Awards Dataframe

* `name`: Name of the award
* `rank`: Gold/Silver rank
* `place`: Placing in top