class Solution(object):
    def removeElement(self, nums, val):
        l = 0
        for i in range(len(nums)):
            if (nums[i] != val):        
                    nums[l] = nums[i]
                    l+=1
        return l