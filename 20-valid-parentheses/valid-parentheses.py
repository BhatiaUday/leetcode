class Solution:
    def isValid(self, s: str) -> bool:
        l=[]
        for i in s:
            if i in "{[(":
                l.append(i)
            elif i ==")":
                if len(l)==0:
                    return False
                x=l.pop()
                if x!="(":
                    return False
            elif i =="]":
                if len(l)==0:
                    return False
                x=l.pop()
                if x!="[":
                    return False
            elif i =="}":
                if len(l)==0:
                    return False
                x=l.pop()
                if x!="{":
                    return False
        if len(l)==0:
            return True
        return False