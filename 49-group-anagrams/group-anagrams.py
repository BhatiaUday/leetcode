class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ret=[]
        m={}
        for i in strs:
            ss=''.join(sorted(i))
            if ss in m:
                ret[m[ss]].append(i)
            else:
                m[ss]=len(ret)
                ret.append([i])
        return ret