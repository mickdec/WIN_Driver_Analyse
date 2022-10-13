import subprocess

#Based on https://www.synacktiv.com/sites/default/files/2021-10/2021_sthack_windows_lpe.pdf
#Need : i686-w64-mingw32-gcc.exe from cygwin
#Need DriverQUery from https://github.com/matterpreter/OffensiveCSharp
#       Compile with > C:\Windows\Microsoft.Net\Framework\V3.5\csc.exe

c = """#include <stdio.h>
#include <tchar.h>
#include <Windows.h>

#define DRIVER_PATH "\\\\\\\\.\\\\DRIVER_NAME"
#define IOCTL_CODE 0x8001E000

int main()
{
	DWORD bResult;
	DWORD junk = 0;
    HANDLE _hDriver = CreateFileA(DRIVER_PATH,GENERIC_READ | GENERIC_WRITE,FILE_SHARE_WRITE,NULL,
				    OPEN_EXISTING,FILE_FLAG_OVERLAPPED | FILE_ATTRIBUTE_NORMAL,NULL);
    if(_hDriver == INVALID_HANDLE_VALUE) {
        printf("Failed to get driver handle. Status 0x%X\\n", GetLastError());
    } else {
        printf("Acquired a driver handle!\\n");
    }
	CloseHandle(_hDriver);
    return 0x0;
}"""

stdout = subprocess.run("Program.exe", shell=True, stdout=subprocess.PIPE).stdout.decode('cp1252', errors="ignore").split("\n")
for driver in stdout:
    if "Service Name:" in driver:
        driver = driver.replace("Service Name:","").replace(" ","")
        f = open("compil.c","w+")
        f.write(c.replace("DRIVER_NAME",driver))
        f.close()
        stdout2 = subprocess.run("i686-w64-mingw32-gcc.exe -w .\compil.c && a.exe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.decode('cp1252', errors="ignore")
        if "Acquired a driver handle!" in stdout2:
            print("Driver "+driver+" OK")
            f = open("Open_Driver_RES", "a+")
            f.write("[+] Driver "+driver+" OK\n")
            f.close()
        f = open("Open_Driver_RES", "a+")
        f.write("[-] Driver "+driver+" NOK\n")
        f.close()