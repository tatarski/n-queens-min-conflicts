from random import randint
import time

# Count conflicts for queen on given column
# Count conflict from each direction only once
def count_conflicts(queen_rows:list[int], cur_col:int) -> int:
    n = len(queen_rows)
    attacked_from_dir = [
        [False, False, False],
        [False, False, False], 
        [False, False, False]
    ]
    cur_row = queen_rows[cur_col]
    for col in range(n):
        if col == cur_col: continue
        row = queen_rows[col]
        d_col = cur_col - col
        d_row = cur_row - row

        if d_col != 0 and d_row != 0 and abs(d_row) != abs(d_col): continue
        if d_col != 0:
            d_col = -1 if d_col < 0 else 1
        if d_row != 0:
            d_row = -1 if d_row < 0 else 1
        attacked_from_dir[d_row + 1][d_col + 1] = True

    return sum([int(attacked_from_dir[i][j]) for i in range(3) for j in range(3)])

def count_all_conflicts(queen_rows: list[int]) -> list[int]:
    return [count_conflicts(queen_rows, col) for col in range(len(queen_rows))]

def print_board(queen_rows: list[int]):
    for i in range(len(queen_rows)):
        for j in range(len(queen_rows)):
            if(queen_rows[j] == i):
                print("* ", end="")
            else:
                print("- ", end="")

        print()

def min_conflicts(queen_rows: list[int]):
    n = len(queen_rows)
    col_conflicts = count_all_conflicts(queen_rows)
    if sum(col_conflicts) == 0: return queen_rows

    iterC = 0
    for i in range(256):
        iterC+=1
        # Find all columns with conflicts
        conflicted = [col for col in range(n) if 0 < col_conflicts[col]]
        # Select random column
        col = conflicted[randint(0, len(conflicted) - 1)]

        # Find row that minimizes conflicts
        row_conflicts = [0 for j in range(n)]
        for row in range(n):
            queen_rows[col] = row
            row_conflicts[row] = count_conflicts(queen_rows, col)

        # If more than one row minimize conflicts - select one at random
        min_conflict_c = min(row_conflicts)
        min_rows = [row for row in range(n) if row_conflicts[row] == min_conflict_c]
        new_row = min_rows[randint(0, len(min_rows)-1)]
        queen_rows[col] = new_row
        
        # Recalculate conflicts and check if board is solved
        col_conflicts = count_all_conflicts(queen_rows)
        all_conflicts = sum(col_conflicts)
        if all_conflicts == 0:
            print("ITERATION NUMBER:", iterC)
            return queen_rows

    return -1


# Generate board, depending on N
def gen_board(n) -> list[int]:
    queen_rows = [(2*i)%n + -int(i/(n/2))*(n%2 - 1) for i in range(0, n)]
    if n% 6 == 4:
        queen_rows = [(2*i + 1)%n - int(i/(n/2)) for i in range(0, n)]
    elif n%6 == 3:
        queen_rows = [(2*i + 1)%n if i <= int(n/2) else (2*(i-int(n/2) - 1))%n for i in range(0, n)]
        queen_rows[int(n/2)] = n-1    
    return queen_rows

def main():
    N = int(input())
    queen_rows = gen_board(N)
    t1 = time.time()
    result = min_conflicts(queen_rows)
    t2 = time.time()
    if result == -1:
        print("FAIL")
        print_board(queen_rows)
    else:
        print_board(result)
        print("TIME", t2-t1)

if __name__ == "__main__":
    main()