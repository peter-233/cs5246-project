import argparse
import os
import subprocess
import sys

NPM_EXE = r"npm"


def run_command(command: list[str], cwd: str = "./") -> int:
    try:
        ret = subprocess.call(command, cwd=cwd, shell=True)
        if ret != 0:
            sys.exit(ret)
        return ret
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr.decode()}")
        return e.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="tools for power the project")

    parser.add_argument('-b', '--backend', action='store_true', help='start the backend server')
    parser.add_argument('-ft', '--frontend-test', action='store_true', help='start the frontend server in test mode')
    parser.add_argument('-fd', '--frontend-dev', action='store_true', help='start the frontend server in dev mode')
    parser.add_argument('-fi', '--frontend-install', action='store_true', help='install the frontend dependencies')

    args = parser.parse_args()

    ret = 0
    if args.backend:
        ret = run_command(
            ['python', '-m', 'backend.app'],
            cwd='./'
        )
    elif args.frontend_test:
        path = os.path.join(os.getcwd(), 'frontend', 'read-supporter')
        print(path, os.path.exists(path))
        ret = run_command(
            [NPM_EXE, 'run', 'test'],
            cwd=os.path.join(os.getcwd(), 'frontend', 'read-supporter')
        )
    elif args.frontend_dev:
        ret = run_command(
            [NPM_EXE, 'run', 'dev'],
            cwd=os.path.join(os.getcwd(), 'frontend', 'read-supporter')
        )
    elif args.frontend_install:
        ret = run_command(
            [NPM_EXE, 'install'],
            cwd=os.path.join(os.getcwd(), 'frontend','read-supporter')
        )
    else:
        ret = -1
        print("No command specified.")
        parser.print_help()

    sys.exit(ret)
