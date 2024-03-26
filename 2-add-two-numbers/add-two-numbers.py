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

            # Find the sum of two nodes and carray
            val=0
            if l1:
                val+=l1.val
            if l2:
                val+=l2.val
            val+=carry

            # if sum is greater than 9 that means next nodes
            # will have carry
            if val>9:
                carry=1 
            else:
                carry=0

            # Create a new node and add it to the result 
            newNode=ListNode(val%10)
            c.next=newNode
            c=c.next

            if l1 :
                l1=l1.next
            if l2 :
                l2=l2.next

        # if there is an carry creae a new node
        if carry:
            newNode= ListNode(carry)
            c.next=newNode
        return result.next