class Solution:
    def findDuplicates(self, nums: List[int]) -> List[int]:
        hashmap=set()
        dup=[]
        for i in nums:
            if i in hashmap:
                dup.append(i)
            else:
                hashmap.add(i)
        return dup