class Solution:
    def pivotArray(self, nums: List[int], pivot: int) -> List[int]:
        left=[]
        right=[]
        pc=0
        for i in nums:
            if i<pivot:
                left.append(i)
            elif i>pivot:
                right.append(i)
            else:
                pc+=1
        for i in range(pc):
            left.append(pivot)
        left.extend(right)
        return left
        