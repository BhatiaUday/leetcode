class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        x=set(nums)
        return len(x)!=len(nums)