class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        mappings={'2':'abc','3':'def','4':'ghi','5':'jkl','6':'mno','7':'pqrs','8':'tuv','9':'wxyz'}
        if not digits:
            return []
        def backtrack(index, path):
            if index == len(digits):
                combinations.append("".join(path))
                return

            for char in mappings[digits[index]]:
                path.append(char)
                backtrack(index + 1, path)
                path.pop()

        combinations = []
        backtrack(0, [])
        return combinations