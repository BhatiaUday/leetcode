class Solution:
    def reverse(self, x: int) -> int:
        out=""
        x=(list(str(x)))
        if x[0]=='-':
            out+="-"
            x.pop(0)
        for i in x[::-1]:
            out+=i
        out=int(out)
        if out in range(-2**31,2**31):
            return out
        else:
            return 0
