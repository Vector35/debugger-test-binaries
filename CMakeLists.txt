cmake_minimum_required(VERSION 3.13 FATAL_ERROR)

# This project builds the test binaries for the debugger unit test. It does not run the test.
project(debugger-test-binaries C CXX)

if (CROSS_COMPILE_LINUX)
	message("Cross compiling for Linux aarch64")
	SET(CMAKE_SYSTEM_NAME Linux)
	SET(CMAKE_SYSTEM_VERSION 1)
	SET(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
	SET(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
	SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
	SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
	SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
	SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
endif()

if (ARCH STREQUAL "x86_64")
	add_definitions(-DARCH_IS_X64)
elseif(ARCH STREQUAL "x86")
	add_definitions(-DARCH_IS_X86)
elseif(ARCH STREQUAL "arm64")
	add_definitions(-DARCH_IS_AARCH64)
elseif(ARCH STREQUAL "armv7")
	add_definitions(-DARCH_IS_ARMV7)
endif()

if (APPLE)
	set(CMAKE_OSX_ARCHITECTURES ${ARCH})
else()
	if (ARCH STREQUAL "x86")
		set(CMAKE_C_FLAGS -m32)
		set(CMAKE_CXX_FLAGS -m32)
	endif()
endif()

add_executable(helloworld src/helloworld.c)
set_target_properties(helloworld PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(getcwd src/getcwd.c)
set_target_properties(getcwd PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(exitcode src/exitcode.c)
set_target_properties(exitcode PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_thread src/helloworld_thread.c)
set_target_properties(helloworld_thread PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)
if(UNIX AND NOT APPLE)
	target_link_libraries(helloworld_thread pthread)
endif()

add_executable(helloworld_loop src/helloworld_loop.c)
set_target_properties(helloworld_loop PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_func src/helloworld_func.c)
set_target_properties(helloworld_func PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_recursion src/helloworld_recursion.c)
set_target_properties(helloworld_recursion PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_pie src/helloworld.c)
set_target_properties(helloworld_pie PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_thread_pie src/helloworld_thread.c)
set_target_properties(helloworld_thread_pie PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)
if(UNIX AND NOT APPLE)
	target_link_libraries(helloworld_thread_pie pthread)
endif()

add_executable(helloworld_loop_pie src/helloworld_loop.c)
set_target_properties(helloworld_loop_pie PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_func_pie src/helloworld_func.c)
set_target_properties(helloworld_func_pie PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(helloworld_recursion_pie src/helloworld_recursion.c)
set_target_properties(helloworld_recursion_pie PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

if(APPLE)
	add_executable(helloworld_objc src/helloworld_objc.m)
	set_target_properties(helloworld_objc PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	target_link_libraries(helloworld_objc
			"-framework AppKit"
			"-framework Carbon"
			"-framework Foundation")
endif()

add_executable(helloworld_virtual src/helloworld_virtual.cpp)
set_target_properties(helloworld_virtual PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(many_stdlib_calls src/many_stdlib_calls.c)
set_target_properties(many_stdlib_calls PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

add_executable(read_input src/read_input.c)
set_target_properties(read_input PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

if (ARCH STREQUAL "x86_64" OR ARCH STREQUAL "x86")
	# ASM files
	enable_language(ASM_NASM)
	# This flag is used to generate different assembly instruction on different OS
	if(APPLE)
		set(CMAKE_ASM_NASM_FLAGS "-DOS_IS_MACOS")
	elseif(WIN32)
		set(CMAKE_ASM_NASM_FLAGS "-DOS_IS_WINDOWS")
	else()
		set(CMAKE_ASM_NASM_FLAGS "-DOS_IS_LINUX")
	endif(APPLE)

	if (APPLE)
		set(CMAKE_NASM_LINK_EXECUTABLE "ld <LINK_FLAGS> -macos_version_min 10.7.0 -L/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/lib <OBJECTS> -o <TARGET> <LINK_LIBRARIES>")
	elseif (WIN32)
		set(CMAKE_NASM_LINK_EXECUTABLE "link <OBJECTS> <LINK_FLAGS> /ENTRY:WinMain /SUBSYSTEM:CONSOLE /LARGEADDRESSAWARE:NO /DYNAMICBASE:NO /OUT:<TARGET> <LINK_LIBRARIES>")
	else()
		set(CMAKE_NASM_LINK_EXECUTABLE "ld <LINK_FLAGS> <OBJECTS> -o <TARGET> <LINK_LIBRARIES>")
	endif()
endif()

if (ARCH STREQUAL "x86_64")
	add_executable(asmtest src/asmtest_x64.asm)
	if (APPLE)
		target_link_libraries(asmtest System)
	elseif (WIN32)
		target_link_libraries(asmtest kernel32)
	endif (APPLE)
	set_target_properties(asmtest PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)

	add_executable(hello src/hello_x64.asm)
	if (APPLE)
		target_link_libraries(hello System)
	elseif (WIN32)
		target_link_libraries(hello kernel32)
	endif (APPLE)
	set_target_properties(hello PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)

	if (NOT WIN32)
		add_executable(analysis_propagation src/analysis_propagation_x64.asm)
		if (APPLE)
			target_link_libraries(analysis_propagation System)
		elseif (WIN32)
			target_link_libraries(analysis_propagation kernel32)
		endif (APPLE)
		set_target_properties(analysis_propagation PROPERTIES
				POSITION_INDEPENDENT_CODE OFF
				LINKER_LANGUAGE NASM
				RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
				)
		if(APPLE)
			add_custom_command(TARGET analysis_propagation POST_BUILD
					COMMAND strip "$<TARGET_FILE:analysis_propagation>"
					COMMAND python3 ${CMAKE_SOURCE_DIR}/src/rm_func_starts.py "$<TARGET_FILE:analysis_propagation>")
		elseif (UNIX)
			add_custom_command(TARGET analysis_propagation POST_BUILD
					COMMAND strip "$<TARGET_FILE:analysis_propagation>")
		endif()
	endif()

	add_executable(missing_switch_case src/missing_switch_case_x64.asm)
	if (APPLE)
		target_link_libraries(missing_switch_case System)
	elseif (WIN32)
		target_link_libraries(missing_switch_case kernel32)
	endif (APPLE)
	set_target_properties(missing_switch_case PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	if(APPLE)
		add_custom_command(TARGET missing_switch_case POST_BUILD
				COMMAND strip "$<TARGET_FILE:missing_switch_case>"
				COMMAND python3 ${CMAKE_SOURCE_DIR}/src/rm_func_starts.py "$<TARGET_FILE:missing_switch_case>")
	elseif (UNIX)
		add_custom_command(TARGET missing_switch_case POST_BUILD
				COMMAND strip "$<TARGET_FILE:missing_switch_case>")
	endif()

	add_executable(undiscovered_func src/undiscovered_func_x64.asm)
	if (APPLE)
		target_link_libraries(undiscovered_func System)
	elseif (WIN32)
		target_link_libraries(undiscovered_func kernel32)
	endif (APPLE)
	set_target_properties(undiscovered_func PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	if(APPLE)
		add_custom_command(TARGET undiscovered_func POST_BUILD
				COMMAND strip "$<TARGET_FILE:undiscovered_func>"
				COMMAND python3 ${CMAKE_SOURCE_DIR}/src/rm_func_starts.py "$<TARGET_FILE:undiscovered_func>")
	elseif (UNIX)
		add_custom_command(TARGET undiscovered_func POST_BUILD
				COMMAND strip "$<TARGET_FILE:undiscovered_func>")
	endif()

	if (NOT WIN32)
		add_executable(undiscovered_func2 src/undiscovered_func2_x64.asm)
		if (APPLE)
			target_link_libraries(undiscovered_func2 System)
		elseif (WIN32)
			target_link_libraries(undiscovered_func2 kernel32)
		endif (APPLE)
		set_target_properties(undiscovered_func2 PROPERTIES
				POSITION_INDEPENDENT_CODE OFF
				LINKER_LANGUAGE NASM
				RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
				)
		if (APPLE)
			add_custom_command(TARGET undiscovered_func2 POST_BUILD
					COMMAND strip "$<TARGET_FILE:undiscovered_func2>"
					COMMAND python3 ${CMAKE_SOURCE_DIR}/src/rm_func_starts.py "$<TARGET_FILE:undiscovered_func2>")
		elseif (UNIX)
			add_custom_command(TARGET undiscovered_func2 POST_BUILD
					COMMAND strip "$<TARGET_FILE:undiscovered_func2>")
		endif()
	endif()

	add_executable(indirect_calls src/indirect_calls_x64.asm)
	if (APPLE)
		target_link_libraries(indirect_calls System)
	elseif (WIN32)
		target_link_libraries(indirect_calls kernel32)
	endif (APPLE)
	set_target_properties(indirect_calls PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	if (APPLE)
		add_custom_command(TARGET indirect_calls POST_BUILD
				COMMAND strip "$<TARGET_FILE:indirect_calls>"
				COMMAND python3 ${CMAKE_SOURCE_DIR}/src/rm_func_starts.py "$<TARGET_FILE:indirect_calls>")
	elseif (UNIX)
		add_custom_command(TARGET indirect_calls POST_BUILD
				COMMAND strip "$<TARGET_FILE:indirect_calls>")
	endif()
endif()


if (ARCH STREQUAL "x86")
	add_executable(asmtest src/asmtest_x86.asm)
	set_target_properties(asmtest PROPERTIES
			POSITION_INDEPENDENT_CODE OFF
			LINKER_LANGUAGE NASM
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	if (WIN32)
		target_link_libraries(asmtest kernel32)
	endif()
endif()


add_executable(do_exception src/do_exception.c)
set_target_properties(do_exception PROPERTIES
		POSITION_INDEPENDENT_CODE OFF
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)

if (NOT WIN32)
	add_executable(nopspeed src/nopspeed.c)
	set_target_properties(nopspeed PROPERTIES
			POSITION_INDEPENDENT_CODE ON
			RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
			)
	target_compile_options(nopspeed PUBLIC -O3)
endif()

add_executable(cat src/cat.c)
set_target_properties(cat PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)
if (NOT WIN32)
	target_compile_options(cat PUBLIC -O3)
endif()

add_executable(commandline_test src/commandline_test.c)
set_target_properties(commandline_test PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)
if (NOT WIN32)
	target_compile_options(commandline_test PUBLIC -O3)
endif()

file(GLOB MD5_SOURCES
		src/md5/*.c
		src/md5/*.h
		)
add_executable(md5 ${MD5_SOURCES})
set_target_properties(md5 PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		)
if (NOT WIN32)
	target_compile_options(md5 PUBLIC -g -DMD=5)
else()
	target_compile_options(md5 PUBLIC -DMD=5)
endif()


add_library(library SHARED src/debug_library/library.h src/debug_library/library.c)
set_target_properties(library PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
)
if (WIN32)
	set_target_properties(library PROPERTIES
			WINDOWS_EXPORT_ALL_SYMBOLS ON
	)
endif ()

add_executable(test_library src/debug_library/main.c)
target_link_libraries(test_library library)
set_target_properties(test_library PROPERTIES
		POSITION_INDEPENDENT_CODE ON
		LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
		RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/binaries/${CMAKE_SYSTEM_NAME}-${ARCH}
)

if (APPLE)
	set_property(TARGET test_library APPEND PROPERTY INSTALL_RPATH "@loader_path")
	set_target_properties(test_library PROPERTIES
			BUILD_WITH_INSTALL_RPATH TRUE)
elseif (UNIX)
	set_property(TARGET test_library APPEND PROPERTY INSTALL_RPATH "\$ORIGIN")
	set_target_properties(test_library PROPERTIES
			BUILD_WITH_INSTALL_RPATH TRUE)
endif ()