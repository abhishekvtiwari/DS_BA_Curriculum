#!/usr/bin/env python3
"""ch55_code_sync.py - keeps Chapter 55's printed code and its companion modules in step.

Usage: python3 checks/ch55_code_sync.py [manuscript/ch55-building-ai-applications.md] [companion/ch55]

Every function or class the chapter defines or prints (in ```python blocks, run or not) that also exists in
retrieval.py, assistant.py or tools.py must have the same code (compared as syntax trees, so comments and
blank lines don't matter). Methods printed on their own (an indented `def`) are compared with the class's
method of the same name. Exit code 0 when everything matches.
"""
import ast, pathlib, re, sys, textwrap

BOOK = pathlib.Path(__file__).resolve().parent.parent
md_path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK / 'manuscript/ch55-building-ai-applications.md'
companion = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else BOOK / 'companion/ch55'


def definitions(tree):
    found = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found[node.name] = node
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        found[f'{node.name}.{item.name}'] = item
    return found


modules = {}
for name in ('retrieval', 'assistant', 'tools'):
    for key, node in definitions(ast.parse((companion / f'{name}.py').read_text(encoding='utf-8'))).items():
        modules[key] = (name, node)

md = md_path.read_text(encoding='utf-8')
checked = bad = 0
for block in re.findall(r'^```python\n(.*?)^```$', md, re.S | re.M):
    source = textwrap.dedent(block)
    tree = ast.parse(source)
    chapter_defs = definitions(tree)
    if block.startswith('    def '):            # a method printed on its own
        chapter_defs = {f'SupportAssistant.{k}': v for k, v in chapter_defs.items()}
    for key, node in chapter_defs.items():
        if key == 'load_documents' or key not in modules:
            continue                            # load_documents differs only in its default folder
        module_name, module_node = modules[key]
        if isinstance(node, ast.ClassDef):
            printed = [i.name for i in node.body if isinstance(i, ast.FunctionDef)]
            for method in printed:
                checked += 1
                if ast.dump(definitions(ast.Module(body=[node], type_ignores=[]))[f'{key}.{method}']) != \
                        ast.dump(modules[f'{key}.{method}'][1]):
                    bad += 1
                    print(f'DIFFERS: {key}.{method} (chapter vs {module_name}.py)')
            continue
        checked += 1
        if ast.dump(node) != ast.dump(module_node):
            bad += 1
            print(f'DIFFERS: {key} (chapter vs {module_name}.py)')

print(f'{md_path.name}: {checked} definitions compared with the companion modules, {bad} different')
sys.exit(1 if bad else 0)
