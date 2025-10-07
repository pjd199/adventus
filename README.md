# adventus

_Adventus_ is a command line utility (CLI) for downloading puzzle input files
for Advent of Code (AOC). File can also be accesses within the code using the 
fetch function. 

```python
from adventus import fetch

input_data = fetch(day=1,year=2015)
```

The files are cached to reduce the number of requests to the AOC server,
as required within the 
[AOC automation guidelines](https://www.reddit.com/r/adventofcode/wiki/faqs/automation)

## Basic Usage

```sh
adventus {day} {year} {--fetch} {--submit}
```

## Full Usage

```sh
usage: adventus [-h] [--fetch] [--submit]
                [{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25}]
                [{2015,2016,2017,2018,2019,2020,2021,2022,2023,2024}]

Download input file from the Advent of Code website.

positional arguments:
  {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25}
                        the day of the puzzle input to download
  {2015,2016,2017,2018,2019,2020,2021,2022,2023,2024}
                        the year of the puzzle input to download

options:
  -h, --help            show this help message and exit
  --fetch               fetch the puzzle input
  --submit              submit the puzzle answers
```

## Word Origin
_adventus_ is the Latin root for the word Advent,
which means arrival. 
