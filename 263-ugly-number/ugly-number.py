class Solution:
    def isUgly(self, n: int) -> bool:
        for i in 2,3,5:
            while n%i == 0 and n%i<n:
                n=n/i
        return n==1

        