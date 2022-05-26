from winreg import (
  ConnectRegistry,
  OpenKey,
  KEY_ALL_ACCESS,
  EnumValue,
  QueryInfoKey,
  HKEY_LOCAL_MACHINE,
  HKEY_USERS
)
targetSID = "S-S-1-15-1-404565...."
def enum_key(hive, subkey:str):
    with OpenKey(hive, subkey, 0, KEY_ALL_ACCESS) as key:
        num_of_values = QueryInfoKey(key)[1]
        for i in range(num_of_values):
            values = EnumValue(key, i)
            if values[0] == "LangID": continue
            print(*values[:-1], sep="\t")
if __name__ == "__main__":
    # Connecting to the HKEY_LOCAL_MACHINE hive
    # Looking for possible persistence or evidence of malicious activity
    with ConnectRegistry(None, HKEY_LOCAL_MACHINE) as hklm_hive:
        print("\nSystem Environment Variables")
        print("-"*50)
        enum_key(hklm_hive, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
        print("\nStartup Applications")
        print("-"*50)
        enum_key(hklm_hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        print("\nShell Folders")
        print("-"*50)
        enum_key(hklm_hive, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        print("\nWinLogon User Init Check")
        print("-"*50)
        enum_key(hklm_hive, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\WinLogon")
        print("\nBoot Execute Check - value should be autocheck autochk *")
        print("-"*50)
        enum_key(hklm_hive, r"SYSTEM\CurrentControlSet\Control\Session Manager")
    # Connecting to the HKEY_USER hive
    # Enumerating the suspicious users recent activity and possible persistence in user key
    with ConnectRegistry(None, HKEY_USERS) as hku_hive:
        print("\nPreviously Ran Applications")
        print("-"*50)
        enum_key(hku_hive, r"{}\SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\Shell\MuiCache".format(targetSID))
        print("\nRecently Opened Programs/Files/URLs")
        print("-"*50)
        enum_key(hku_hive, r"{}\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU".format(targetSID))
        enum_key(hku_hive, r"{}\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU".format(targetSID))
        print("\nFiles Recently Opened from Explorer")
        print("-"*50)
        enum_key(hku_hive, r"{}\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs".format(targetSID))
        print("\nSuspicious User Run Key")
        print("-"*50)
        enum_key(hku_hive, r"{}\SOFTWARE\Microsoft\Windows\CurrentVersion\Run".format(targetSID))

