# Ascii Etch [![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause) [![Build Status](https://travis-ci.org/linkedin/asciietch.svg?branch=master)](https://travis-ci.org/linkedin/asciietch) [![Coverage Status](https://coveralls.io/repos/github/linkedin/asciietch/badge.svg)](https://coveralls.io/github/linkedin/asciietch)
A graphing library with the goal of making it simple to graph series of numbers using ascii characters.

## Quick Start
To start using Ascii Etch ensure Python 3.6 or higher is installed. Then install asciietch using pip3.6 or higher:
```
pip3 install asciietch
```
Then import asciietch and begin using it.
## Examples
### Graphing 0-4 values as a line graph
```python
>>> from asciietch.graph import Grapher
>>> g = Grapher()
>>> values = [0, 1, 2, 3, 4]
>>> print(g.asciigraph(values))
    -
   /
  /
 /
/
```
### Graphing 0-4 values as a histogram
```python
>>> from asciietch.graph import Grapher
>>> g = Grapher()
>>> values = [0, 1, 2, 3, 4]
>>> print(g.asciihist(values))
▁▃▅▆█
```
### Graphing more values
```python
>>> from asciietch.graph import Grapher
>>> g = Grapher()
>>> values = [0, 1, 2, 3, 4, 4, 3, 2, 1, 2, 2, 2]
>>> print(g.asciigraph(values))
    --
   /  \
  /    \ ---
 /      -
/
>>> print(g.asciihist(values))
▁▃▅▆██▆▅▃▅▅▅
```
### Graphing a large set of values and adding labels
```python
>>> import random
>>> from asciietch.graph import Grapher
>>> g = Grapher()
>>> values = []
>>> v = 0
>>> for i in range(1000):
...     v = v + random.randint(-1, 1)
...     values.append(v)
>>> print(g.asciigraph(values, max_height=10, max_width=100, label=True))
```
```
Upper value: 147.6 *********************************************************************************
                             -------- ---                                                           
                        ----/        -   \-      -                                                  
                   ----/                   \----/ \--                                               
                 -/                                  \                                              
----        ----/                                     \------      -  ----                          
    \------/                                                 \----/ \/    \-                        
                                                                            \--                     
                                                                               \-------             
                                                                                       \------      
                                                                                              \-   -
                                                                                                \-/ 
Lower value: 85.3 ********************************************* Mean: 122.196 *** Std Dev: 16.20 ***
```

## Developing

```sh
git clone git@github.com:linkedin/asciietch.git
cd asciietch
python3 setup.py venv
source activate
python3 setup.py develop
```

## Testing

```sh
pip3.6 install tox
tox
```

## Contributing Code
Contributions are welcome, see [Contribution guidelines for this project](CONTRIBUTING.md)
