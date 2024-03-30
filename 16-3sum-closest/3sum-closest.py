class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        s=set()
        o=nums[0]+nums[1]+nums[2]
        t=target
        def closest(a,b,t):
            if abs(a-t)<abs(b-t):
                return a
            else:
                return b
        for i in range(len(nums)):
            j=i+1
            k=len(nums)-1
            while j<k:
                su = nums[i] +nums[j] +nums[k]
                # print(o,su)
                o=closest(o,su,t)
                if su==t:
                    return target
                elif su<t:
                    j+=1
                else:
                    k-=1
        return o