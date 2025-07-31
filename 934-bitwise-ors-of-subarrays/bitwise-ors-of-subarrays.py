class Solution:
    def subarrayBitwiseORs(self, arr: List[int]) -> int:
        result = set()
        current = set()

        for i in arr:
            next = {i | j for j in current}
            next.add(i)
            result.update(next)
            current = next
        return len(result)
        