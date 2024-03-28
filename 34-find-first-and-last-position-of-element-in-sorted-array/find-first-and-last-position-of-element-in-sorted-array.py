class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        out=[-1,-1]
        for i in range(len(nums)):
            if nums[i]==target and out[0]==-1:
                out[0]=i
            if nums[i]==target:
                out[1]=i
        return out
            