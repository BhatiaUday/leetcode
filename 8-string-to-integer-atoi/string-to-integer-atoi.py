class Solution:
    def myAtoi(self, s: str) -> int:
        s = s.strip()
        if not s:
            return 0
        i=0
        num=0
        sign=1
        if s[0] == '+' or s[0] == '-':
            sign = -1 if s[0] == '-' else 1
            i += 1
        while i<len(s) and s[i].isdigit():
            digit=int(s[i])
            num = num * 10 + digit
            i+=1
        if num>(2**31-1):
            if sign==1:
                return 2**31-1
            else:
                return -1*(2**31)
        return sign*num