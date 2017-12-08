# Ascii Etch
A graphing library with the goal of making it simple to graphs using ascii characters.

## Quick Start
To start using Ascii Etch ensure Python 3.6+ is installed. Then install asciietch using pip3:
```
pip3 install asciietch
```
Then import asciietch and begin using it.
## Examples
### Graphing 0-4 values
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
### Graphing ups and downs
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
```
### Graphing a large set of values and add labels
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
Lower value: 85.3 ***************************** Mean: 122.196 *** Std Dev: 16.204881430673357 ******
```

## Contributing Code
Contributions are welcome, see [Contribution guidelines for this project](CONTRIBUTING.md)

## More information
Feel free to reach out if you have any questions [scallister@linkedin.com](mailto:scallister@linkedin.com)
