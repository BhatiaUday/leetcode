class Solution:
    def myPow(self, x: float, n: int) -> float:
        def dfs(x, n):
            if n == 0:
                return 1
            if n == 1:
                return x
    
            if n%2 == 1:
                return x* dfs(x*x, n//2)
            else:
                return dfs(x*x, n//2)
        if n > 0:
            return dfs(x,n)
        else:
            return 1/dfs(x,-n)