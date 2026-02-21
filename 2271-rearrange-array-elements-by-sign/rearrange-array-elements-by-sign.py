class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        i, j = 0, 1
        res = [0]*n
        pos = 0
        neg = 1
        while i<n:
            if nums[i]>0:
                res[pos] = nums[i]
                pos += 2
            else:
                res[neg] = nums[i]
                neg += 2
            i += 1
               
        return res
