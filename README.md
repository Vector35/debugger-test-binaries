# debugger-test-binaries
Source and binary of test binaries for the Binary Ninja Debugger

## macOS

- arm64
```zsh
cd test
cmake -DARCH=arm64 .
make
```
Build results are in `binaries/Darwin-arm64`.
- x86_64
```zsh
cd test
cmake -DARCH=x86_64 .
make
```
Build results are in `binaries/Darwin-x86_64`.

## Linux
- x86_64
```Bash
cd test
cmake -DARCH=x86_64 .
make
```
Build results are in `binaries/Linux-x86_64`.
- x86
```Bash
cd test
cmake -DARCH=x86 .
make
```
Build results are in `binaries/Linux-x86`.

## Windows
- x86_64

Open x64 Visual Studio command prompt
```cmd
cd test
cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release -DARCH=x86_64 .
nmake
```

- x86
  Open x86 Visual Studio command prompt
```cmd
cd test
cmake -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release -DARCH=x86 .
nmake
```