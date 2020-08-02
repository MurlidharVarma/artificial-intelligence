import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if count equals to number of cells, then all are mines
        if len(self.cells) > 0 and len(self.cells) == self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # if count is zero, and there exists some cells then those are safe
        if self.count == 0 and len(self.cells) > 0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) mark the cell as safe
        self.mark_safe(cell)

        # 3) add a new sentence to the AI's knowledge base
        #    based on the value of `cell` and `count`

        # get neighbouring cells
        neighbours = self.get_nearby_cells(cell)
        new_sentence = Sentence(neighbours, count)

        # if the neighbouring cells are already part of mines and safes then 
        # discard them from sentence cell
        for neighbour_cell in neighbours:

            if neighbour_cell in self.mines:
                new_sentence.mark_mine(neighbour_cell)

            if neighbour_cell in self.safes:
                new_sentence.mark_safe(neighbour_cell)

        if len(new_sentence.cells) > 0:
            self.knowledge.append(new_sentence)

        # 4) mark any additional cells as safe or as mines
        # if it can be concluded based on the AI's knowledge base
        for sentence in self.knowledge:

            # if there exists sentences with no cells then remove them
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)
                pass

            known_mines = sentence.known_mines()
            # if there are any known mines
            if known_mines != None:
                # see if there exists any mines that are not already available in self.mines
                known_mines.difference_update(self.mines)
                #if yes, then mark them as mines
                for mine in known_mines.copy():
                    self.mark_mine(mine)
            
            known_safes = sentence.known_safes()
            # if there are known mines
            if known_safes != None:
                # see if there exists any mines that are not already available in self.mines
                known_safes.difference_update(self.safes)
                #if yes, then mark them as mines
                for safe in known_safes.copy():
                    self.mark_safe(safe)

        # 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge
        queue = self.knowledge.copy()
        while len(queue) > 0:

            # pop the first sentence from queue
            curr_sentence = queue.pop(0)

            # if there exists sentences with no cells then remove them from knowledge
            if len(curr_sentence.cells) == 0:
                self.knowledge.remove(curr_sentence)
            else:
                # iterate through all sentences in knowledge base
                for sentence in self.knowledge:
                    # if the sentence is current sentence from queue then pass
                    if(sentence == curr_sentence):
                        pass
                    else:
                        # draw inferences
                        new_sentence = self.infer(curr_sentence, sentence)

                        # if there is a new infered sentence that is not already available in knowledge
                        if len(new_sentence.cells) > 0 and new_sentence not in self.knowledge:
                            # add to knowledge
                            self.knowledge.append(new_sentence)
                            # add to queue to determine any futher new inferences 
                            queue.append(new_sentence)




    def infer(self, sentence1, sentence2):
        """
            Returns new sentence that could be derived 
            based on two sentences passed as argument
        """
        inference = Sentence([],0)

        parent = sentence1
        child = sentence2

        len_1 = len(parent.cells)
        len_2 = len(child.cells)

        # both sentence has non zero number of cells
        if len_1 >0 and len_2 >0:

            # if the parent has less cells than child, then switch parent-child designation
            # this it to determine which sentence could be super set of other
            if len_2 > len_1:
                parent = sentence2
                child = sentence1
            
            if parent.cells.issuperset(child.cells):
                clone_superset = parent.cells.copy()
                inference = Sentence(clone_superset.difference(child.cells),parent.count-child.count)

        return inference



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves_available = self.safes.copy().difference(self.moves_made)

        if len(safe_moves_available) > 0:
            retVal = safe_moves_available.pop()
            return retVal
        else: 
            return None



    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # when moves made + known mines = number of cells in grid,
        # then no more cell available for assignment
        total = len(self.moves_made) + len(self.mines)
        if total == (self.height * self.width):
            return None
        else:
            cell = self.get_random_cell()

            while cell in self.moves_made or cell in self.mines:
                cell = self.get_random_cell()

            return cell




    def get_random_cell(self):
        """
            Returns a random cell position based on width and height of board
        """
        return (random.randint(0, self.height-1), random.randint(0, self.width-1))




    def get_nearby_cells(self, cell):
        """
        Returns cells that are nearby given cells.
        """
        # to collect nearby cells
        nearby_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # add to nearby cells
                if 0 <= i < self.height and 0 <= j < self.width:
                    nearby_cells.add((i,j))

        return nearby_cells
