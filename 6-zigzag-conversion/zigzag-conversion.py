class Solution:
    def convert(self, s: str, numRows: int) -> str:
        e=[]
        for i in range(numRows):
            e.append("")
        print(e)
        index=0
        direction=-1
        if numRows==1:
            return s
        for i in s:
            e[index]+=i
            if index==0:
                direction=1
            elif index==numRows-1:
                direction=-1
            index+=direction
        print(e)
        out=""
        for i in e:
            out+=i
        return out
            