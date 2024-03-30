class Solution:
    def grayCode(self, n: int) -> List[int]:
        l=[0]
        for i in range(n):
            n=[]
            for x in l:
                n.append(x+(1<<i))
                print(bin(x+(1<<i)))
            l=l+n[::-1]
        return l