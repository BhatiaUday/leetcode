class Solution:
    def minimumOperations(self, nums: List[int]) -> int:
        if not nums:
            return None
        x = set(nums)
        if 0 in x:
            return len(x)-1
        else:
            return len(x)
        