class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        while True:
            if n<=0:
                return False
            elif n%2==0:
                n=n/2
            elif n==1:
                break
            else:
                return False
        return True