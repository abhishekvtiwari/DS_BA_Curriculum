"""Chapter 52 companion: work out which GitHub Actions jobs start for a given event,
by reading the real workflow YAML and applying its 'on', 'needs' and 'if' rules in Python.
It is not GitHub's own engine: it handles branch filters, needs, and 'if' tests on
github.event_name and github.ref joined by &&, and nothing else (no path filters, tags,
manual runs, schedules, or failing jobs).
Riverstone Supplies is fictional; every name and number is invented."""
import yaml

def load_workflow(path):
    with open(path) as f:
        return yaml.safe_load(f)

def matches_trigger(workflow, event_name, branch):
    on = workflow.get(True) or workflow.get("on")   # PyYAML can read a bare 'on:' as True
    if event_name not in on:
        return False
    branches = (on[event_name] or {}).get("branches")
    return not branches or branch in branches

def eval_if(expr, context):
    """A tiny evaluator for the two tests this workflow uses, joined by &&."""
    if expr is None:
        return True
    for part in (p.strip() for p in expr.split("&&")):
        name, _, want = (x.strip() for x in part.partition("=="))
        want = want.strip("'")
        if name == "github.event_name":
            if context["event_name"] != want:
                return False
        elif name == "github.ref":
            if context["ref"] != want:
                return False
        else:
            raise ValueError(f"unhandled expression: {part}")
    return True

def jobs_that_run(workflow, event_name, branch):
    context = {"event_name": event_name, "ref": f"refs/heads/{branch}"}
    if not matches_trigger(workflow, event_name, branch):
        return []
    would_run = {}
    for name, job in workflow["jobs"].items():
        needs = job.get("needs")
        needs = [needs] if isinstance(needs, str) else (needs or [])
        would_run[name] = all(would_run.get(n) for n in needs) and eval_if(job.get("if"), context)
    return [name for name, runs in would_run.items() if runs]

if __name__ == "__main__":
    wf = load_workflow(".github/workflows/deploy.yml")
    for event, branch in [("pull_request", "main"), ("push", "main"), ("push", "develop"), ("pull_request", "develop")]:
        print(f"{event} to {branch}: {jobs_that_run(wf, event, branch)}")
