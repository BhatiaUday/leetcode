class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:
        i=0
        while buckets> (minutesToTest//minutesToDie +1)**i:
            i+=1
        return(i)


