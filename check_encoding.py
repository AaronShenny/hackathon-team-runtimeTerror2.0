import os

def check_files(directory):
    for root, dirs, files in os.walk(directory):
        if 'venv' in dirs:
            dirs.remove('venv')
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'rb') as f:
                        content = f.read()
                        if b'\x00' in content:
                            print(f"NULL BYTES FOUND: {path}")
                        # Try to decode as utf-8
                        content.decode('utf-8')
                except UnicodeDecodeError:
                    print(f"ENCODING ERROR (not UTF-8): {path}")
                except Exception as e:
                    print(f"ERROR reading {path}: {e}")

if __name__ == "__main__":
    check_files('.')
