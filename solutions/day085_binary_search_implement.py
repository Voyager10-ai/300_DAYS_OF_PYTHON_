# LeetCode: Binary Search Implementation

# Problem: 704. Binary Search
# Difficulty: Easy
# Language: Python
# Platform: LeetCode

# Problem link:  ⁠LeetCode 704: Binary Search

# Problem Statement

# Given an array of integers nums, which is sorted in ascending order, and an integer target, write a function to search for target in nums.

class Solution:
    def search(self, nums: list[int], target: int) ->int:
        left = 0
        right = len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1
