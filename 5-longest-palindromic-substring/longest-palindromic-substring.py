class Solution:
    def longestPalindrome(self, s: str) -> str:
        if len(s)<=1:
            return s
        m=1
        ms=s[0]
        for i in range(len(s)-1):
            for j in range(i+1,len(s)):
                if j-i+1>m and s[i:j+1]==s[i:j+1][::-1]:
                    m=j-i+1
                    ms = s[i:j+1]
        return ms