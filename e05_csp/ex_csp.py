"""
The exercise is to create a (almost) general constraint satisfaction problem
solver. You will have to use the CSP data structure from csp.py. Read it for
reference!

"""
import numpy as np
import csp
from data import create_map_csp


def backtracking(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A csp.ConstrainedSatisfactionProblem, where all Variables
             are set and csp.complete() returns True. (I.e. the solved
             CSP)
    """
    assigned = []
    unassigned = csp.variables[:]
    for v in unassigned:
        if v.value is not None:
            unassigned.remove(v)
    
    result = recursive_backtracking(csp, assigned,unassigned)
    if result is False:
        print "fuck"
    return csp
    
def recursive_backtracking(csp, assigned,unassigned):
    if len(unassigned) == 0: # == len(csp.variables):
        return assigned

    var = unassigned[0]
    for v in csp.variables:
        if v not in assigned and v.value is None:
            var = v
            break
    valid_domain = get_valid_domain(var)
    for value in valid_domain:
        var.set_value(value)
        if csp.consistent():
            assigned.append(var)
            unassigned.remove(var)
            result = recursive_backtracking(csp, assigned,unassigned)
            if csp.complete():
                return result
            assigned.remove(var)
            unassigned.append(var)
        var.set_value(None)
    return False
    
  
def minimum_remaining_values(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP with
    minimum remaining values heuristic and no tie-breaker. Thus the
    first of all best solution is taken.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A tuple of 1) a csp.ConstrainedSatisfactionProblem, where
             all Variables are set and csp.complete() returns True. (I.e.
             the solved CSP) and 2) a list of all variables in the order
             they have been assigned.
    """
    assigned = list()
    result = mrv_rec_backtracking(csp, assigned, csp.variables[:]) 
    if result is False:
        print "fuck"
    return csp, assigned

def mrv_rec_backtracking(csp, assigned, unassigned,degree=False):
    if len(assigned) == len(csp.variables):
        return assigned
        
    var_list = min_remain_values(unassigned, len(csp.variables[0].domain))

    if degree:
        var = degree_heuristic(var_list,unassigned)
    else:
        var = var_list[0]
    valid_domain = get_valid_domain(var)
    for value in valid_domain:
        var.set_value(value)
        if csp.consistent():
            assigned.append(var)
            unassigned.remove(var)
            result = mrv_rec_backtracking(csp, assigned,unassigned,degree)
            if csp.complete():
                return result
            assigned.remove(var)
            unassigned.append(var)
        var.set_value(None)
    return False
    
def min_remain_values(unassigned,def_len):
    min_var = []
    min_len = def_len + 1
    for var in unassigned:
        valid_domain = get_valid_domain(var)
        if len(valid_domain) <= min_len:
            if len(valid_domain) < min_len:
                min_var = []
                min_len = len(valid_domain)
            min_var.append(var)
    return min_var
    
def get_valid_domain(var):
    valid_domain = var.domain[:]
    for p in var.peers:
        if p.value in valid_domain:
            valid_domain.remove(p.value)
    return valid_domain
    
def degree_heuristic(var_list,unassigned):
    max_c = -1
    result_var = None
    for var in var_list:
        counter = 0
        for peer in var.peers:
            if peer in unassigned:
                counter += 1
        if counter > max_c:
            result_var = var
            max_c = counter
    return result_var

def minimum_remaining_values_with_degree(csp, ac_3=False):
    """
    Implement the basic backtracking algorithm to solve a CSP with
    minimum remaining values heuristic and the degree heuristic as
    tie-breaker.

    Optional: if ac_3 == True use the AC-3 algorithm for constraint
              propagation. Important: if ac_3 == false don't use
              AC-3!
    :param csp: A csp.ConstrainedSatisfactionProblem object
                representing the CSP to solve
    :return: A tuple of 1) a csp.ConstrainedSatisfactionProblem, where
             all Variables are set and csp.complete() returns True. (I.e.
             the solved CSP) and 2) a list of all variables in the order
             they have been assigned.
    """
    assigned = list()
    result = mrv_rec_backtracking(csp, assigned, csp.variables[:],True) 
    if result is False:
        print "fuck"
    return csp, assigned


def create_sudoku_csp(sudoku):
    """
    Creates a csp.ConstrainedSatisfactionProblem from a np array
    `sudoku` which has shape (9, 9). Each entry of the sudoku is either
    0, which means it is not set yet or in [1, ..., 9], which means
    it is already assigned a number.

    The CSP should contain all constraints necessary to solve the sudoku.
    I.e. no two numbers in a row must be equal, no two numbers in a column
    must be equal and no two numbers in one of the 9 3x3 blocks must be
    equal. All numbers in the array must be already set.

    :param sudoku: A np array representing a unsolved sudoku
    :return: A csp.ConstrainedSatisfactionProblem which can be used
             to solve the sudoku
    """
    print sudoku
    constraints = []
    variables = []
    tupel_list = np.empty((9,9), dtype = csp.Variable)
    domain = range(1,10)#['1','2','3','4','5','6','7','8','9']
    for i,row in enumerate(sudoku):
        for j,field in enumerate(row):
            if field == 0:
                field = None
            """    do = domain
            else:
                do = [field]"""
            var = csp.Variable((i,j),domain)
            var.set_value(field)
            variables.append(var)
            tupel_list[i][j]=var            
    
    for i in range(0,9):
        for j in range(0,9):
            for r in range(i+1,9):
                constraints.append(csp.UnequalConstraint(tupel_list[i][j],tupel_list[r][j]))
            for l in range(j+1,9):
                constraints.append(csp.UnequalConstraint(tupel_list[i][j],tupel_list[i][l]))
            for outer in range(0,3):
                for inner in range(0,3):
                    if outer is not i % 3 and inner is not j % 3:
                        constraints.append(csp.UnequalConstraint(tupel_list[i][j],tupel_list[3*(i/3)+outer][3*(j/3)+inner]))
    return csp.ConstrainedSatisfactionProblem(variables,constraints)


def sudoku_csp_to_array(csp):
    """
    Takes a sudoku CSP from `create_sudoku_csp()` as you implemented
    it and returns a np array s with `s.shape == (9, 9)` (i.e. a
    9x9 matrix) representing the sudoku.

    :param csp: The CSP created with `create_sudoku_csp()`
    :return: A np array with shape (9, 9)
    """
    sudoku = np.zeros((9,9),np.int8)
    for var in csp.variables:
        i,j = var.name
        if var.value is None:
            sudoku[i][j]=0
        else:
            sudoku[i][j] = var.value
    return sudoku


def read_sudokus():
    """
    Reads the sudokus in the sudoku.txt and saves them as np arrays.
    :return: A list of np.arrays containing the sudokus
    """
    with open("sudoku.txt", "r") as f:
        lines = f.readlines()
    sudoku_strs = []
    for line in lines:
        if line[0] == 'G':
            sudoku_strs.append("")
        else:
            sudoku_strs[-1] += line.replace("", " ")[1:]
    sudokus = []
    for sudoku_str in sudoku_strs:
        sudokus.append(np.fromstring(sudoku_str, sep=' ',
                                     dtype=np.int).reshape((9, 9)))
    return sudokus


def main():
    """
    A main function. This might be useful for developing, if you don't
    want to run all tests all the time. Just write here what ever you
    want to develop your code. If you use pycharm you can run the unittests
    also by right-clicking them and then e.g. "Run 'Unittest test_sudoku_1'".
    """

    # first lets test with a already created csp:
    csp = create_map_csp()
    solution = backtracking(csp)
    #solution2,assigned = minimum_remaining_values(csp)
    print(solution)
    #print assigned

    # and now with our own generated sudoku CSP
    """sudokus = read_sudokus()
    csp = create_sudoku_csp(sudokus[1])
    solution = backtracking(csp)
    print sudoku_csp_to_array(solution)
"""

if __name__ == '__main__':
    main()
