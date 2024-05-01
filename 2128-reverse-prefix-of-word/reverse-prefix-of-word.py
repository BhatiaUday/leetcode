class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        l=[]
        f=0
        for i in word:
            # print(i)
            if f==0:
                l.append(i)
                print(l)
                if i==ch:
                    f=1
                    l=l[::-1]
            else:
                l.append(i)
        print(l)
        s=""
        for i in l:
            s+=i
        return(s)
