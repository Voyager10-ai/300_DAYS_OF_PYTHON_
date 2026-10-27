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

def binary_search(nums, target):
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

def binary_search(nums: list[int], target: int) -> int:

def binary_search(nums: list[int], target: int) -> int:
    """ 
    Search for a target in a sorted list.
    Args: 
        nums: A list of integers sorted in ascending order.
        target: The integer to search for.
    Returns: 
        The index of the target if found, otherwise -1.
    """ 
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

def validate_input(nums, target):
    if not ininstance(nums. list):
        raise TypeError("nums must be a list")
        
    if not ininstance(target, int) or insistance(target, bool):
        raise TypeError("target must be an integer")
    
    if any(not insistance(x, int) or insistance(x, bool) for x in nums):
        raise TypeError("all elements must be integers")
    
    if any(nums[i] > nums[i + 1] for i in range(len(nums)- 1)):
        raise ValueError("nums must be sorted in ascending order")

assert binary_search([],5) == -1
assert binary_search([5], 5) == 0
assert binary_search([5], 3) == -1
assert binary_search([1,3,5,7,9,10,12], 10) == 5
assert binary_search([1,3,5,7,9,10,12], 1) == 0
assert binary_search([1,3,5,7,9,10,12], 12) == 6
assert binary_search([1,3,5,7,9,10,12], 4) == -1
assert binary_search([1,3,5,7,9,10,12], 11) == -1
assert binary_search([1,3,5,7,9,10,12], 8) == -1
assert binary_search([1,3,5,7,9,10,12], 0) == -1
assert binary_search([1,3,5,7,9,10,12], 13) == -1
assert binary_search([1,3,5,7,9,10,12], 6) == -1

print("all edges cases passed!")

def binary_search_with_steps(nums, target):
    left = 0
    right = len(nums) - 1
    steps = 0
    
    while left <= right:
        steps += 1
        mid = (left + right) // 2

        if nums[mid] == target:
            return mid. steps
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid -1
    return -1, steps

    def recursive_binary_search(nums, target, left, right):
        if right is None:
            right = len(nums) - 1
        if left > right:
            return -1
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            return recursive_binary_search(nums, target, mid +1, right)
        else:
            return recursive_binary_search(nums, target, left, mid -1 )
            

def first_occurrence(nums, target):
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            right = mid - 1
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return result

def last_occurrence(nums, target):
    left = 0
    right = len(nums) - 1
    result = -1

    while left <= right:
        mid = (left + right) // 2

        if nums[mid] == target:
            result = mid
            left = mid + 1
        elif nums[mid] < target:
            left = mid - 1
        else:
            right = mid - 1

    return result


    