class Solution:
    def simplifyPath(self, path: str) -> str:
        stack=path.split("/")
        # print(stack)
        out=[]
        for i in stack:
            if i==".." and out:
                out.pop()
            elif i not in [".","",".."]:
                out.append(i)
        
        return "/"+ "/".join(out)
        