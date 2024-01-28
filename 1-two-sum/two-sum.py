class Solution:
    def twoSum(self, nums: List[int], target: int):
        checked={}
        x=0
        while x <len(nums):
            n=nums[x]
            f=target-n
            if f in checked:
                return(x,checked[f])
            checked[n]=x
            x+=1