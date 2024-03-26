class Solution:
    def minCost(self, colors: str, neededTime: List[int]) -> int:
        n = len(neededTime)
        time = 0
        i = 0

        while i < n:
            j = i + 1
            count, max_time, total_time = 1, neededTime[i], neededTime[i]

            while j < n and colors[i] == colors[j]:
                max_time = max(max_time, neededTime[j])
                total_time += neededTime[j]
                count += 1
                j += 1
            if count > 1:
                time += total_time - max_time
            i = j

        return time