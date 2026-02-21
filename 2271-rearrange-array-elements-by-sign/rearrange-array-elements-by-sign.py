class Solution:
    def rearrangeArray(self, nums: List[int]) -> List[int]:
        n = len(nums)
        result = [0] * n
        
        pos_index = 0   # even index
        neg_index = 1   # odd index
        
        for num in nums:
            if num > 0:
                result[pos_index] = num
                pos_index = pos_index + 2
            else:
                result[neg_index] = num
                neg_index = neg_index + 2
                
        return result