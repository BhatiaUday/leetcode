class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        s=set()
        o=[]
        t=0
        for i in range(len(nums)):
            j=i+1
            k=len(nums)-1
            while j<k:
                su = nums[i] +nums[j] +nums[k]
                if su==t:
                    s.add((nums[i],nums[j],nums[k]))
                    j+=1
                    k-=1
                elif su<t:
                    j+=1
                else:
                    k-=1
        output=list(s)
        return output