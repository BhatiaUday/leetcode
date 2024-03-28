class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen={}
        l=0
        a=0
        n=len(s)
        for i in range(n):
            seen[s[i]] = seen.get(s[i],0)+1
            if seen[s[i]]>1:
                while s[l]!=s[i]:
                    seen[s[l]]-=1
                    l+=1
                seen[s[l]]-=1
                l+=1
            a=max(a,i-l+1)
        return a