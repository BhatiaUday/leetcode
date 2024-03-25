class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        hashmap={}
        for i in nums:
            if hashmap.get(i) is not None:
                return True
            else:
                hashmap[i]=1
        