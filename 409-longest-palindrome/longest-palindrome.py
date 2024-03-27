class Solution:
    def longestPalindrome(self, s: str) -> int:
        odd=0
        d={}
        for i in s:
            if i in d:
                d[i]+=1
            else:
                d[i]=1
            if d[i]%2==1:
                odd+=1
            else:
                odd-=1
        if odd >1:
            return len(s)-odd+1
        return len(s)