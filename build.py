import platform
import sys
import os
import subprocess
import zipfile
import glob


def run_cmd(cmd: str) -> bool:
    print(cmd)
    ok = subprocess.call(cmd, shell=True) == 0
    if not ok:
        print("Command failed")
        return False

    return True


def create_archive():
    pass
    # print("\nCreating archive...")
    # with zipfile.ZipFile('binaries.zip', 'w', zipfile.ZIP_DEFLATED) as z:
    #     for root, dirs, files in os.walk('binaries'):
    #         for file in files:
    #             print(f"Adding {root}/{file}...")
    #             z.write(os.path.join(root, file), os.path.join(root, file))


def mac_build():
    build_cmd = f"cmake -B build/arm64 -DARCH=arm64 . && cd build/arm64 && make"
    if not run_cmd(build_cmd):
        return False

    build_cmd = f"cmake -B build/x86_64 -DARCH=x86_64 . && cd build/x86_64 && make"
    if not run_cmd(build_cmd):
        return False

    create_archive()
    return True


def linux_build():
    build_cmd = f"cmake -B build/x86_64 -DARCH=x86_64 . && cd build/x86_64 && make"
    if not run_cmd(build_cmd):
        return False

    build_cmd = f"cmake -B build/x86 -DARCH=x86 . && cd build/x86 && make"
    if not run_cmd(build_cmd):
        return False

    build_cmd = f"cmake -B build/arm64 -DARCH=arm64 -DCROSS_COMPILE_LINUX=ON . && cd build/arm64 && make"
    if not run_cmd(build_cmd):
        return False

    create_archive()
    return True


def windows_build():
    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars64.bat" && set""", shell=True)
    for line in vcvars.split(b'\r\n'):
        line = line.strip()
        if b'=' not in line:
            continue
        parts = line.split(b'=')
        key = parts[0].decode()
        value = b'='.join(parts[1:]).decode()
        os.environ[key] = value

    build_cmd = f"cmake -B build/x86_64 -G \"NMake Makefiles\" -DCMAKE_BUILD_TYPE=Release -DARCH=x86_64 . && cd build/x86_64 && nmake"
    if not run_cmd(build_cmd):
        return False

    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Enterprise\VC\Auxiliary\Build\vcvars32.bat" && set""", shell=True)
    for line in vcvars.split(b'\r\n'):
        line = line.strip()
        if b'=' not in line:
            continue
        parts = line.split(b'=')
        key = parts[0].decode()
        value = b'='.join(parts[1:]).decode()
        os.environ[key] = value

    build_cmd = f"cmake -B build/x86 -G \"NMake Makefiles\" -DCMAKE_BUILD_TYPE=Release -DARCH=x86 . && cd build/x86 && nmake"
    if not run_cmd(build_cmd):
        return False

    create_archive()
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
