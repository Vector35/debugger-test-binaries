// tests: getcwd

#include <stdio.h>

#if defined(_WIN32) || defined(_WIN64)
#include <direct.h>
#define CWDFUNC _getcwd
#else
#include <unistd.h>
#define CWDFUNC getcwd
#endif

int main(int argc, char **argv)
{
	char path[1024] = {};
	if (CWDFUNC(path, sizeof(path)))
	{
		printf("cwd: %s\n", path);
	}
	else
	{
		printf("fail to get cwd\n");
	}

	return 0;
}
