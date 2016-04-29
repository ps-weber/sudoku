class IncorrectSudokuException(Exception):
    pass


class Sudoku:
    """
    Reads, stores and solves 9x9 sudoku puzzles.

    Attributes:
        grid            a 9x9 list of integer-lists for holding the the puzzle numbers,
                        zero symbolizes no value
        solved          true when sudoku has been successfully solved

        _boxes          3x3 list of lists of sets, containing each number contained
                        in a box (a box is a 3x3 segment of the puzzle)
        _rows           list of sets, containing each number in a row
        _columns        list of sets, containing each number in a column
        _poss           9x9 list of lists of sets, stores the possible numbers
                        for each cell
        _possCRows      list of lists that store the count of a possible number for each row
                        _possCRows[row][number-1]: count of possibilities for "number" in the row
        _possCColumns   same as _possCRows, but for columns
        _possCBoxes     same as _possCRows, but for boxes
    """
    def __init__(self, other=None):
        self.grid =         [[0]*9 for _ in range(9)]
        self._boxes =       [[set() for _ in range(3)] for _ in range(3)]
        self._rows =         [set() for _ in range(9)]
        self._columns =      [set() for _ in range(9)]
        self._poss =        [[set() for _ in range(9)] for _ in range(9)]
        self._possCRows =    [[0] * 9 for _ in range(9)]
        self._possCColumns = [[0] * 9 for _ in range(9)]
        self._possCBoxes =  [[[0] * 9 for _ in range(3)] for _ in range(3)]
        self.solved = False
        if other is not None:
            for x in range(9):
                for y in range(9):
                    self.grid[x][y] = other.grid[x][y]

    def _reset_poss_counts(self):
        """
        resets _possCColumns, _possCRows and _possCBoxes
        """
        for i in range(9):
            for n in range(9):
                self._possCColumns[i][n] = 0
                self._possCRows[i][n] = 0

        for i in range(3):
            for j in range(3):
                for n in range(9):
                    self._possCBoxes[i][j][n] = 0

    def read_string(self, in_string):
        """
        read in sudoku from string
        :param in_string:   string with numbers which are written row by row,
                            a ',' indicates the next number,
                            a ';' indicates a new row. zero symbolizes no value
        """
        x = 0
        y = 0
        for c in in_string:
            if c == " " or c == "\n":
                continue
            elif c == "," or c == "|":
                x += 1
            elif c == ";":
                x = 0
                y += 1
            else:
                self.grid[x][y] = int(c)
        self._update_units()

    def recursive_solve(self):
        """
        Solves the sudoku with regular strategies until it can not find any new numbers.
        Then it tries to find the solution by recursively "brute-forcing" the cells with
        the fewest possibilities. If the sudoku is ambiguous, it uses one possible solution.
        :raise IncorrectSudokuException: If the input sudoku has no solution.
        """
        self.solve()
        if not self.solved:
            x, y = self._find_min_poss()
            min_set = set(self._poss[x][y])
            for n in min_set:
                s = Sudoku(self)
                s.grid[x][y] = n
                try:
                    s.recursive_solve()
                except IncorrectSudokuException:
                    pass
                if s.solved:
                    print("'guessed' %i out of %i numbers in %i %i" % (n, len(min_set), x, y))
                    self.grid = s.grid
                    self.solved = True
                    break
        if not self.solved:
            raise IncorrectSudokuException()

    def solve(self):
        """
        tries to solve the sudoku repeatedly applying the strategies
        used in _solve_step()
        :return: whether the sudoku has been successfully solved
        """
        while self._solve_step():
            pass
        return self.solved

    def _find_min_poss(self):
        """
        find one of the cells with the fewest number of possibilities
        :return: tuple of indexes (x, y)
        """
        minx, miny = 0, 0
        minlen = 9
        for x in range(9):
            for y in range(9):
                if len(self._poss[x][y]) != 0 and len(self._poss[x][y]) < minlen:
                    minlen = len(self._poss[x][y])
                    minx, miny = x, y
        return minx, miny

    def __str__(self):
        """
        :return: the comma separated numbers row by row
        """
        out = ""
        for y in range(9):
            for x in range(9):
                out += str(self.grid[x][y])
                out += ", "
            out = out[:-2] + ";\n"
        return out

    def _solve_step(self):
        """
        fills all values which can be found in the current state of the sudoku
        the only choice rule, the single possibility rule,
        the Sub-Group exclusion rule and
        the Hidden Twin exclusion rule
        (see http://www.sudokudragon.com/sudokustrategy.htm)
        :return: true if a new number has been found
        """
        self._update_units()
        self._fill_poss()

        while True:
            change = False
            if self._hidden_twin():
                change = True

            self._update_poss_counts()
            if self._subgroup_exclusion():
                change = True

            if not change:
                break
        progressing = False
        solved = True
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    solved = False
                    if len(self._poss[x][y]) == 0:
                        raise IncorrectSudokuException()

                    # only choice rule
                    if len(self._poss[x][y]) == 1:
                        self.grid[x][y] = self._poss[x][y].pop()
                        # print("%i %i only poss in cell %i" % (x, y,  self.grid[x][y]))
                        progressing = True
                        continue

                    # single possibility rule
                    for n in self._poss[x][y]:
                        if self._possCRows[y][n - 1] == 1 or \
                           self._possCColumns[x][n - 1] == 1 or \
                           self._possCBoxes[x//3][y//3][n - 1] == 1:
                            self.grid[x][y] = n
                            # print("%i %i only poss in container %i" % (x, y,  self.grid[x][y]))
                            progressing = True
                            continue
        self.solved = solved
        return progressing

    def _update_units(self):
        """
        Update the values in _rows, _columns and _boxes
        """
        # update rows and columns and boxes
        for x in range(9):
            for y in range(9):
                n = self.grid[x][y]
                if n != 0:
                    self._rows[y].add(n)
                    self._columns[x].add(n)
                    self._boxes[x // 3][y // 3].add(n)

    def _fill_poss(self):
        """
        update the values in _poss
        :return:
        """
        alln = set([x for x in range(1, 10)])
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    self._poss[x][y] = alln - self._rows[y] - self._columns[x] \
                                       - self._boxes[x // 3][y // 3]
                else:
                    self._poss[x][y].clear()

    def _hidden_twin(self):
        """
        try apply the hidden twin rule once to either a row, column or a box
        the rule itself if implemented in _hidden_twin_step
        :return: true if the rule was applied
        """
        # what follows are the functions used on the offsets
        # to iterate on columns, rows and boxes
        def box_x(i, j): return (i // 3) * 3 + j // 3

        def box_y(i, j): return (i % 3) * 3 + j % 3

        def col_x(i, j): return i

        def col_y(i, j): return j

        def row_x(i, j): return j

        def row_y(i, j): return i

        for i in range(9):
            for j in range(9):
                if self._hidden_twin_step(col_x(i, j), col_y(i, j)):
                    return True
                elif self._hidden_twin_step(row_x(i, j), row_y(i, j)):
                    return True
                elif self._hidden_twin_step(box_x(i, j), box_y(i, j)):
                    return True
        return False

    def _hidden_twin_step(self, xfunc, yfunc, i, j):
        """
        apply the Hidden twin rule described at www.sudokudragon.com/sudokustrategy.htm
        :param xfunc: function that defines how the i and j parameters should be
                      transformed to get the x coordinate. This parameter makes it
                      possible to apply this function to rows, columns and boxes
        :param yfunc: same as xfunc for the y coordinate
        :param i: first offset of the cell
        :param j: second offset of the cell
        :return: true if the rule was successfully applied
        """
        changed = False
        x, y = xfunc(i, j), yfunc(i, j)
        # check if there is a pair at the given offset
        if len(self._poss[x][y]) == 2:
            # search for cell with the same pair
            for j2 in range(j + 1, 9):
                if self._poss[x][y] == self._poss[xfunc(i, j2)][yfunc(i, j2)]:
                    # cell with same pair is cell (i, j2)
                    pair = self._poss[x][y]
                    # remove all occurrences of the paired numbers in the sequence
                    # which are not the pairs themselves
                    for j3 in range(9):
                        if j3 != j and j3 != j2:
                            if not self._poss[xfunc(i, j3)][yfunc(i, j3)].isdisjoint(pair):
                                self._poss[xfunc(i, j3)][yfunc(i, j3)] -= pair
                                changed = True
                    break
        return changed

    def _subgroup_exclusion(self):
        """
        apply the Subgroup exclusion rule(see www.sudokudragon.com/sudokustrategy.htm)
        :return: whether the rule was successfully applied
        """
        for i in range(9):
            for boxIndex in range(3):
                # check columns intersecting with boxes
                poss_c = [0]*9
                for k in range(3):
                    for n in self._poss[i][3*boxIndex+k]:
                        poss_c[n-1] += 1
                    for index, count in enumerate(poss_c):
                        if count != 0 and count == self._possCBoxes[i//3][boxIndex][index]:
                            n = index + 1
                            changed = False
                            for y in range(9):
                                if y//3 != boxIndex and n in self._poss[i][y]:
                                    changed = True
                                    self._poss[i][y].remove(n)
                            if changed:
                                # print("reduced %i in intersecting column %i box %i %i" % (n, i, i//3, boxIndex))
                                return True

                # check for rows intersecting with boxes
                poss_c = [0]*9
                for k in range(3):
                    for n in self._poss[3*boxIndex+k][i]:
                        poss_c[n-1] += 1
                    for index, count in enumerate(poss_c):
                        if count != 0 and count == self._possCBoxes[boxIndex][i//3][index]:
                            n = index + 1
                            changed = False
                            for x in range(9):
                                if x//3 != boxIndex and n in self._poss[x][i]:
                                    changed = True
                                    self._poss[x][i].remove(n)
                            if changed:
                                # print("reduced %i in intersecting row %i box %i %i" % (n, i, boxIndex, i//3))
                                return True
        return False

    def _update_poss_counts(self):
        self._reset_poss_counts()
        for x in range(9):
            for y in range(9):
                if self.grid[x][y] == 0:
                    for n in self._poss[x][y]:
                        self._possCRows[y][n - 1] += 1
                        self._possCColumns[x][n - 1] += 1
                        self._possCBoxes[x // 3][y // 3][n - 1] += 1

if __name__ == "__main__":
    sudoku = Sudoku()

    instr = " ,  ,  ,  ,  , 1,  , 3, 4;" + \
            " ,  ,8 , 5, 3,  ,  ,6 ,  ;" + \
            " ,  ,  , 8,  ,  , 5,  , 2;" + \
            "7,  ,  ,  ,  ,  , 2,  ,  ;" + \
            "2, 8,  , 9,  , 3,  , 5, 6;" + \
            " ,  , 6,  ,  ,  ,  ,  , 9;" + \
            "8,  , 5,  ,  , 6,  ,  ,  ;" + \
            " , 9,  ,  , 1, 5, 3,  ,  ;" + \
            "3, 2,  , 4,  ,  ,  ,  ,  ;"

    sudoku.read_string(instr)
    sudoku.recursive_solve()
    print(sudoku)
