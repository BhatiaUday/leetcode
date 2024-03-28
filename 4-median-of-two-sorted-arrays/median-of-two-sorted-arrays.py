class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        nums1+=nums2
        nums1.sort()
        print(nums1)
        x=len(nums1)
        print(x)
        if x%2==0:
            return (nums1[int((x/2)-1)]+nums1[int(x/2)])/2
        else:
            return nums1[int((x-1)/2)]