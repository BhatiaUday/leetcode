class Solution:
    def poorPigs(self, buckets: int, minutesToDie: int, minutesToTest: int) -> int:
        b=minutesToTest//minutesToDie
        b=b+1
        i=0
        while True:
            p=b**i
            if p>=buckets:
                return i
            else:
                i+=1


