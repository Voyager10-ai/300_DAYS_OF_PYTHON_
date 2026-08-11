# Day 36: Check Key Exist
#
# Problem:
#   Write a Python program to check whether a given key exists in a dictionary using multiple approaches.
#   - Direct Membership Check: Fast O(1) membership test using `in` operator.
#   - Safe Value Retrieval: Using `.get()` with a unique sentinel object.
#   - View-Based Check: Using `.keys()` dictionary view object.

import sys
import re
import unittest
from typing import List, Set, Dict, Tuple, Optional, Iterable, Any, Union


_SENTINEL = object()


def check_key_in(d: dict, key: Any) -> bool:
    """
    Checks if a key exists in a dictionary using the `in` operator.

    Args:
        d: Input dictionary.
        key: Key to check for existence.

    Returns:
        True if key exists in d, False otherwise.

    Time Complexity: O(1) on average.
    Space Complexity: O(1).

    Example:
        check_key_in({"a": 1, "b": 2}, "a") -> True
        check_key_in({"a": 1, "b": 2}, "c") -> False
    """
    if not isinstance(d, dict):
        return False
    return key in d


def check_key_get(d: dict, key: Any) -> Tuple[bool, Any]:
    """
    Checks key existence and retrieves value safely using dict.get() with a sentinel object.

    Args:
        d: Input dictionary.
        key: Key to check.

    Returns:
        Tuple (exists: bool, value: Any). If key does not exist, value is None.

    Example:
        check_key_get({"a": None}, "a") -> (True, None)
        check_key_get({"a": None}, "b") -> (False, None)
    """
    if not isinstance(d, dict):
        return False, None
    val = d.get(key, _SENTINEL)
    if val is _SENTINEL:
        return False, None
    return True, val


def check_key_has_keys(d: dict, key: Any) -> bool:
    """
    Checks if key exists by inspecting the dict.keys() view.

    Args:
        d: Input dictionary.
        key: Key to look for.

    Returns:
        True if key is present in d.keys(), False otherwise.
    """
    if not isinstance(d, dict):
        return False
    return key in d.keys()


def check_nested_key(d: dict, key_path: List[Any]) -> Tuple[bool, Any]:
    """
    Traverses a sequence of keys through nested dictionaries to check for path existence.

    Args:
        d: Input dictionary.
        key_path: List of keys representing path (e.g., ['user', 'profile', 'id']).

    Returns:
        Tuple (exists: bool, value: Any).

    Example:
        check_nested_key({"a": {"b": {"c": 42}}}, ["a", "b", "c"]) -> (True, 42)
        check_nested_key({"a": {"b": 10}}, ["a", "b", "c"]) -> (False, None)
    """
    if not isinstance(d, dict) or not key_path:
        return False, None

    current = d
    for key in key_path:
        if not isinstance(current, dict) or key not in current:
            return False, None
        current = current[key]

    return True, current


def check_key_recursive(d: Any, target_key: Any) -> List[Any]:
    """
    Recursively searches for all occurrences of a target key in nested dicts/lists.

    Args:
        d: Input data structure (dict, list, or primitive).
        target_key: Key to find.

    Returns:
        List of values associated with target_key at any depth.

    Example:
        check_key_recursive({"a": 1, "sub": {"a": 2, "c": [{"a": 3}]}}, "a") -> [1, 2, 3]
    """
    results: List[Any] = []

    if isinstance(d, dict):
        for k, v in d.items():
            if k == target_key:
                results.append(v)
            results.extend(check_key_recursive(v, target_key))
    elif isinstance(d, list):
        for item in d:
            results.extend(check_key_recursive(item, target_key))

    return results


def check_all_keys_exist(d: dict, keys: Iterable[Any]) -> bool:
    """
    Checks whether ALL specified keys exist in the dictionary.

    Args:
        d: Input dictionary.
        keys: Iterable of keys to check.

    Returns:
        True if every key in keys exists in d, False otherwise.

    Example:
        check_all_keys_exist({"name": "Alice", "age": 30}, ["name", "age"]) -> True
        check_all_keys_exist({"name": "Alice"}, ["name", "age"]) -> False
    """
    if not isinstance(d, dict):
        return False
    return all(key in d for key in keys)


def check_any_key_exists(d: dict, keys: Iterable[Any]) -> bool:
    """
    Checks whether AT LEAST ONE of the specified keys exists in the dictionary.

    Args:
        d: Input dictionary.
        keys: Iterable of keys to check.

    Returns:
        True if at least one key exists in d, False otherwise.

    Example:
        check_any_key_exists({"name": "Alice"}, ["age", "name"]) -> True
        check_any_key_exists({"name": "Alice"}, ["age", "city"]) -> False
    """
    if not isinstance(d, dict):
        return False
    return any(key in d for key in keys)


def get_missing_keys(d: dict, required_keys: Iterable[Any]) -> Set[Any]:
    """
    Identifies which required keys are missing from the dictionary using set operations.

    Args:
        d: Input dictionary.
        required_keys: Iterable of expected keys.

    Returns:
        Set of keys present in required_keys but absent in d.

    Example:
        get_missing_keys({"a": 1}, ["a", "b", "c"]) -> {"b", "c"}
    """
    if not isinstance(d, dict):
        return set(required_keys)
    return set(required_keys) - set(d.keys())


def check_key_case_insensitive(d: dict, search_key: str) -> Tuple[bool, Optional[str], Any]:
    """
    Checks for a string key in dictionary ignoring case sensitivity.

    Args:
        d: Input dictionary with string keys.
        search_key: Target key string to match case-insensitively.

    Returns:
        Tuple (exists: bool, matching_actual_key: Optional[str], value: Any).

    Example:
        check_key_case_insensitive({"User_Name": "Alice"}, "username") -> (True, "User_Name", "Alice")
        check_key_case_insensitive({"User_Name": "Alice"}, "user_name") -> (True, "User_Name", "Alice")
        check_key_case_insensitive({"User_Name": "Alice"}, "email") -> (False, None, None)
    """
    if not isinstance(d, dict) or not isinstance(search_key, str):
        return False, None, None

    normalized_target = search_key.lower()
    for k, v in d.items():
        if isinstance(k, str) and k.lower() == normalized_target:
            return True, k, v

    return False, None, None


def search_keys_by_regex(d: dict, pattern: str) -> Dict[str, Any]:
    """
    Finds all dictionary key-value pairs where string keys match a regular expression pattern.

    Args:
        d: Input dictionary.
        pattern: Regex pattern string.

    Returns:
        Sub-dictionary containing matching key-value pairs.

    Example:
        search_keys_by_regex({"user_id": 1, "user_name": "Bob", "age": 25}, r"^user_")
        -> {"user_id": 1, "user_name": "Bob"}
    """
    if not isinstance(d, dict) or not pattern:
        return {}

    compiled_regex = re.compile(pattern)
    matched: Dict[str, Any] = {}

    for k, v in d.items():
        if isinstance(k, str) and compiled_regex.search(k):
            matched[k] = v

    return matched


def validate_dict_schema(d: dict, schema: Dict[str, type]) -> Dict[str, Any]:
    """
    Validates dictionary against a schema defining required keys and expected data types.

    Args:
        d: Input dictionary.
        schema: Mapping of required key names -> expected Python data types.

    Returns:
        Dict containing 'valid' (bool), 'missing_keys' (list), and 'type_mismatches' (list).

    Example:
        validate_dict_schema({"name": "Alice", "age": "thirty"}, {"name": str, "age": int, "email": str})
        -> {'valid': False, 'missing_keys': ['email'], 'type_mismatches': [('age', int, str)]}
    """
    missing_keys: List[str] = []
    type_mismatches: List[Tuple[str, type, type]] = []

    if not isinstance(d, dict):
        return {
            "valid": False,
            "missing_keys": list(schema.keys()),
            "type_mismatches": []
        }

    for req_key, expected_type in schema.items():
        if req_key not in d:
            missing_keys.append(req_key)
        else:
            val = d[req_key]
            if not isinstance(val, expected_type):
                type_mismatches.append((req_key, expected_type, type(val)))

    is_valid = len(missing_keys) == 0 and len(type_mismatches) == 0

    return {
        "valid": is_valid,
        "missing_keys": missing_keys,
        "type_mismatches": type_mismatches
    }


class TestCheckKeyExist(unittest.TestCase):
    """Unit test suite for Day 36: Check Key Exist algorithms."""

    def test_check_key_in(self):
        sample = {"a": 1, "b": 2, 3: "three", None: "none"}
        self.assertTrue(check_key_in(sample, "a"))
        self.assertTrue(check_key_in(sample, 3))
        self.assertTrue(check_key_in(sample, None))
        self.assertFalse(check_key_in(sample, "c"))
        self.assertFalse(check_key_in(None, "a"))

    def test_check_key_get(self):
        sample = {"a": 10, "b": None}
        self.assertEqual(check_key_get(sample, "a"), (True, 10))
        self.assertEqual(check_key_get(sample, "b"), (True, None))
        self.assertEqual(check_key_get(sample, "c"), (False, None))

    def test_check_key_has_keys(self):
        sample = {"x": 1, "y": 2}
        self.assertTrue(check_key_has_keys(sample, "x"))
        self.assertFalse(check_key_has_keys(sample, "z"))

    def test_check_nested_key(self):
        nested = {"user": {"profile": {"id": 101, "name": "Alice"}}}
        self.assertEqual(check_nested_key(nested, ["user", "profile", "id"]), (True, 101))
        self.assertEqual(check_nested_key(nested, ["user", "profile", "email"]), (False, None))
        self.assertEqual(check_nested_key(nested, ["user", "settings"]), (False, None))

    def test_check_key_recursive(self):
        tree = {"id": 1, "child": {"id": 2, "items": [{"id": 3}, {"other": 4}]}}
        ids = check_key_recursive(tree, "id")
        self.assertEqual(ids, [1, 2, 3])

    def test_check_all_keys_exist(self):
        data = {"name": "Alice", "age": 30, "city": "NY"}
        self.assertTrue(check_all_keys_exist(data, ["name", "age"]))
        self.assertFalse(check_all_keys_exist(data, ["name", "zip"]))

    def test_check_any_key_exists(self):
        data = {"name": "Alice", "age": 30}
        self.assertTrue(check_any_key_exists(data, ["zip", "name"]))
        self.assertFalse(check_any_key_exists(data, ["zip", "country"]))

    def test_get_missing_keys(self):
        data = {"a": 1, "b": 2}
        missing = get_missing_keys(data, ["a", "b", "c", "d"])
        self.assertEqual(missing, {"c", "d"})

    def test_check_key_case_insensitive(self):
        data = {"User_Name": "Alice", "API_KEY": "secret"}
        self.assertEqual(check_key_case_insensitive(data, "user_name"), (True, "User_Name", "Alice"))
        self.assertEqual(check_key_case_insensitive(data, "api_key"), (True, "API_KEY", "secret"))
        self.assertEqual(check_key_case_insensitive(data, "missing"), (False, None, None))

    def test_search_keys_by_regex(self):
        data = {"user_id": 1, "user_name": "Bob", "app_version": "1.0", "user_email": "b@x.com"}
        matched = search_keys_by_regex(data, r"^user_")
        self.assertEqual(set(matched.keys()), {"user_id", "user_name", "user_email"})

    def test_validate_dict_schema(self):
        schema = {"name": str, "age": int, "email": str}
        valid_data = {"name": "Alice", "age": 30, "email": "a@x.com"}
        invalid_data = {"name": "Alice", "age": "thirty"}

        self.assertTrue(validate_dict_schema(valid_data, schema)["valid"])
        res = validate_dict_schema(invalid_data, schema)
        self.assertFalse(res["valid"])
        self.assertIn("email", res["missing_keys"])
        self.assertEqual(len(res["type_mismatches"]), 1)


def main():
    print("=" * 60)
    print("🐍 300 Days of Python - Day 36: Check Key Exist")
    print("=" * 60)

    sample_dict = {
        "User_ID": 1001,
        "User_Name": "Alice",
        "email_address": "alice@example.com",
        "is_active": True,
        "nested_config": {
            "theme": "dark",
            "notifications": {"email": True, "sms": False}
        }
    }

    print("\n1️⃣ Direct Membership Key Checks:")
    print("   - 'User_Name' in dict:", check_key_in(sample_dict, "User_Name"))
    print("   - 'phone' in dict:", check_key_in(sample_dict, "phone"))

    print("\n2️⃣ Sentinel-Based Safe Value Retrieval (.get()):")
    print("   - 'is_active':", check_key_get(sample_dict, "is_active"))
    print("   - 'missing_key':", check_key_get(sample_dict, "missing_key"))

    print("\n3️⃣ Nested Path Traversal:")
    path = ["nested_config", "notifications", "email"]
    print(f"   - Path {path}:", check_nested_key(sample_dict, path))

    print("\n4️⃣ Recursive Search for 'email':")
    print("   - All values under key 'email':", check_key_recursive(sample_dict, "email"))

    print("\n5️⃣ Case-Insensitive Key Search:")
    print("   - Search 'user_name':", check_key_case_insensitive(sample_dict, "user_name"))

    print("\n6️⃣ Regex Pattern Matching (keys ending in '_address' or starting with 'User_'):")
    print("   - Matches:", search_keys_by_regex(sample_dict, r"^User_|_address$"))

    print("\n🧪 Running Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCheckKeyExist)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("✅ All Day 36 unit tests passed successfully!")
    else:
        print("❌ Some unit tests failed.")


if __name__ == "__main__":
    main()






