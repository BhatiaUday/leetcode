class Solution:
    def climbStairs(self, n: int) -> int:
        save={}
        return self.climb(n,save)
    def climb(self,n,save):
        if n==0 or n==1:
            return 1
        if n not in save:
            save[n]=self.climb(n-1,save)+self.climb(n-2,save)
        return save[n]