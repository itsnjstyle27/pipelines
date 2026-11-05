# Copyright 2022 The Kubeflow Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for `dsl compile` command group in KFP CLI."""

import unittest

from kfp import dsl
from kfp.cli import compile_


class TestIsPipelineOrComponent(unittest.TestCase):
    def test_is_pipeline(self):

        @dsl.component
        def my_comp():
            pass

        @dsl.container_component
        def my_container_comp():
            return dsl.ContainerSpec(
                image='python:3.11',
                command=['echo', 'hello world'],
                args=[],
            )

        def my_func(a: str, b: int):
            pass

        @dsl.pipeline(name='my-pipeline')
        def my_pipeline(a: str, b: int):
            my_comp()

        self.assertFalse(compile_.is_pipeline_func(my_comp))
        self.assertFalse(compile_.is_pipeline_func(my_container_comp))
        self.assertFalse(compile_.is_pipeline_func(my_func))
        self.assertTrue(compile_.is_pipeline_func(my_pipeline))

    def test_is_component(self):

        @dsl.component
        def my_comp():
            pass

        @dsl.container_component
        def my_container_comp():
            return dsl.ContainerSpec(
                image='python:3.11',
                command=['echo', 'hello world'],
                args=[],
            )

        def my_func(a: str, b: int):
            pass

        @dsl.pipeline(name='my-pipeline')
        def my_pipeline(a: str, b: int):
            my_comp()

        self.assertTrue(compile_.is_component_func(my_comp))
        self.assertTrue(compile_.is_component_func(my_container_comp))
        self.assertFalse(compile_.is_component_func(my_func))
        self.assertFalse(compile_.is_component_func(my_pipeline))


class TestParseParameters(unittest.TestCase):
    def test_no_parameters(self):
        self.assertEqual(compile_.parse_parameters(None), {})

    def test_json_object(self):
        self.assertEqual(
            compile_.parse_parameters('{"a": 1, "b": "x"}'), {'a': 1, 'b': 'x'}
        )

    def test_json_null(self):
        self.assertEqual(compile_.parse_parameters('null'), {})

    def test_json_value_that_is_not_an_object_raises(self):
        for parameters in ['[1, 2]', '"a"', '1']:
            with self.subTest(parameters=parameters):
                with self.assertRaisesRegex(
                    ValueError, '--pipeline-parameters must be a JSON object'
                ):
                    compile_.parse_parameters(parameters)


if __name__ == '__main__':
    unittest.main()
