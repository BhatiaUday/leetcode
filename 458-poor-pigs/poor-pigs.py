class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:
        b=minutesToTest//minutesToDie
        b=b+1
        i=0
        while (minutesToTest//minutesToDie +1)**i<buckets:
            i+=1
        return(i)

