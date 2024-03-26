class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        num=sorted(set(nums))
        x=1
        # if x>0 and x!=1:
        #     return 1
        # x=1
        for i in num:
            print(i,x)
            if i>0:
                if i!=x:
                    return x
                x+=1
        return x
        