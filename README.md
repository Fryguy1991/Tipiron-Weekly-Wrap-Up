# Tippy Wrap-Up Data Puller

This is a quick and dirty Python script to pull Tipiron player/matchup data for the week you specify!

## Instructions to pull data

1. Download and install [python](https://www.python.org/downloads/), ensure you set the required [environment variables](https://docs.python.org/3/using/windows.html). 

1. Checkout this repository.

1. Open a command prompt terminal at the root of this repository.

1. Run the following terminal command: 
`python -m pip install requests`

1. Run the player data puller script: 
`python player-data-puller.py` 
__THIS DOES NOT NEED TO BE RUN OFTEN, RECOMMEND ONCE A DAY AT MOST!__

1. Ensure the file `playerData.json` now exists in the root of the repository.

1. Run the wrap up data puller script: 
`python wrap-up-data-puller.py`.

1. When prompted, enter the week you'd like wrap up data for.

The weekly wrap up lists you're interested in should print to the terminal. You can copy them from there.