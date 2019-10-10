import pytest
import os
from utils import compare_errors

tests_dir = './tests/compile/'
tests = [(tests_dir + file) for file in os.listdir(tests_dir) if file.endswith('.cl')]

@pytest.mark.lexer
@pytest.mark.parser
@pytest.mark.semantic
@pytest.mark.ok
@pytest.mark.parametrize("cool_file", tests)
def test_compile(compiler_path, cool_file):
    compare_errors(compiler_path, cool_file, None)