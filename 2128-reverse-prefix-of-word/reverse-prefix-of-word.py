class Solution:
    def reversePrefix(self, word: str, ch: str) -> str:
        f=0
        for i in range(len(word)):
            if f==0:
                if word[i]==ch:
                    f=i
                    break
        s=word[0:f+1][::-1]+word[f+1::]
        return(s)