def makeGrid(puzzle_string):
    if len(puzzle_string) != 81:
        print("invalid puzzle string")
        return
    grid = [[0]*9 for _ in range(9)]
    
    for i in range(9):
        for j in range(9):
            grid[i][j] = int(puzzle_string[i*9 + j])

    return grid

def makePuzzleString(grid):
    puzzle = ""
    for i in range(9):
        for j in range(9):
            puzzle += str(grid[i][j])
    return puzzle

def isOK(grid, r, c, n):
    # Check if number exists in row already
    if n in grid[r]:
        return False
    #check if number exists in col already
    if n in [grid[i][c] for i in range(9)]:
        return False
    #check if number exists in 3x3 box already
    startR, startC = r - r % 3, c - c % 3
    for i in range(3):
        for j in range(3):
            if grid[startR + i][startC + j] == n:
                return False
    return True

def solvePuzzle(grid, r=0, c=0): 
    if r == 9:
        return True

    if c == 9:
        return solvePuzzle(grid, r+1, 0)
    
    if grid[r][c] != 0:
        return solvePuzzle(grid,r,c+1)

    for k in range(1,10):
        if isOK(grid, r, c, k):
            grid[r][c] = k
            if solvePuzzle(grid, r, c+1):
                return True
            grid[r][c] = 0

    return False


