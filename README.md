# function-magnitude

A tool for identifying the (big-O) run time of a Python function. This is found by measuring the execution time of a given function for various input sizes, then using least-squares error to fit a selection of common run time functions to the results. The fitted function with the smallest error is found and returned.

## Getting Started

This project consists of two modules.
* `arrays.py` - A class to represent matrices/vectors and perform typical operations including solving systems of linear equations.
* `magnitude.py` - The collection of functions to measure function run time and write data to csv.

### Prerequisites

To run function-magnitude, the host machine must have the following installed:
* `Python3` - The programming language in which function-magnitude was written. Available [here](https://www.python.org/).

### Use

The module `magnitude.py` offers four methods that work together to characterise a given function. These should be imported by a script which has access to the measured function (e.g. "testFunction"), as follows.  
`from magnitude import getData, getFittedFuncs, getMagnitude, resultToCsv`

Typical use of these methods is present as the contents of the `main` function of `magnitude.py`, namely:
```data = getData('testFunction', testTaskGen, 1, 100, 10001, 100)
fittedFuncs = getFittedFuncs(data)
magnitudeLabel = getMagnitude(data, fittedFuncs)
csvData = resultToCsv(data, fittedFuncs)

print("Function magnitude:", magnitudeLabel)

with open('Graph Data.csv', "w") as outfile:
    outfile.write(csvData)
```

In order, this snippet times the execution of the function named "testFunction", identifies the times which would be taken by the fitted version of each available comparison function\* (for each task size\*\*), then retrieves two characterisation strings: the best-suited comparison function's name, and the csv-formatted time data for each comparison function. 

To observe the output of the above snippet, run the `magnitude.py` module as follows:
`python3 magnitude.py`

This will create a file `Graph Data.csv` in the working directory, which may be used to plot the execution time for varying task sizes, and the fitted comparison functions.

\* The tested big-O run times are from the list `magnitudeForms` in the `magnitude.py` module.  
\** The `getData` method must be supplied with the handle to a function which generates input for `testFunction`. This function must, in turn, take a single input number - the task size. Task sizes to test are defined by a start value, step value and stop value (all given to `getData`.)

## Authors

* **Marc Katzef** - [mkatzef](https://github.com/mkatzef)
