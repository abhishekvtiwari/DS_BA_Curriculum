"""Author tool: runs each python block in order (as verify_python.py does) and writes the real output
into the plain block that follows it. Used once while drafting; verify_python.py then re-checks."""
import re, sys, io, os, contextlib, traceback
path, cwd = os.path.abspath(sys.argv[1]), sys.argv[2]
md = open(path, encoding='utf-8').read()
pat = re.compile(r'(```python\n(.*?)^```\n\n```\n)(.*?)(^```$)', re.S | re.M)
os.chdir(cwd); ns = {'__name__': '__main__'}; out=[]; pos=0
for m in pat.finditer(md):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try: exec(m.group(2), ns)
        except Exception: print(traceback.format_exc().strip().splitlines()[-1])
    out.append(md[pos:m.start(3)]); out.append(buf.getvalue()); pos = m.start(4)
out.append(md[pos:]); open(path, 'w', encoding='utf-8').write(''.join(out))
print('filled', len(re.findall(pat, md)))
