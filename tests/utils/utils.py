import subprocess

COMPILER_TIMEOUT = 'El compilador tarda mucho en responder.'
TEST_MUST_FAIL = 'El test %s debe fallar al compilar'
TEST_MUST_COMPILE = 'El test %s debe compilar'
BAD_ERROR_FORMAT = '''El error no esta en formato: (<línea>,<columna>) - <tipo_de_error>: <texto_del_error>
                        o no se encuentra en la 3ra linea'''
UNEXPECTED_ERROR = 'Se esperaba un %s en (%d, %d). Su error fue un %s en (%d, %d)'

def compare_errors(compiler_path: str, cool_file_path: str, error_file_path: str, timeout=10):
    try:
        sp = subprocess.run(['bash', compiler_path, cool_file_path], capture_output=True, timeout=timeout)
        return_code, output = sp.returncode, sp.stdout.decode().split('\n')
    except TimeoutError:
        assert False, COMPILER_TIMEOUT

    if error_file_path:
        assert return_code == 1, TEST_MUST_FAIL % cool_file_path

    
        fd = open(error_file_path, 'r')
        line, column, error_type = fd.read().split()
        fd.close()

        try:
            oerror, _ = output[2].split(':')
            opos, oerror_type = oerror.replace(' ', '').split('-')
            oline, ocolumn = (int(x) for x in opos[1:-1].split(','))
        except Exception as ex:
            print(ex)
            assert False, BAD_ERROR_FORMAT

        assert line == oline and column == ocolumn and error_type == oerror_type,\
            UNEXPECTED_ERROR % (error_type, line, column, oerror_type, oline, ocolumn)
    else:
        assert return_code == 0, TEST_MUST_COMPILE % cool_file_path