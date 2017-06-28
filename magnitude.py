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
magnitudeForms = [('Constant', '1'), ('Linear', '{}'), 
                  ('Quadratic', '{} ** 2'), ('Cubic', '{} ** 3'),
                  ('Logarithmic', 'math.log({})'),
                  ('Log-Linear', '{0} * math.log({0})')]


def getData(function_str, task_gen_func, task_size_start, task_size_step, task_size_stop, runsPerTrial=1):
    """Takes the name of a function to test (type str), the handle
    to a function which generates input for the first function, and
    the range of task sizes to test (as start,step and stop values).
    Returns the collected time data as a list of tuples of the form
    (task size, time taken)."""
    task_size = task_size_start
        
    data = []
    while task_size <= task_size_stop:
        arguments = task_gen_func(task_size)
        t1 = timeit.Timer('{}({})'.format(function_str, arguments), 'from __main__ import {}'.format(function_str))
        value = t1.timeit(number=runsPerTrial)
        data.append((task_size, value))
        
        task_size += task_size_step
    
    return data
    
    
def getFittedFuncs(data):
    """Finds the multiple of each of the possible function forms which
    minimises error. Returns a dictionary with function labels as the
    keys, and lists of the fitted function values as values."""
    trials = len(data)
    b = Array(trials, 1)
    
    A_dict = {}
    for title, function in magnitudeForms:
        A_dict[title] = b.deepCopy()
        
    for index in range(trials):
        b.changeEntry(index, 0, data[index][1])
        for title, function in magnitudeForms:
            expected_value = eval(function.format(data[index][0]))
            A_dict[title].changeEntry(index, 0, expected_value)
    
    fitted_functions_dict = {}
    for title, function in magnitudeForms:
        x = lsSolve(A_dict[title], b)
        fitted_functions_dict[title] = A_dict[title] * x
    
    return fitted_functions_dict


def getMagnitude(data, fittedFuncs):
    """Compares the shape of the given data with that of the possible functions
    (in magnitudeForms). Returns the title of the function that can be scaled
    to provide the smallest error."""
    trials = len(data)
    b = Array(trials, 1)
        
    for index in range(trials):
        b.changeEntry(index, 0, data[index][1])
        
    errors = []
    for title, function in magnitudeForms:
        error = (b - fittedFuncs[title]).ONEnorm()
        errors.append(error)

    return magnitudeForms[errors.index(min(errors))][0]

    
def resultToCsv(data, fittedFuncs):
    trials = len(data)
    
    output = ''
    output += 'Job Size, Time,'
    for title, function in magnitudeForms:
        output += title + ','
    output += '\n'
    
    for index in range(trials):
        line = str(data[index][0]) + ','
        line += str(data[index][1]) + ','
        
        for title, function in magnitudeForms:
            value = fittedFuncs[title].getEntry(index, 0)
            line += "{}, ".format(value)
            
        output += line + '\n'
    
    return output
    
        
def testFunction(inputList):
    """A sample function to measure. Returns the length of a given list."""
    return len(inputList)


def testTaskGen(task_size):
    """A sample task generator function. Returns a list with task_size
    entries, formatted as a string. Note: eval(return value) must be
    suitable as input for measured function."""
    task = [0] * task_size
    formatted_task = str(task)
    return formatted_task


def main():
    data = getData('testFunction', testTaskGen, 1, 100, 1001, 100)
    fittedFuncs = getFittedFuncs(data)
    magnitudeLabel = getMagnitude(data, fittedFuncs)
    csvData = resultToCsv(data, fittedFuncs)
    
    print("Function magnitude:", magnitudeLabel)
    
    with open('Graph Data.csv', "w") as outfile:
        outfile.write(csvData)
    

if __name__ == '__main__':
    main()
   