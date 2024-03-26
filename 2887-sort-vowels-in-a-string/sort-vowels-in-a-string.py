class Solution:
    def sortVowels(self, s: str) -> str:
        x=list(s)
        vov="aeiouAEIOU"
        con=[]
        v=[]
        out=""
        vind=0
        for i in x:
            if i in vov:
                v.append(i)
                con.append(1)
            else:
                con.append(i)
        v.sort()
        for i in con:
            if i==1:
                out=out+v[vind]
                vind+=1
            else:
                out=out+i
        return out