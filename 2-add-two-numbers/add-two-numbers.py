# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        
        
        carry=0 
        result=ListNode(0)
        c=result
        while l1 or l2:
            val=0
            if l1:
                val+=l1.val
            if l2:
                val+=l2.val
            val+=carry
            if val>9:
                carry=1 
            else:
                carry=0
            newNode=ListNode(val%10)
            c.next=newNode
            c=c.next
            if l1 :
                l1=l1.next
            if l2 :
                l2=l2.next
        if carry:
            newNode= ListNode(carry)
            c.next=newNode
        return result.next