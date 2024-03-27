class Solution:
    def isPalindrome(self, s: str) -> bool:
        st=""
        st1=""
        for i in s:
            if i in "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890":
                st1+=i
                st=i+st
        return st.lower()==st1.lower()
        