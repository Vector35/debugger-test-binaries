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
    print("\nCreating archive...")
    with zipfile.ZipFile('binaries.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk('binaries'):
            for file in files:
                print(f"Adding {root}/{file}...")
                z.write(os.path.join(root, file), os.path.join(root, file))


def keychain_unlocker():
    keychain_unlocker = os.environ["HOME"] + "/unlock-keychain"
    if os.path.exists(keychain_unlocker):
        return subprocess.call([keychain_unlocker]) == 0
    return False


def mac_sign(path):
    if not keychain_unlocker():
        return False

    args = ['codesign']
    args += ["--options", "runtime", "--entitlements", "entitlements.plist", "--timestamp", "-s", "Developer ID"]
    for f in glob.glob(path):
        args.append(f)

    return subprocess.call(args) == 0


def mac_build():
    if not os.path.exists('build/arm64'):
        os.makedirs('build/arm64')

    build_cmd = f"cmake -B build/arm64 -DARCH=arm64 . && cd build/arm64 && make"
    if not run_cmd(build_cmd):
        return False

    if not os.path.exists('build/x86_64'):
        os.makedirs('build/x86_64')

    build_cmd = f"cmake -B build/x86_64 -DARCH=x86_64 . && cd build/x86_64 && make"
    if not run_cmd(build_cmd):
        return False

    if not mac_sign('binaries/*/*'):
        print('codesign failed')
        return False

    create_archive()
    return True


def linux_build():
    if not os.path.exists('build/x86_64'):
        os.makedirs('build/x86_64')

    build_cmd = f"cmake -B build/x86_64 -DARCH=x86_64 . && cd build/x86_64 && make"
    if not run_cmd(build_cmd):
        return False

    if not os.path.exists('build/x86'):
        os.makedirs('build/x86')

    build_cmd = f"cmake -B build/x86 -DARCH=x86 . && cd build/x86 && make"
    if not run_cmd(build_cmd):
        return False

    create_archive()
    return True


def windows_build():
    if not os.path.exists('build/x86_64'):
        os.makedirs('build/x86_64')

    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars64.bat" && set""", shell=True)
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

    vcvars = subprocess.check_output(fR"""call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\VC\Auxiliary\Build\vcvars32.bat" && set""", shell=True)
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
