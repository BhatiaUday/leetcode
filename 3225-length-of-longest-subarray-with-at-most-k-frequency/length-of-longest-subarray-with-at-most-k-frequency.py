class Solution:
    def maxSubarrayLength(self, nums: List[int], k: int) -> int:
        seen={}
        a=0
        l=0
        n=len(nums)
        for i in range(n):
            seen[nums[i]]= seen.get(nums[i],0)+1
            if seen[nums[i]]>k:
                while nums[l]!=nums[i]:
                    seen[nums[l]]-=1
                    l+=1
                seen[nums[l]]-=1
                l+=1
            a=max(a,i-l+1)
        return a
