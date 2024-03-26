class Solution:
    def totalMoney(self, n: int) -> int:
        x=0
        bal=0
        for i in range(n):
            if i%7==0:
                x+=1
                y=x
                bal+=y
                y+=1
            else:
                bal+=y
                y+=1
        return bal