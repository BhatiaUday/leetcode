class Solution:
    def sortByBits(self, arr: List[int]) -> List[int]:
        dic={}
        out=[]
        for i in arr:
            b=bin(i).count('1')
            if b in dic.keys():
                c=dic[b]
                c.append(i)
                c.sort()
                
            else:
                dic[b]=[i]
        print(dic)
        x=sorted(dic.keys())
        for i in x:
            out.extend(dic[i])
        return out