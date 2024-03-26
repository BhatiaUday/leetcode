class Solution:
    def addBinary(self, a: str, b: str) -> str:
        c=0
        r=""
        a=list(a)
        b=list(b)
        while a or b:
            v=0
            if a:
                v+=int(a[-1])
            if b:
                v+=int(b[-1])
            v+=c
            if v==0:
                r=str(0)+r
                c=0
            if v==1:
                r=str(1)+r
                c=0
            if v==2:
                r=str(0)+r
                c=1
            if v==3:
                r=str(1)+r
                c=1
            if a:
                a.pop()
            if b:
                b.pop()
        if c:
            r=str(1)+r
        return r