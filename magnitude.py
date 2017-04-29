""" A module designed to measure the performance of a given function in terms of
    its growth rate upper-bound. This is achieved through finding the
    appropriate coefficient for each of the functions in 'magnitudeForms' using
    least-squares error, then calculating and comparing the errors each of these
    best-cases give.
    Important: this module depends on the module 'Arrays'
    Author: Marc Katzef
    Date: 27/3/2016
"""

from arrays import *
import timeit
import math
import os


#The list of function tuples to consider, each entry must be of the form (title,
#variable label, function) all of type str, where the function may be formatted
#with the 'n' value and evaluate to a float.
magnitudeForms = [('Constant', 'cons', '1'), ('Linear', 'lin', '{}'), 
                  ('Quadratic', 'quad', '{} ** 2'), ('Cubic', 'cube', '{} ** 3'),
                  ('Logarithmic', 'log', 'math.log({})'),
                  ('Log-Linear', 'logl', '{0} * math.log({0})')]


def getData(function_str, iterable, runsPerTrial=1):
    """Takes the name of a local function (type str), an iterable which generates
    test input, and the number of times each test input value should be tested
    (type int). Returns the collected time data as a list of tuples of the form
    (iterable index, time taken)"""
    trials = len(iterable)
        
    data = []
    for n in iterable:
        t1 = timeit.Timer('{}({})'.format(function_str, n), 'from __main__ import {}'.format(function_str))
        value = t1.timeit(number=runsPerTrial)
        data.append((n, value))
    
    return data
    
    
def getFittedFuncs(data):
    """Finds the multiple of each of the possible function forms which
    minimises error. Returns a dictionary with function labels as the
    keys, and lists of the fitted function values as values."""
    trials = len(data)
    b = Array(trials, 1)
    
    A_dict = {}
    for title, label, function in magnitudeForms:
        A_dict[label] = b.deepCopy()
        
    for index in range(trials):
        b.changeEntry(index, 0, data[index][1])
        for title, label, function in magnitudeForms:
            expected_value = eval(function.format(data[index][0]))
            A_dict[label].changeEntry(index, 0, expected_value)
    
    fitted_functions_dict = {}
    for title, label, function in magnitudeForms:
        x = lsSolve(A_dict[label], b)
        fitted_functions_dict[label] = A_dict[label] * x
    
    return fitted_functions_dict


def getMagnitude(data, fittedFuncs):
    """Compares the shape of the given data with that of the possible functions
    (in magnitudeForms). Returns the label of the function that can be scaled
    to provide the smallest error."""
    trials = len(data)
    b = Array(trials, 1)
        
    for index in range(trials):
        b.changeEntry(index, 0, data[index][1])
        
    errors = []
    for title, label, function in magnitudeForms:
        error = (b - fittedFuncs[label]).ONEnorm()
        errors.append(error)

    return magnitudeForms[errors.index(min(errors))][0]

    
def resultToCsv(data, fittedFuncs):
    trials = len(data)
    
    output = ''
    output += 'Job Size, Time,'
    for title, label, function in magnitudeForms:
        output += title + ','
    output += '\n'
    
    for index in range(trials):
        line = str(data[index][0]) + ','
        line += str(data[index][1]) + ','
        
        for title, label, function in magnitudeForms:
            value = fittedFuncs[label].getEntry(index, 0)
            line += "{}, ".format(value)
            
        output += line + '\n'
    
    return output
    
        
def testfunction1(n):
    for i in range(n):
        assignment = 1


def main():
    data = getData('testfunction1', range(1, 10001, 100), 100)
    fittedFuncs = getFittedFuncs(data)
    magnitudeLabel = getMagnitude(data, fittedFuncs)
    csvData = resultToCsv(data, fittedFuncs)
    
    print("Function magnitude:", magnitudeLabel)
    
    with open('Graph Data.csv', "w") as outfile:
        outfile.write(csvData)
    

if __name__ == '__main__':
    main()
    