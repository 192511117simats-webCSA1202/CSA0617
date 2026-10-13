"""Search algorithms for DAA Assignment 1."""
import math

def linear_search(arr, target):
    comparisons = 0
    for i, value in enumerate(arr):
        comparisons += 1
        if value == target:
            return i, comparisons
    return -1, comparisons

def binary_search(arr, target):
    """Requires ascending sorted arr."""
    lo, hi = 0, len(arr) - 1
    comparisons = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        if target < arr[mid]:
            hi = mid - 1
        else:
            lo = mid + 1
    return -1, comparisons

def hash_lookup(table, target):
    # One dictionary membership/key lookup is counted as one logical key check.
    checks = 1
    return (target in table), checks

def interpolation_search(arr, target):
    """Requires sorted numeric arr. Returns index and comparison/probe count."""
    lo, hi = 0, len(arr) - 1
    checks = 0
    while lo <= hi and arr[lo] <= target <= arr[hi]:
        if arr[lo] == arr[hi]:
            checks += 1
            return (lo if arr[lo] == target else -1), checks
        pos = lo + int((target - arr[lo]) * (hi - lo) / (arr[hi] - arr[lo]))
        pos = max(lo, min(pos, hi))
        checks += 1
        if arr[pos] == target:
            return pos, checks
        if arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1
    return -1, checks

def jump_search(arr, target):
    """Requires sorted arr."""
    n = len(arr)
    step = max(1, int(math.sqrt(n)))
    prev = 0
    checks = 0
    while prev < n and arr[min(step, n)-1] < target:
        checks += 1
        prev = step
        step += max(1, int(math.sqrt(n)))
        if prev >= n:
            return -1, checks
    for i in range(prev, min(step, n)):
        checks += 1
        if arr[i] == target:
            return i, checks
        if arr[i] > target:
            return -1, checks
    return -1, checks

class BSTNode:
    __slots__ = ("key", "left", "right")
    def __init__(self, key):
        self.key, self.left, self.right = key, None, None

def bst_build(values):
    root = None
    for key in values:
        node = BSTNode(key)
        if root is None:
            root = node
            continue
        cur = root
        while True:
            if key < cur.key:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            elif key > cur.key:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right
                # Duplicate keys are ignored.
            else:
                break
    return root

def bst_lookup(root, target):
    checks = 0
    cur = root
    while cur is not None:
        checks += 1
        if cur.key == target:
            return True, checks
        cur = cur.left if target < cur.key else cur.right
    return False, checks
