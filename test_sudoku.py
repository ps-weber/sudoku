from nose.tools import assert_equal
from nose.tools import raises
from sudoku import Sudoku, IncorrectSudokuException


def test_read_string():
    str1 = " , 9,  ,  ,  ,  , 2,  , 5;\n" + \
           "2,  ,  , 3,  ,  , 8, 9,  ;\n" + \
           " ,  ,  ,  , 2, 5,  , 7,  ;\n" + \
           " ,  , 1,  , 6,  ,  ,  , 2;\n" + \
           " , 3,  ,  , 9,  ,  , 5,  ;\n" + \
           "9,  ,  ,  , 1,  , 4,  ,  ;\n" + \
           " , 5,  , 7, 4,  ,  ,  ,  ;\n" + \
           " , 6, 3,  ,  , 8,  ,  , 9;\n" + \
           "7,  , 4,  ,  ,  ,  , 6,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(str1)
    assert_equal(str(sudoku), str1)


def test_only_choice():
    one_choice = " ,  ,  ,  , 3, 4,  ,  ,  ;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                 " ,  ,  ,  ,  ,  , 2,  , 5;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 6;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 7;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 8;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 9;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"

    solution =   " ,  ,  ,  , 3, 4,  ,  , 1;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                 " ,  ,  ,  ,  ,  , 2,  , 5;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 6;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 7;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 8;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  , 9;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                 " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(one_choice)
    sudoku.solve()
    assert_equal(str(sudoku), solution)


def test_single_possibility():
    one_poss = "1,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  , 1,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  , 1,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  , 1;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    solution = "1,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  , 1,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  , 1,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  , 1,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  , 1;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(one_poss)
    sudoku.solve()
    assert_equal(str(sudoku), solution)


def test_subgroup_exclusion():
    intBoxColumn = " ,  ,  ,  ,  ,  , 4, 5,  ;\n" + \
                   " ,  ,  ,  ,  ,  , 6, 7,  ;\n" + \
                   " ,  ,  ,  ,  , 1,  , 9, 8;\n" + \
                   " ,  ,  ,  ,  ,  ,  , 2, 9;\n" + \
                   " ,  ,  ,  ,  , 3,  ,  ,  ;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 4;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 5;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 6;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"

    solution =     " ,  ,  ,  ,  ,  , 4, 5,  ;\n" + \
                   " ,  ,  ,  ,  ,  , 6, 7,  ;\n" + \
                   " ,  ,  ,  ,  , 1,  , 9, 8;\n" + \
                   " ,  ,  ,  ,  ,  ,  , 2, 9;\n" + \
                   " ,  ,  ,  ,  , 3,  ,  , 7;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 4;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 5;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  , 6;\n" + \
                   " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(intBoxColumn)
    sudoku.solve()
    assert_equal(str(sudoku), solution)


def test_hidden_twins():
    boxPair =  " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  , 3,  , 5, 6,  ,  ,  ;\n" + \
               " ,  ,  ,  , 7, 8, 3,  ,  ;\n" + \
               " ,  ,  , 4,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  , 9,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"

    solution = " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  , 3,  ,  ,  ,  ,  ;\n" + \
               " ,  , 3,  , 5, 6,  ,  ,  ;\n" + \
               " ,  ,  ,  , 7, 8, 3,  ,  ;\n" + \
               " ,  ,  , 4,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  , 9,  ,  ,  ,  ,  ;\n" + \
               " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(boxPair)
    sudoku.solve()
    assert_equal(str(sudoku), solution)


def test_recursive_solve():
    rec_sudoku = " ,  ,  ,  , 5, 3,  ,  ,  ;\n" + \
                 "1,  ,  , 6,  ,  ,  ,  , 8;\n" + \
                 " , 5,  ,  ,  , 1,  , 4,  ;\n" + \
                 "4,  ,  ,  , 9,  , 5, 3,  ;\n" + \
                 " ,  , 9, 7,  , 6, 8,  ,  ;\n" + \
                 " , 2, 7,  , 3,  ,  ,  , 6;\n" + \
                 " , 4,  , 1,  ,  ,  , 8,  ;\n" + \
                 "2,  ,  ,  ,  , 7,  ,  , 1;\n" + \
                 " ,  ,  , 3, 2,  ,  ,  ,  ;\n"

    solution = "6, 8, 4, 2, 5, 3, 1, 7, 9;\n" + \
               "1, 9, 3, 6, 7, 4, 2, 5, 8;\n" + \
               "7, 5, 2, 9, 8, 1, 6, 4, 3;\n" + \
               "4, 1, 6, 8, 9, 2, 5, 3, 7;\n" + \
               "5, 3, 9, 7, 1, 6, 8, 2, 4;\n" + \
               "8, 2, 7, 4, 3, 5, 9, 1, 6;\n" + \
               "3, 4, 5, 1, 6, 9, 7, 8, 2;\n" + \
               "2, 6, 8, 5, 4, 7, 3, 9, 1;\n" + \
               "9, 7, 1, 3, 2, 8, 4, 6, 5;\n"

    sudoku = Sudoku()
    sudoku.read_string(rec_sudoku)
    sudoku.recursive_solve()
    assert_equal(str(sudoku), solution)


@raises(IncorrectSudokuException)
def test_incorrect_sudoku():
    incorrect = "1, 2, 3,  ,  ,  ,  ,  ,  ;\n" + \
                "4, 5, 6,  ,  ,  ,  ,  ,  ;\n" + \
                "7, 8,  , 9,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n" + \
                " ,  ,  ,  ,  ,  ,  ,  ,  ;\n"
    sudoku = Sudoku()
    sudoku.read_string(incorrect)
    sudoku.recursive_solve()
