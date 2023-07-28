import marshal
import zlib
import base64
import os
import time
from sys import exit


def make_encoded_file(input_file_path):
  directory_path = os.path.dirname(input_file_path)
  encoded_code_filename = '_code_.py'
    
  with open(input_file_path, mode='r', encoding='utf-8') as f:
    code = f.read()

  encoded_code = base64.b64encode(zlib.compress(marshal.dumps(compile(code, 'main', 'exec'))))

  encoded_code_file_path = os.path.join(directory_path, encoded_code_filename)

  formatted_encoded_code = f'SCRIPT="{encoded_code.decode()}"'

  with open(encoded_code_file_path, 'w', encoding='utf-8') as f:
    f.write(formatted_encoded_code)
    
  print(f'\nEncoding Done! Check the path \"{encoded_code_file_path}\"')
  return code

def find_imported_module(code):
  code_lines = code.split('\n')
  imported_module = ''
  for line in code_lines:
    if line.startswith('import ') or line.startswith('from '):
      imported_module += line + '\n'
  return imported_module


def make_run_py_file(input_file_path, code):
  
  directory_path = os.path.dirname(input_file_path)
  run_py_file_path = os.path.join(directory_path, 'run.py')
  imported_module = find_imported_module(code)
  template = f"""
import marshal, zlib, base64
{imported_module}
from _code_ import SCRIPT

script = SCRIPT.encode()
  
script = marshal.loads(zlib.decompress(base64.b64decode(script)))
exec(script)
  """
  
  with open(run_py_file_path, 'w', encoding='utf=8') as f:
    f.write(template)
  print(f"\n{run_py_file_path} file created!")


def main():
  input_file_path = input('\nEnter the file path: ')

  _, file_extension = os.path.splitext(input_file_path)

  if not os.path.exists(input_file_path) or file_extension.lower() != '.py':
    print(f'\n\"{input_file_path}\" file not exists or invalid file.')
    time.sleep(3)
    exit()
  
  script = make_encoded_file(input_file_path)
  make_run_py_file(input_file_path, script)
  time.sleep(3)
  
if __name__=='__main__':
  main()