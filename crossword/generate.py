import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # iterate over each variables in self.domains
        for variable, domain in self.domains.items():
            for x in domain.copy():
                # remove items whose length does not match with variable length
                if variable.length != len(x):
                    self.domains[variable].remove(x)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        is_revised = False
        overlaps = self.crossword.overlaps[(x,y)]

        if overlaps != None:
            for x_domain_val in self.domains[x].copy():

                has_possible_val_in_y = False
                
                # check if x domain value satisfies any value in y domain
                for y_domain_val in self.domains[y]:
                    if self.is_overlap_satisfied(x_domain_val,y_domain_val,overlaps):
                        has_possible_val_in_y = True
                        break
                
                # if no value in domain in y has been satisfied,
                # then remove that x value from x domain
                if not has_possible_val_in_y:
                    self.domains[x].remove(x_domain_val)
                    is_revised = True

        return is_revised

    def is_overlap_satisfied (self, str1, str2, overlap):
        """
            if the character at index as mentioned in overlap 
            matches for both str1 and str2 the returns True else False
        """
        if str1[overlap[0]] == str2[overlap[1]]:
            return True
        else:
            return False


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        queue = arcs
        if arcs == None:
            queue = list(self.crossword.overlaps.keys())
        
        while len(queue) > 0:
            x, y = queue.pop(0)

            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                else:
                    for dependent in self.crossword.neighbors(x):
                        queue.append((dependent,x))
        
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        is_complete = True

        for variable in self.crossword.variables:
            if assignment.get(variable) == None or len(assignment.get(variable)) == 0:
                is_complete = False
                break
        
        return is_complete

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        value_used = set()

        for variable, value in assignment.items():
            # check if values are distinct
            if value in value_used:
                return False
            else:
                value_used.add(value)

            # check if the node consistent
            if len(value) != variable.length:
                return False

            # check if arc consistent
            for neighbour in self.crossword.neighbors(variable):
                overlaps = self.crossword.overlaps[variable, neighbour]
                if assignment.get(neighbour) != None and self.is_overlap_satisfied(value, assignment[neighbour], overlaps) == False:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # a dict to store domain value and its occurrance in neighbour's domain
        domain_counts = dict()

        # iterate through each domain of var passed
        for value in self.domains[var]:
            counter = 0

            # count the number of neighbours that has this domain value
            for neighbour in self.crossword.neighbors(var):
                # if the neighbour is already in assignment, then discard such neighbour from counting
                if assignment.get(neighbour) != None or len(assignment.get(neighbour)) == 0:
                    pass
                elif value in self.domains[neighbour]:
                    counter += 1
            
            domain_counts[value] = counter

        # sort the dict based on count
        sorted_by_count = sorted(domain_counts.items(), key=lambda item: item[1])

        # extract the domain to a list based on count with least first
        ordered_domain = []
        for domain, count in sorted_by_count.items():
            ordered_domain.append(domain)

        return ordered_domain

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        if self.assignment_complete(assignment):
            return None
        
        # get all the unassigned variables
        unassigned_variables = dict()
        for variable in self.crossword.variables:
            if assignment.get(variable) == None or len(assignment.get(variable)) == 0:
                unassigned_variables[variable] = len(self.domains[variable])
        
        # out of all unassigned variables, get the one with least number of domain values.
        sorted_by_count = sorted(unassigned_variables.items(), key=lambda item: item[1])
        min_remaining_domain = dict()
        min_count=0
        # check if there exists more than one unassigned variables competing with same number of least number of domain values
        for variable, count in sorted_by_count:
            if min_count == 0:
                min_count = count

            if count == min_count:
                degree = len(self.crossword.neighbors(variable))
                min_remaining_domain[variable] = degree
            else:
                break
        
        # check which one of those unassigned variable has highest degrees
        # return the one with highest degress or else return any one of them
        sorted_by_degree = sorted(unassigned_variables.items(), key=lambda item: item[1], reverse=True)
        
        return sorted_by_degree[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)

        for value in self.domains[var]:
            assignment[var] = value

            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                    
            assignment.pop(var)

        return None
            

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
