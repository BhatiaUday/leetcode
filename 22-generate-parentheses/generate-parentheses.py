class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def a(l, r, s):
            if len(s)==n*2:
                res.append(s)
                return 

            if l < n:
                a(l + 1, r, s + '(')

            if r < l:
                a(l, r + 1, s + ')')
        res=[]
        a(0,0,"")
        return res