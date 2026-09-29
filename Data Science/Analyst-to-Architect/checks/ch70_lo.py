"""ch70_lo.py - check Chapter 70's formula answers and VBA macros in LibreOffice (headless).

Opens a copy of companion/ch70/ch70_practice.xlsx, types each formula the chapter quotes into a spare
cell of the Orders sheet, recalculates and prints the result. Then inserts the chapter's VBA
procedures (the ```vb blocks, BROKEN one excluded: it never ends) in VBA-compatibility mode
(Option VBASupport 1), runs them and prints Debug.Print output and column K.
LibreOffice 24.2 has no XLOOKUP, FILTER or UNIQUE: checks/ch70_check.py evaluates those.
Usage (from the book folder):  python3 checks/ch70_lo.py
"""
import os, re, shutil, subprocess, sys, tempfile, time
import uno
from com.sun.star.beans import PropertyValue

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS = BOOK + '/manuscript/ch70-excel-google-sheets-vba-and-bi-question-bank.md'
HERE = tempfile.mkdtemp(prefix='ch70_lo_')

FORMULAS = [
    ('Q70-001 SUMIFS', '=SUMIFS(I2:I7, C2:C7, "Sharma Hardware", F2:F7, ">=20", J2:J7, "<>Cancelled")'),
    ('Q70-001 without status', '=SUMIFS(I2:I7, C2:C7, "Sharma Hardware", F2:F7, ">=20")'),
    ('Q70-002 INDEX/MATCH', '=INDEX(G2:G7, MATCH("Storage Box 25L", E2:E7, 0))'),
    ('Q70-002 MATCH position', '=MATCH("Storage Box 25L", E2:E7, 0)'),
    ('Q70-002 VLOOKUP', '=VLOOKUP("Storage Box 25L", E2:G7, 3, FALSE)'),
    ('Q70-005 SUMPRODUCT', '=SUMPRODUCT(F2:F7, G2:G7, 1-H2:H7/100)'),
    ('Q70-005 SUM(I)', '=SUM(I2:I7)'),
    ('Q70-005 SUMPRODUCT excl', '=SUMPRODUCT(F2:F7 * G2:G7 * (1-H2:H7/100) * (J2:J7<>"Cancelled"))'),
    ('Q70-005 SUMIFS excl', '=SUMIFS(I2:I7, J2:J7, "<>Cancelled")'),
    ('Q70-010 TEXT', '=TEXT(B2, "MMMM")'),
    ('Q70-026 MAXIFS-MINIFS', '=MAXIFS(B2:B7, C2:C7, "Sharma Hardware") - MINIFS(B2:B7, C2:C7, "Sharma Hardware")'),
    ('Q70-006 COUNT/COUNTA', '=COUNT(I2:I7)&" / "&COUNTA(J2:J7)&" / "&COUNTBLANK(K2:K7)'),
]
TIERS = '=IF(I{r}>20000, "Large", IF(I{r}>5000, "Medium", "Small"))'
BROKEN = '=IF(I{r}>5000, "Medium", IF(I{r}>20000, "Large", "Small"))'


def lo(f):
    """LibreOffice's API wants ';' between arguments; commas inside quotes stay."""
    return re.sub(r'("[^"]*")|,', lambda m: m.group(1) or ';', f)


def pv(n, v):
    p = PropertyValue(); p.Name = n; p.Value = v; return p


md = open(MS, encoding='utf-8').read()
blocks = [b for b in re.findall(r'^```vb\n(.*?)^```$', md, re.S | re.M) if 'BROKEN' not in b]
procs = {}
for b in blocks:
    for m in re.finditer(r'^(Sub (\w+).*?^End Sub)', b, re.S | re.M):
        procs[m.group(2)] = m.group(1)
code = "Option VBASupport 1\nPublic LOG As String\nSub DP(s)\n  LOG = LOG & s & Chr(10)\nEnd Sub\n" + "\n".join(procs.values())
code = re.sub(r'\bDebug\.Print ', 'DP ', code)
code += "\nFunction RunIt(n As String) As String\n  LOG = \"\"\n  If n = \"ShowLastRow\" Then ShowLastRow\n  If n = \"MarkLargeOrders\" Then MarkLargeOrders\n  RunIt = LOG\nEnd Function\n"

xl = os.path.join(HERE, 'ch70_practice.xlsx')
shutil.copy(BOOK + '/companion/ch70/ch70_practice.xlsx', xl)
prof = 'file://' + os.path.join(HERE, 'lo_profile')
proc = subprocess.Popen(['soffice', '-env:UserInstallation=' + prof, '--headless', '--invisible', '--norestore',
                         '--accept=socket,host=localhost,port=2370;urp;'], stderr=subprocess.DEVNULL)
ctx = None
for _ in range(120):
    try:
        local = uno.getComponentContext()
        res = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        ctx = res.resolve("uno:socket,host=localhost,port=2370;urp;StarOffice.ComponentContext"); break
    except Exception:
        time.sleep(0.5)
desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(xl), "_blank", 0,
                                   (pv("Hidden", False), pv("MacroExecutionMode", 4)))
sh = doc.Sheets.getByName('Orders')
row = 20
for label, f in FORMULAS:
    c = sh.getCellRangeByName(f'N{row}'); c.setFormula(lo(f)); row += 1
for r in range(2, 8):
    sh.getCellRangeByName(f'L{r}').setFormula(lo(TIERS.format(r=r)))
    sh.getCellRangeByName(f'M{r}').setFormula(lo(BROKEN.format(r=r)))
doc.calculateAll()
row = 20
for label, f in FORMULAS:
    c = sh.getCellRangeByName(f'N{row}')
    print(f'{label:26} {f}  -> {c.getString()}'); row += 1
print('Q70-004 tiers (L2:L7)      ', [sh.getCellRangeByName(f'L{r}').getString() for r in range(2, 8)])
print('Q70-004 broken (M2:M7)     ', [sh.getCellRangeByName(f'M{r}').getString() for r in range(2, 8)])
for r in range(2, 8):
    sh.getCellRangeByName(f'L{r}').setString(''); sh.getCellRangeByName(f'M{r}').setString('')
for r in range(20, row):
    sh.getCellRangeByName(f'N{r}').setString('')

libs = doc.BasicLibraries
lib = libs.getByName("Standard") if libs.hasByName("Standard") else libs.createLibrary("Standard")
lib.insertByName("Module1", code)
sp = doc.getScriptProvider()
s = sp.getScript("vnd.sun.star.script:Standard.Module1.RunIt?language=Basic&location=document")
for name in ('ShowLastRow', 'MarkLargeOrders'):
    try:
        out = s.invoke((name,), (), ())[0]
    except Exception as e:
        out = f'ERR {e}'
    print(f'==== VBA {name}\n{out}', end='')
print('column K after MarkLargeOrders:', [sh.getCellRangeByName(f'K{r}').getString() for r in range(2, 8)])
doc.close(True)
try:
    desktop.terminate()
except Exception:
    pass
proc.wait(timeout=30)
