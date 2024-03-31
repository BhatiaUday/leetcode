class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res=[]
        line=[]
        c=0
        for w in words:
            if c+len(w)+len(line)>maxWidth:
                for i in range(maxWidth-c):
                    line[i%(len(line)-1 or 1)]+=" "
                res.append("".join(line))
                line=[]
                c=0
            line+=[w]
            c+=len(w)
        return res+ [' '.join(line).ljust(maxWidth)]
             