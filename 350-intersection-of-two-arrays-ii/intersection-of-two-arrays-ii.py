class Solution(object):
    def intersect(self, nums1, nums2):
        nums1.sort()
        nums2.sort()
        ans=[]
        a=0
        b=0
        while a<len(nums1) and b<len(nums2):
            if nums1[a]==nums2[b]:
                ans.append(nums2[b])
                a+=1
                b+=1
            elif nums1[a]>nums2[b]:
                b+=1
            else:
                a+=1
        return ans
        