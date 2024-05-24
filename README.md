Bulk-Vscode-Restore restores lost files in vscode by recreating the right file path, name, and restoring the latest save through vscodes's local history.

## Local History

Have you accidentally permanently deleted some important programming files? If you were using vscode, local history is here to save you.

You can find it at the bottom left in the timeline.

![image](https://github.com/PythonDominator/Bulk-Vscode-Restore/assets/102424561/de35b462-dc50-402e-82b6-dfec0c276a24)

You can also find it by pressing `CTRL+SHIFT+P` and then typing `Explorer: Focus on Timeline View`
![image](https://github.com/PythonDominator/Bulk-Vscode-Restore/assets/102424561/2928731c-922f-4942-8ef3-077094e62a66)

It saves a bunch of saves for every file you had. You can right-click on point and restore it.

![image](https://github.com/PythonDominator/Bulk-Vscode-Restore/assets/102424561/0507c034-c40b-4a5b-821f-ce533c906989)

## Problem
If you deleted a file you will have to put the file back with the right path and name in order to restore it. If you deleted hundreds of files this can be very tedious. Bulk-Vscode-Restore can recreate the right file path, name, and restore the latest save for hundreds of files instantly.

# Usage
1. Copy the code from `restore.py`
2. Naviagate the parent folder of where you put `restore.py` in
3. Find where local history is stored (For Windows it is `C:\Users\[YOUR_USERNAME_HERE]\AppData\Roaming\Code\User\History`)
4. Run:
```
python restore.py [restore_from] [history] [restore_to]
```
   
## Example:
```
python restore.py C:\Users\Joe\Downloads\Programming\MyLostProject C:\Users\Joe\AppData\Roaming\Code\User\History C:\Users\Joe\OneDrive\Documents\RestoredProject
```
