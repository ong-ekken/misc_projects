#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""SudokuBoardGen.py
   Defined a Sudoku_Board Class, allowing generation of a 9x9 Sudoku board,
   saving it into sudokuboards.csv in the same folder
"""

from random import sample
from copy import deepcopy
import csv
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

print("This program will generate sodukko-boards and save them in a separate file.\n")

class Sudoku_Board:

    def __init__(self):
        self.blank = True                
        self.fill = None

    def __repr__(self) -> str:
        return "\n".join([" ".join([str(num) for num in line]) for line in self.fill])

    def __iter__(self):
        return iter(self.fill)

    # retrieves cell values
    def get(self):
        return self.fill

    def generate(self):
        # Helper function to check square allocation
        def sq(num):
            if num in (0,1,2):
                return 0
            if num in (3,4,5):
                return 1
            if num in (6,7,8):
                return 2

        # Loop while cells not correctly filled
        # while self.blank:
        while True:

            # preliminarily fill cells with zeros
            zeros = [ 0 for _ in range(9) ]
            self.fill = [ zeros[:] for _ in range(9) ]
            
            # setup quota trackers for each row, col, square
            numbers = set(range(1, 10))
            rows_quota = [deepcopy(numbers) for row in range(9)]
            cols_quota = [deepcopy(numbers) for col in range(9)]
            squares = [ [deepcopy(numbers) for sq_y in range(3)] for sq_x in range(3) ]

            # iterate through each row and col
            for row in range(9):
                for col in range(9):

                    # Continue if cell is filled
                    if self.fill[row][col]:
                        continue
                    
                    # Continue if no options left
                    pool_avail = rows_quota[row] \
                                & cols_quota[col] \
                                & squares[sq(row)][sq(col)]             
                    if not len(pool_avail):
                        continue
                    
                    # Fill in number
                    new_num = sample(list(pool_avail), 1)[0]
                    self.fill[row][col] = new_num
                    
                    # Update quotas
                    rows_quota[row].remove(new_num)
                    cols_quota[col].remove(new_num)
                    squares[sq(row)][sq(col)].remove(new_num)
        
            # If all cells are filled, allow while loop to terminate
            # self.blank = False
            # for row in self.fill:
            #     if 0 in row:
            #         logging.debug(row)
            #         self.blank = True

            if "0" not in str(new_board):
                break

            
            
if __name__=="__main__":
    
    # Create board object
    new_board = Sudoku_Board()

    # Generate board
    new_board.generate()
    print(new_board)
    
    # save generated board 
    with open('sudokuboards.csv', 'a+') as csvfile:
        filewriter = csv.writer(csvfile)
        filewriter.writerow(new_board.get())
