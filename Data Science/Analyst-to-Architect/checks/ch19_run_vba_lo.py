"""ch19_run_vba_lo.py - run chapter 19 VBA procedures in LibreOffice's VBA-compatibility mode (Option VBASupport 1)
against a copy of companion/ch19/ch19_practice.xlsx, capturing Debug.Print output.
Usage (from the book folder):
  python3 checks/ch19_run_vba_lo.py VariableDemo TestCheckTarget TestBandBySize LoopDemo ArrayDemo UseIt ByRefDemo \
      ObjectBasics RangeToolkit TestRebate SayHello
  SRC=/path/to/copy/of/branch_files/ python3 checks/ch19_run_vba_lo.py ConsolidateBranchFiles
Each TARGET is a statement run inside a wrapper (a Sub name, or a call with arguments).
LibreOffice's VBA mode has no Scripting.Dictionary, so CleanMaster, CleanStatusFast and the dictionary
half of ArrayDemo can't run here; Outlook, pivot and PDF procedures are Excel-only. Debug.Print output
is captured; MsgBox text is printed as [MsgBox] ...."""
import subprocess, time, uno, sys, os, re, shutil
from com.sun.star.beans import PropertyValue
import tempfile
HERE=tempfile.mkdtemp(prefix='ch19_lo_')
BOOK=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS=BOOK+'/manuscript/ch19-spreadsheet-automation.md'
def pv(n,v):
    p=PropertyValue(); p.Name=n; p.Value=v; return p
md=open(MS,encoding='utf-8').read()
blocks=re.findall(r'^```vb\n(.*?)^```$',md,re.S|re.M)
procs={}
for b in blocks:
    for m in re.finditer(r'^((?:Public |Private )?(?:Sub|Function) (\w+).*?^End (?:Sub|Function))',b,re.S|re.M):
        procs[m.group(2)]=m.group(1)
consts="\n".join(sorted(set(re.findall(r'^Private Const .*$',"\n".join(blocks),re.M))))
if os.environ.get("SRC"): consts=consts.replace("C:\\Riverstone\\branch_files\\", os.environ["SRC"])
def module(targets, needed):
    body=[procs[n] for n in needed]
    code="Option VBASupport 1\nOption Explicit\nPublic LOG As String\n"+consts+"\nSub DP(s)\n  LOG = LOG & s & Chr(10)\nEnd Sub\n"
    code+="\n".join(body)
    for i,t in enumerate(targets):
        code+=f"\nFunction Run_{i}() As String\n  LOG = \"\"\n  On Error GoTo Bad\n  {t}\n  Run_{i} = LOG\n  Exit Function\nBad:\n  Run_{i} = LOG & \"[ERROR \" & Err.Number & \": \" & Err.Description & \" (\" & Err.Source & \") line \" & Erl & \"]\" & Chr(10)\nEnd Function\n"
    code=re.sub(r'\bDebug\.Print ', 'DP ', code)
    code=re.sub(r'\bMsgBox ', 'DP "[MsgBox] " & ', code)
    return code
targets=sys.argv[1:]
needed=[n for n in procs if n not in ('Format_Sales_Sheet',)]
work=os.path.join(HERE,'lo_run'); os.makedirs(work,exist_ok=True)
xl=os.path.join(work,'ch19_practice.xlsx'); shutil.copy(BOOK+'/companion/ch19/ch19_practice.xlsx',xl)
prof='file://'+os.path.join(HERE,'lo_profile')
proc=subprocess.Popen(['soffice','-env:UserInstallation='+prof,'--headless','--invisible','--norestore','--accept=socket,host=localhost,port=2319;urp;'],stderr=subprocess.DEVNULL)
ctx=None
for i in range(120):
    try:
        local=uno.getComponentContext()
        res=local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver",local)
        ctx=res.resolve("uno:socket,host=localhost,port=2319;urp;StarOffice.ComponentContext"); break
    except Exception: time.sleep(0.5)
desktop=ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop",ctx)
doc=desktop.loadComponentFromURL(uno.systemPathToFileUrl(xl),"_blank",0,(pv("Hidden",False),pv("MacroExecutionMode",4)))
libs=doc.BasicLibraries
lib=libs.getByName("Standard") if libs.hasByName("Standard") else libs.createLibrary("Standard")
code=module(targets,needed)
open(os.path.join(work,'module.bas'),'w').write(code)
lib.insertByName("Module1",code)
sp=doc.getScriptProvider()
for i,t in enumerate(targets):
    s=sp.getScript(f"vnd.sun.star.script:Standard.Module1.Run_{i}?language=Basic&location=document")
    try:
        r=s.invoke((),(),())
        print(f"==== {t}\n{r[0]}",end='')
    except Exception as e:
        print(f"==== {t}\nERR {e}")
doc.close(True)
try: desktop.terminate()
except Exception: pass
proc.wait(timeout=30)
