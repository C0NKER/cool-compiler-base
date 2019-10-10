import subprocess

def test_compiler(compiler_path:str, cool_file_path:str, timeout=10):
    try:
        sp = subprocess.run(['bash', compiler_path, cool_file_path], capture_output=True, timeout=timeout)
        return sp.returncode, sp.stdout.decode().split('\n')
    except TimeoutError:
        return None, None