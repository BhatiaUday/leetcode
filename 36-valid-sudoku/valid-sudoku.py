class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        def isValid(row, col, ch):
            row, col = int(row), int(col)
            board[row][col]='.'
            
            for i in range(9):
                
                if board[i][col] == ch:
                    return False
                if board[row][i] == ch:
                    return False
                
                if board[3*(row//3) + i//3][3*(col//3) + i%3] == ch:
                    return False
            board[row][col]=ch
            return True
        for i in range(9):
            print(board[i])
            for j in range(9):
                if board[i][j]!='.':
                    print(board[i][j])
                    x=isValid(i,j,board[i][j])
                    if x==False:
                        return False
        return True