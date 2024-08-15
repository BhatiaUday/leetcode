class Solution(object):
    def lemonadeChange(self, bills):
        a={}
        for i in bills:
            if i in a.keys():
                a[i]+=1
            else:
                a[i]=1
            if i!=5:
                ret=i-5
                bill=a.keys()
                bill.sort(reverse=True)
                for j in bill:
                    while j<=ret and a[j]!=0:        
                        ret-=j
                        a[j]-=1
                if ret!=0:
                    return False
        return True
                    
                
        