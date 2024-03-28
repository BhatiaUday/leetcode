class Solution:
    def romanToInt(self, s: str) -> int:
        t = {"I": 1,"V": 5,"X": 10,"L": 50,"C": 100,"D": 500,"M": 1000}
        n=0
        p=0
        for c in s[::-1]:
            if t[c]>=p:
                n+=t[c]
            else:
                n-=t[c]
            p=t[c]
        return n