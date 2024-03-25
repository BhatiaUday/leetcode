class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        if n<=0:
            return False
        c=bin(n).count('1')
        if c==1:
            return True