class Solution:
    def isHappy(self, n: int) -> bool:
        repeat=0
        seen=[]
        seen.append(n)
        while n!=1 and repeat==0:
            n=list(str(n))
            n=self.sqlist(n)
            if n in seen:
                repeat=1
            seen.append(n)
        return repeat==0

    def sqlist(self, l:list):
        s=0
        for i in l:
            s+=int(i)**2
        return s
