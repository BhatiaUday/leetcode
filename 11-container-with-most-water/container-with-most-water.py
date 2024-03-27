class Solution:
    def maxArea(self, height: List[int]) -> int:
        p1=0
        p2=len(height)-1
        largest=0
        def volume():
            d=p2-p1
            if height[p1]>height[p2]:
                v=height[p2]*d
            elif height[p1]<=height[p2]:
                v=height[p1]*d
            return v
        while p1<p2:
            volu=volume()
            if largest<volu:
                largest=volu
            if height[p1]>height[p2]:
                p2-=1
            elif height[p1]<=height[p2]:
                p1+=1
        return largest
        
