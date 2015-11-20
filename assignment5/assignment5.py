#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import itertools

backtrack_calls = 0
backtrack_failures = 0



class CSP:
    def __init__(self):
        # self.variables is a list of the variable names in the CSP
        self.variables = []

        # self.domains[i] is a list of legal values for variable i
        self.domains = {}

        # self.constraints[i][j] is a list of legal value pairs for
        # the variable pair (i, j)
        self.constraints = {}

    def add_variable(self, name, domain):
        """Add a new variable to the CSP. 'name' is the variable name
        and 'domain' is a list of the legal values for the variable.
        """
        self.variables.append(name)
        self.domains[name] = list(domain)
        self.constraints[name] = {}

    def get_all_possible_pairs(self, a, b):
        """Get a list of all possible pairs (as tuples) of the values in
        the lists 'a' and 'b', where the first component comes from list
        'a' and the second component comes from list 'b'.
        """
        return itertools.product(a, b)

    def get_all_arcs(self):
        """Get a list of all arcs/constraints that have been defined in
        the CSP. The arcs/constraints are represented as tuples (i, j),
        indicating a constraint between variable 'i' and 'j'.
        """
        return [ (i, j) for i in self.constraints for j in self.constraints[i] ]

    def get_all_neighboring_arcs(self, var):
        """Get a list of all arcs/constraints going to/from variable
        'var'. The arcs/constraints are represented as in get_all_arcs().
        """
        return [ (i, var) for i in self.constraints[var] ]

    def add_constraint_one_way(self, i, j, filter_function):
        """Add a new constraint between variables 'i' and 'j'. The legal
        values are specified by supplying a function 'filter_function',
        that returns True for legal value pairs and False for illegal
        value pairs. This function only adds the constraint one way,
        from i -> j. You must ensure that the function also gets called
        to add the constraint the other way, j -> i, as all constraints
        are supposed to be two-way connections!
        """
        if not j in self.constraints[i]:
            # First, get a list of all possible pairs of values between variables i and j
            self.constraints[i][j] = self.get_all_possible_pairs(self.domains[i], self.domains[j])

        # Next, filter this list of value pairs through the function
        # 'filter_function', so that only the legal value pairs remain
        self.constraints[i][j] = filter(lambda value_pair: filter_function(*value_pair), self.constraints[i][j])

    def add_all_different_constraint(self, variables):
        """Add an Alldiff constraint between all of the variables in the
        list 'variables'.
        """
        for (i, j) in self.get_all_possible_pairs(variables, variables):
            if i != j:
                self.add_constraint_one_way(i, j, lambda x, y: x != y)

    def backtracking_search(self):
        """This functions starts the CSP solver and returns the found
        solution.
        """
        # Make a so-called "deep copy" of the dictionary containing the
        # domains of the CSP variables. The deep copy is required to
        # ensure that any changes made to 'assignment' does not have any
        # side effects elsewhere.
        assignment = copy.deepcopy(self.domains)

        # Run AC-3 on all constraints in the CSP, to weed out all of the
        # values that are not arc-consistent to begin with
        self.inference(assignment, self.get_all_arcs())

        # Call backtrack with the partial assignment 'assignment'
        return self.backtrack(assignment)

    def backtrack(self, assignment):
        """The function 'Backtrack' from the pseudocode in the
        textbook.

        The function is called recursively, with a partial assignment of
        values 'assignment'. 'assignment' is a dictionary that contains
        a list of all legal values for the variables that have *not* yet
        been decided, and a list of only a single value for the
        variables that *have* been decided.

        When all of the variables in 'assignment' have lists of length
        one, i.e. when all variables have been assigned a value, the
        function should return 'assignment'. Otherwise, the search
        should continue. When the function 'inference' is called to run
        the AC-3 algorithm, the lists of legal values in 'assignment'
        should get reduced as AC-3 discovers illegal values.

        IMPORTANT: For every iteration of the for-loop in the
        pseudocode, you need to make a deep copy of 'assignment' into a
        new variable before changing it. Every iteration of the for-loop
        should have a clean slate and not see any traces of the old
        assignments and inferences that took place in previous
        iterations of the loop.
        """
 

        # TODO: IMPLEMENT THIS

        #Prøver å se om en løsning kan sees direkte
        complete = True
        global backtrack_calls
        backtrack_calls += 1

        for value in assignment.values():
            if len(value) != 1:
                complete = False
                break

        if complete:
            return assignment

        #Dersom en løsning ikke er funnet, forstett å prøve veridere på brette
        else:
            var = self.select_unassigned_variable(assignment)
            for value in assignment[var]:
                new_assignment_table = copy.deepcopy(assignment)

                #Sletter alle mulige løsninger og legger til den oppslåtte verdien
                new_assignment_table.pop(var, None)
                new_assignment_table[var] = [value]

                inferences = self.inference(new_assignment_table, self.get_all_neighboring_arcs(var))
                if inferences is not False:
                    result = self.backtrack(new_assignment_table)
                    if result is not False:
                        return result
            global backtrack_failures
            backtrack_failures += 1
            return False

    def select_unassigned_variable(self, assignment):
        """The function 'Select-Unassigned-Variable' from the pseudocode
        in the textbook. Should return the name of one of the variables
        in 'assignment' that have not yet been decided, i.e. whose list
        of legal values has a length greater than one.
        """
        # TODO: IMPLEMENT THIS

        #Finner og returnerer den verdien som har færrest valg i forhold til sine naboer
        min_value = 10
        for key in assignment.keys():
            domain = assignment[key]
            domain_size = len(domain)

            #Her finnes og settes den minste verien lik den akutelle verdien(keyen)
            if (domain_size > 1) and (domain_size < min_value):
                lowest_value = key
        
        return lowest_value

    def inference(self, assignment, queue):
        """The function 'AC-3' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'queue'
        is the initial queue of arcs that should be visited.
        """
        # TODO: IMPLEMENT THIS

        #Mens det ekisterer nye plasser å besøke
        while queue:
            (i, j) = queue.pop()
            #Prøver å sette variablen som fast variabel
            if self.revise(assignment, i, j):
                # Sjekker om løsningen fortsatt er tilgjengelig
                if not assignment[i]:
                    return False

                # Hvis ikke, legg til i løen og fortsett gjennom den.
                else:
                    for (k, _) in self.get_all_neighboring_arcs(i):
                        queue.append((k, i))
        return True

    def revise(self, assignment, i, j):
        """The function 'Revise' from the pseudocode in the textbook.
        'assignment' is the current partial assignment, that contains
        the lists of legal values for each undecided variable. 'i' and
        'j' specifies the arc that should be visited. If a value is
        found in variable i's domain that doesn't satisfy the constraint
        between i and j, the value should be deleted from i's list of
        legal values in 'assignment'.
        """
        # TODO: IMPLEMENT THIS

        revised = False
        index = 0

        #Sjekker domenet for en mulig verdi i i
        for x in assignment[i]:
            satisfied = False
            #Dobbeltsjekker at ikke verdien x og y er den samme,
            for y in assignment[j]:
                if x != y:
                    satisfied = True

            #Dersom ingen verdi y for j fjernes det i'te elementet fra domenet
            if not satisfied:
                assignment[i].pop(index)
                index -= 1
                revised = True
            index += 1
        return revised

def create_map_coloring_csp():
    """Instantiate a CSP representing the map coloring problem from the
    textbook. This can be useful for testing your CSP solver as you
    develop your code.
    """
    csp = CSP()
    states = [ 'WA', 'NT', 'Q', 'NSW', 'V', 'SA', 'T' ]
    edges = { 'SA': [ 'WA', 'NT', 'Q', 'NSW', 'V' ], 'NT': [ 'WA', 'Q' ], 'NSW': [ 'Q', 'V' ] }
    colors = [ 'red', 'green', 'blue' ]
    for state in states:
        csp.add_variable(state, colors)
    for state, other_states in edges.items():
        for other_state in other_states:
            csp.add_constraint_one_way(state, other_state, lambda i, j: i != j)
            csp.add_constraint_one_way(other_state, state, lambda i, j: i != j)
    return csp

def create_sudoku_csp(filename):
    """Instantiate a CSP representing the Sudoku board found in the text
    file named 'filename' in the current directory.
    """
    #Lagt til for å nullstille hvor mange ganger backtrack kalles og failer
    global backtrack_calls
    global backtrack_failures
    backtrack_calls = 0
    backtrack_failures = 0
    

    csp = CSP()
    board = map(lambda x: x.strip(), open(filename, 'r'))

    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                csp.add_variable('%d-%d' % (row, col), map(str, range(1, 10)))
            else:
                csp.add_variable('%d-%d' % (row, col), [ board[row][col] ])

    for row in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for col in range(9) ])
    for col in range(9):
        csp.add_all_different_constraint([ '%d-%d' % (row, col) for row in range(9) ])
    for box_row in range(3):
        for box_col in range(3):
            cells = []
            for row in range(box_row * 3, (box_row + 1) * 3):
                for col in range(box_col * 3, (box_col + 1) * 3):
                    cells.append('%d-%d' % (row, col))
            csp.add_all_different_constraint(cells)

    return csp

def print_sudoku_solution(solution):
    """Convert the representation of a Sudoku solution as returned from
    the method CSP.backtracking_search(), into a human readable
    representation.
    """
    for row in range(9):
        for col in range(9):
            print solution['%d-%d' % (row, col)][0],
            if col == 2 or col == 5:
                print '|',
        print
        if row == 2 or row == 5:
            print '------+-------+------'

    #Lagt til for printing av statistikken
    print "Antall ganger backtrack kalles: " + str(backtrack_calls)
    print "Antall ganger backtrack failer: " + str(backtrack_failures)
    print ""
    print ""



#Printing av resultater
def csp1():
    csp = create_sudoku_csp("sudokus/easy.txt")
    print "Easy board:"
    print_sudoku_solution(csp.backtracking_search())

def csp2():
    csp = create_sudoku_csp("sudokus/medium.txt")
    print "Medium board:"
    print_sudoku_solution(csp.backtracking_search())

def csp3():
    csp = create_sudoku_csp("sudokus/hard.txt")
    print "Hard board:"
    print_sudoku_solution(csp.backtracking_search())

def csp4():
    csp = create_sudoku_csp("sudokus/veryhard.txt")
    print "Veryhard board:"
    print_sudoku_solution(csp.backtracking_search())




csp1()
csp2()
csp3()
csp4()
