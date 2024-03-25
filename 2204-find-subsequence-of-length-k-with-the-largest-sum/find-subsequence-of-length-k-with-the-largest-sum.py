class Solution:
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        max_k = [nums[0]]
        for i in range(1, len(nums)):
            if len(max_k) < k: max_k.append(nums[i])  # put first k elements 
            elif len(max_k) == k:  # whenever we have k elements
                if nums[i] > min(max_k):  # if the i th element is bigger than the minimum of seen so far
                    max_k.remove(min(max_k))  # remove minimum
                    max_k.append(nums[i])  # append the current element at the end
        return max_k