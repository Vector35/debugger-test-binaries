import platform
import sys
import os
import subprocess


def run_cmd(cmd: str) -> bool:
    print(cmd)
    ok = subprocess.call(cmd, shell=True) == 0
    if not ok:
        print("Command failed")
        return False

    return True


def mac_sign():
    pass


def mac_build():
    build_cmd = f"cmake -DARCH=arm64 . && make"
    if not run_cmd(build_cmd):
        return False

    build_cmd = f"cmake -DARCH=x86_64 . && make"
    if not run_cmd(build_cmd):
        return False

    return True


def linux_build():
    build_cmd = f"cmake -DARCH=x86 . && make"
    if not run_cmd(build_cmd):
        return False

    build_cmd = f"cmake -DARCH=x86_64 . && make"
    if not run_cmd(build_cmd):
        return False

    return True


def windows_build():
    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat" && set""", shell=True)
    for line in vcvars.split(b'\r\n'):
        line = line.strip()
        if b'=' not in line:
            continue
        parts = line.split(b'=')
        key = parts[0].decode()
        value = b'='.join(parts[1:]).decode()
        os.environ[key] = value

    build_cmd = f"cmake -G \"NMake Makefiles\" -DCMAKE_BUILD_TYPE=Release -DARCH=x86_64 . && nmake"
    if not run_cmd(build_cmd):
        return False


    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars32.bat" && set""", shell=True)
    for line in vcvars.split(b'\r\n'):
        line = line.strip()
        if b'=' not in line:
            continue
        parts = line.split(b'=')
        key = parts[0].decode()
        value = b'='.join(parts[1:]).decode()
        os.environ[key] = value

    build_cmd = f"cmake -G \"NMake Makefiles\" -DCMAKE_BUILD_TYPE=Release -DARCH=x86 . && nmake"
    if not run_cmd(build_cmd):
        return False

    return True


def main():
    if platform.system() == "Linux":
        ok = linux_build()
    elif platform.system() == "Darwin":
        ok = mac_build()
    elif platform.system() == "Windows":
        ok = windows_build()
    else:
        print("Unknown platform %s" % platform.system())
        ok = False

    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
