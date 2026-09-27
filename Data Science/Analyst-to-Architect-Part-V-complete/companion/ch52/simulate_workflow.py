"""Chapter 52 companion: simulate which GitHub Actions jobs run for a given event,
by reading the real workflow YAML and applying its 'on' and 'if' rules in Python.
This is not GitHub's own engine, but the logic (trigger matching, needs, if conditions
on github.event_name and github.ref) is the same, and it's checkable without a repository.
Riverstone Supplies is fictional; every name and number is invented."""
import yaml

def load_workflow(path):
    return yaml.safe_load(open(path))

def matches_trigger(workflow, event_name, branch):
    on = workflow.get(True) or workflow.get("on")   # PyYAML can parse bare 'on:' as boolean True
    if isinstance(on, str):
        on = {on: {}}
    if event_name not in on:
        return False
    rule = on[event_name] or {}
    branches = rule.get("branches")
    if branches and branch not in branches:
        return False
    return True

def eval_if(expr, context):
    """A tiny evaluator for the handful of expressions this workflow actually uses."""
    if expr is None:
        return True
    expr = expr.strip()
    parts = [p.strip() for p in expr.split("&&")]
    for part in parts:
        if part.startswith("github.event_name =="):
            want = part.split("==")[1].strip().strip("'")
            if context["event_name"] != want:
                return False
        elif part.startswith("github.ref =="):
            want = part.split("==")[1].strip().strip("'")
            if context["ref"] != want:
                return False
        else:
            raise ValueError(f"unhandled expression: {part}")
    return True

def jobs_that_run(workflow, event_name, branch):
    context = {"event_name": event_name, "ref": f"refs/heads/{branch}"}
    if not matches_trigger(workflow, event_name, branch):
        return []
    jobs = workflow["jobs"]
    would_run = {}
    for name, job in jobs.items():
        needs = job.get("needs")
        needs = [needs] if isinstance(needs, str) else (needs or [])
        needs_ok = all(would_run.get(n, False) for n in needs)
        this_ok = needs_ok and eval_if(job.get("if"), context)
        would_run[name] = this_ok
    return [name for name, runs in would_run.items() if runs]

if __name__ == "__main__":
    wf = load_workflow(".github_workflows/deploy.yml")
    cases = [
        ("pull_request", "main", "a pull request targeting main"),
        ("push", "main", "a direct push to main"),
        ("push", "develop", "a push to a branch other than main"),
    ]
    for event, branch, description in cases:
        print(f"{description:<38} -> {jobs_that_run(wf, event, branch)}")
