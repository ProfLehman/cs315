"""Display computer specifications using only the Python 3 standard library."""

import ctypes
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(*args):
    try:
        result = subprocess.run(args, capture_output=True, text=True,
                                timeout=5, check=True)
        return result.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def format_gib(number_of_bytes):
    return f"{number_of_bytes / (1024 ** 3):,.1f} GiB"


def cpu_model():
    system = platform.system()
    if system == "Darwin":
        return (run_command("sysctl", "-n", "machdep.cpu.brand_string")
                or run_command("sysctl", "-n", "hw.model")
                or "Unavailable")
    if system == "Windows":
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0") as key:
                return winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
        except (OSError, ImportError):
            return platform.processor() or "Unavailable"
    if system == "Linux":
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith(("model name", "Hardware", "Processor")) and ":" in line:
                    value = line.split(":", 1)[1].strip()
                    if value:
                        return value
        except OSError:
            pass
    return platform.processor() or "Unavailable"


def physical_cores():
    system = platform.system()
    if system == "Darwin":
        return run_command("sysctl", "-n", "hw.physicalcpu") or "Unavailable"
    if system == "Linux":
        try:
            content = Path("/proc/cpuinfo").read_text()
            pairs = set()
            for block in content.strip().split("\n\n"):
                fields = {}
                for line in block.splitlines():
                    if ":" in line:
                        key, value = line.split(":", 1)
                        fields[key.strip()] = value.strip()
                if "physical id" in fields and "core id" in fields:
                    pairs.add((fields["physical id"], fields["core id"]))
            if pairs:
                return len(pairs)
        except OSError:
            pass
    if system == "Windows":
        output = run_command("powershell", "-NoProfile", "-Command",
                             "(Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfCores -Sum).Sum")
        if output.isdecimal():
            return int(output)
    return "Unavailable"


def total_ram():
    system = platform.system()
    if system == "Darwin":
        value = run_command("sysctl", "-n", "hw.memsize")
        return int(value) if value.isdecimal() else None
    if system == "Linux":
        try:
            for line in Path("/proc/meminfo").read_text().splitlines():
                if line.startswith("MemTotal:"):
                    return int(line.split()[1]) * 1024
        except (OSError, ValueError, IndexError):
            pass
    if system == "Windows":
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        status = MEMORYSTATUSEX()
        status.dwLength = ctypes.sizeof(status)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            return status.ullTotalPhys
    return None


def main():
    print("=" * 48)
    print("          COMPUTER SPECIFICATIONS")
    print("=" * 48)
    print(f"Operating system:  {platform.platform()}")
    print(f"CPU model:         {cpu_model()}")
    print(f"CPU architecture:  {platform.machine()}")
    print(f"Physical cores:    {physical_cores()}")
    print(f"Logical CPUs:      {os.cpu_count() or 'Unavailable'}")
    ram = total_ram()
    print(f"Installed RAM:     {format_gib(ram) if ram else 'Unavailable'}")
    try:
        disk = shutil.disk_usage(Path.home())
        print(f"Home disk size:   {format_gib(disk.total)}")
        print(f"Home disk free:   {format_gib(disk.free)}")
    except OSError:
        print("Home disk size:   Unavailable")
        print("Home disk free:   Unavailable")
    print(f"Python version:    {platform.python_version()}")
    print(f"Python bits:       {64 if sys.maxsize > 2**32 else 32}-bit")
    print("=" * 48)
    print("Note: Linux containers and virtual machines may report")
    print("virtualized or host hardware information.")


if __name__ == "__main__":
    main()
