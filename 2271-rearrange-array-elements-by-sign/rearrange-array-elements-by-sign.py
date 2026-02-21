class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        pos=[]
        neg=[]
        out=[]
        for i in nums:
            if i<0:
                neg.append(i)
            else:
                pos.append(i)
        pos=pos[::-1]
        neg=neg[::-1]
        while neg:
            out.append(pos.pop())
            out.append(neg.pop())
        return out
