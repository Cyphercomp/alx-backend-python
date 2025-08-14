#!/usr/bin/env python3
''' test_utils.py '''

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Any, Mapping, Sequence, Dict, Tuple


class TestAccessNestedMap(unittest.TestCase):
    '''
    Test access Nested Map class
    '''

    @parameterized.expand([
        ({"a": 1}, ["a"], 1),
        ({"a": {"b": 2}}, ["a"], {"b": 2}),
        ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence,
        expected_result: Any
    ) -> None:
        ''' test access nested map '''
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
            self,
            nested_map: Dict,
            path: Tuple[str],
            exception: Exception,
            ) -> None:
        ''' test access nested map exception '''
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    '''
    Test get Json class
    '''

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(
            self,
            test_url: str,
            test_payload: Dict,
            ) -> None:
        ''' test get json '''
        mock_attrs = {'json.return_value': test_payload}
        with patch("requests.get", return_value=Mock(**mock_attrs)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    '''
    Test Memoize class
    '''
    def test_memoize(self) -> None:
        ''' test memoize '''
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(
                TestClass, "a_method", return_value=lambda: 42
        ) as mock_method:
            test_instance = TestClass()
            result_1 = test_instance.a_property()
            result_2 = test_instance.a_property()

            self.assertEqual(result_1, 42)
            self.assertEqual(result_2, 42)
            mock_method.assert_called_once()
