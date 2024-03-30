class Solution:
    def restoreIpAddresses(self, s: str) -> List[str]:
        r=[]
        c=[]
        def b(g):
            if g==len(s) and len(c)==4:
                r.append(".".join(c))
                return 
            if len(c)>4 or g>=len(s):
                return
            if s[g]=="0":
                c.append(s[g])
                b(g+1)
                c.pop()
                return
            j=0
            while j<4 and g+j<len(s):
                if int(s[g:g+j+1])<256:
                    c.append(s[g:g+j+1])
                    b(g+j+1)
                    c.pop()
                j+=1
        b(0)
        return r