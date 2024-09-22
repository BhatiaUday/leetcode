class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        c={}
        for i in range(len(nums)):
            n=nums[i]
            q=target-n
            if q in c:
                return[i,c[q]]
            c[n]=i
        