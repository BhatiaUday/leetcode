class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hashmap={}
        for i in nums:
            try:
                a= hashmap[i]
                return True
            except:
                hashmap[i]=1
        