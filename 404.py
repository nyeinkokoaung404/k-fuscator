# -*- coding: UTF-8 -*-

# 404 SMART TOOL (Modified from K-fuscator)
# Developer : Nyein Ko Ko Aung (@nkka404)
# Telegram  : https://t.me/nkka404
# Channel   : https://t.me/premium_channel_404
# Language  : Python(3)

import os, base64, sys, time
from pprint import pformat

# Emoji unicode list
alphabet = [
    "\U0001f600",
    "\U0001f603",
    "\U0001f604",
    "\U0001f601",
    "\U0001f605",
    "\U0001f923",
    "\U0001f602",
    "\U0001f609",
    "\U0001f60A",
    "\U0001f61b",
]

MAX_STR_LEN = 70
OFFSET = 10

# Basic colors
black="\033[0;30m"
red="\033[0;31m"
green="\033[0;32m"
yellow="\033[0;33m"  
blue="\033[0;34m"
purple="\033[0;35m"
cyan="\033[0;36m"
white="\033[0;37m"

# Snippets
ask = green + '\n[' + white + '?' + green + '] '+ yellow
success = green + '\n[' + white + '√' + green + '] '
error = red + '\n[' + white + '!' + red + '] '
info= yellow + '\n[' + white + '+' + yellow + '] '+ cyan

# Current Directory
pwd=os.getcwd()

# Logo of 404 SMART TOOL
logo = f'''
{cyan}  ____ _   _    _    _   _ _   _ _____ _       _  _    ___  _  _   
{cyan} / ___| | | |  / \  | \ | | \ | | ____| |     | || |  / _ \| || |  
{white}| |   | |_| | / _ \ |  \| |  \| |  _| | |     | || |_| | | | || |_ 
{white}| |___|  _  |/ ___ \| |\  | |\  | |___| |___  |__   _| |_| |__   _|
{blue} \____|_| |_/_/   \_\_| \_|_| \_|_____|_____|    |_|  \___/    |_|  
{yellow} ------------------------------------------------------------------
{green}           Developed by: Nyein Ko Ko Aung (@nkka404)
{yellow} ------------------------------------------------------------------
'''

# Normal slowly printer
def sprint(sentence, second=0.05):
    for word in sentence + '\n':
        sys.stdout.write(word)
        sys.stdout.flush()
        time.sleep(second)

# About section
def about():
    os.system("clear")
    print(logo)
    print(f"{cyan}[ToolName]  {purple} :[404 SMART TOOL]")
    print(f"{cyan}[Version]   {purple} :[2.0]")
    print(f"{cyan}[Developer] {purple} :[Nyein Ko Ko Aung]")
    print(f"{cyan}[Telegram]  {purple} :[@nkka404]")
    print(f"{cyan}[Channel]   {purple} :[t.me/premium_channel_404]\n")
    ret=input(ask+"1 for main menu, 0 for exit  > "+green)
    if ret=="1":
        main()
    else: 
        exit()

# Custom path chooser
def mover(out_file):
    move= input(ask+"Move to a custom path?(y/n) > "+green)
    if move=="y":
        mpath=input(ask+"Enter the path > "+ green)
        if os.path.exists(mpath):
            os.system(f'''mv -f "{out_file}" "{mpath}" ''')
            sprint(f"{success}{out_file} moved to {mpath}\n")
        else:
            sprint(error+"Path do not exist!\n")
    else:
        print("\n")
    exit()

# Base64 encoder function
def obfuscate(VARIABLE_NAME, file_content):
    b64_content = base64.b64encode(file_content.encode()).decode()
    index = 0
    code = f'{VARIABLE_NAME} = ""\n'
    for _ in range(int(len(b64_content) / OFFSET) + 1):
        _str = ''
        for char in b64_content[index:index + OFFSET]:
            byte = str(hex(ord(char)))[2:]
            if len(byte) < 2:
                byte = '0' + byte
            _str += '\\x' + str(byte)
        code += f'{VARIABLE_NAME} += "{_str}"\n'
        index += OFFSET
    code += f'exec(__import__("\\x62\\x61\\x73\\x65\\x36\\x34").b64decode({VARIABLE_NAME}.encode("\\x75\\x74\\x66\\x2d\\x38")).decode("\\x75\\x74\\x66\\x2d\\x38"))'
    return code

def chunk_string(in_s, n):
    return "\n".join(
        "{}\\".format(in_s[i : i + n]) for i in range(0, len(in_s), n)
    ).rstrip("\\")

def encode_string(in_s, alphabet):
    d1 = dict(enumerate(alphabet))
    d2 = {v: k for k, v in d1.items()}
    return (
        'exec("".join(map(chr,[int("".join(str({}[i]) for i in x.split())) for x in\n'
        '"{}"\n.split("  ")]))))\n'.format(
            pformat(d2),
            chunk_string(
                "  ".join(" ".join(d1[int(i)] for i in str(ord(c))) for c in in_s),
                MAX_STR_LEN,
            ),
        )
    )

# Encrypt Bash
def encryptsh():
    in_file = input(ask + "Input Filename  > "+cyan)
    if not os.path.exists(in_file):
        sprint(error+'File not found')
        os.system("sleep 2")
        encryptsh()
    
    os.system("bash-obfuscate " + in_file + " -o .temp")
    if not os.path.exists(".temp"):
        try:
            sprint(info+"Installing Bash-Obfuscate....\n")
            os.system("apt install nodejs -y && npm install -g bash-obfuscate")
            os.system("bash-obfuscate " + in_file + " -o .temp")
        except:
            sprint(error+" Bash-Obfuscate installation failed!")
            exit(1)
            
    out_file= input(ask + "Output Filename  > " + green)   
    with open(".temp",'r') as temp_f, open(out_file,'w') as out_f:
        filedata = temp_f.read()
        out_f.write("# Encrypted by 404 SMART TOOL\n# Developer: @nkka404\n\n"+filedata)
    os.remove(".temp")
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Decrypt bash
def decryptsh():
    in_file = input(ask + "Input File  > "+cyan)
    if not os.path.exists(in_file):
        print(error+' File not found')
        os.system("sleep 2")
        decryptsh()
    with open(in_file,'r') as in_f, open(".temp1",'w') as temp_f:
        filedata = in_f.read()
        if not (filedata.find("eval") != -1):
            sprint(error+" Cannot be decrypted!")
            exit()
        newdata = filedata.replace("eval","echo")
        temp_f.write(newdata)
    out_file = input(ask + "Output File  > " +green)
    os.system("bash .temp1 > .temp2")
    os.remove(".temp1")
    with open(".temp2",'r') as temp_f2, open(out_file,'w') as out_f:
        filedata = temp_f2.read()
        out_f.write("# Decrypted by 404 SMART TOOL\n\n"+filedata)
    os.remove(".temp2")
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Python to Variable
def encryptvar():
    var= input(ask + "Variable to be used  > " + green)
    if (var=="") or (var.find(" ")!= -1):
        sprint(error + " Invalid variable name!")
        encryptvar()
    
    iteration = input(ask + "Iteration count (Default 50)  > " + green)
    try:
        iteration = int(iteration)
    except:
        iteration = 50
        
    VARIABLE_NAME = var * iteration
    in_file = input(ask+ "Input file  > "+cyan)
    if not os.path.isfile(in_file):
        print(error+' File not found')
        encryptvar()
        
    out_file = input(ask + "Output file  > " + green)
    with open(in_file, 'r', encoding='utf-8', errors='ignore') as in_f, open(out_file, 'w') as out_f:
       file_content = in_f.read()
       obfuscated_content = obfuscate(VARIABLE_NAME, file_content)
       out_f.write("# Encrypted by 404 SMART TOOL\n# Developer: @nkka404\n\n"+obfuscated_content)
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Python to Emoji
def encryptem():
    in_file= input(ask +"Input File  > "+cyan )
    if not os.path.isfile(in_file):
        print(error+' File not found')
        encryptem()
    out_file= input(ask + "Output File  > " + green)
    with open(in_file) as in_f, open(out_file, "w", encoding="utf-8") as out_f:
        out_f.write("# Encrypted by 404 SMART TOOL\n# Developer: @nkka404\n\n")
        out_f.write(encode_string(in_f.read(), alphabet))
    sprint(f"{success}{out_file} saved in {pwd}")
    mover(out_file)

# Main menu
def main():
    os.system("clear")
    print(logo)
    print(f"{green}[1]{yellow} Encrypt{cyan} Bash")
    print(f"{green}[2]{yellow} Decrypt{cyan} Bash")
    print(f"{green}[3]{yellow} Encrypt{cyan} Python (Variable)")
    print(f"{green}[4]{yellow} Encrypt{cyan} Python (Emoji)")
    print(f"{green}[5]{yellow} About")
    print(f"{green}[0]{yellow} Exit")
    
    choose = input(f"{ask}{blue}Choose an option : {cyan}")
    
    if choose == "1":
        encryptsh()
    elif choose == "2":
        decryptsh()
    elif choose == "3":
        encryptvar()
    elif choose == "4":
        encryptem()
    elif choose == "5":
        about()
    elif choose == "0":
        exit()
    else:
        sprint(error+'Wrong input!')
        time.sleep(1)
        main()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sprint(info+"Exiting... Good day!")
        exit()
    except Exception as e:
        sprint(error+str(e))
