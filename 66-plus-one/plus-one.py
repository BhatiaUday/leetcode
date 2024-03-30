class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        carry=1
        digits=digits[::-1]
        out=[]
        for i in digits:
            i+=carry
            if i>9:
                i-=10
                carry=1
            else:
                carry=0
            out.append(i)
        if carry==1:
            out.append(carry)
        return out[::-1]

