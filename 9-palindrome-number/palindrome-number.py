class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x<0:
            return False
        
        r=0
        t=x
        while t!=0:
            d=t%10
            r=r*10+d
            t=t//10
        return r==x