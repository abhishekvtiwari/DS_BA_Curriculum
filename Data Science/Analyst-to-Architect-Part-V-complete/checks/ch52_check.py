# Analyst to Architect - Chapter 52 checks. Run from the book root:
#   PYTHONPATH=companion/ch52 python3 checks/ch52_check.py
# No PostgreSQL, Docker, Kubernetes, Terraform, or cloud account needed: everything here is
# local parsing and arithmetic. Riverstone Supplies is fictional; every name and number is invented.
import os, sys
os.chdir('companion/ch52'); sys.path.insert(0, '.')
import yaml, hcl2
from dockerfile_parse import DockerfileParser
import ipaddress
from networking_math import describe
from cost_estimate import container_compute_cost, always_on_vs_scheduled, HOURS_PER_MONTH
from simulate_workflow import load_workflow, jobs_that_run

ok = True
def check(label, got, exp):
    global ok
    good = (got == exp); ok &= good
    print(('OK  ' if good else 'FAIL'), label, got, '' if good else f'(expected {exp})')

# Dockerfile
d = DockerfileParser(fileobj=open("pipeline_image/Dockerfile", "rb"))
check('base image', d.baseimage, 'python:3.12-slim')
check('layers (RUN/COPY/ADD)', sum(1 for s in d.structure if s['instruction'] in ('RUN', 'COPY', 'ADD')), 6)
check('runs as non-root user', [s['value'] for s in d.structure if s['instruction'] == 'USER'], ['pipeline'])

# docker-compose
compose = yaml.safe_load(open("pipeline_image/docker-compose.yml"))
check('compose services', sorted(compose['services'].keys()), ['pipeline', 'postgres'])
check('pipeline depends on postgres', compose['services']['pipeline']['depends_on'], ['postgres'])

# Kubernetes
docs = list(yaml.safe_load_all(open("k8s/pipeline-deployment.yaml")))
check('k8s documents', [d['kind'] for d in docs], ['Deployment', 'Service'])
check('replicas', docs[0]['spec']['replicas'], 2)
container = docs[0]['spec']['template']['spec']['containers'][0]
check('cpu request', container['resources']['requests']['cpu'], '250m')
check('cpu limit', container['resources']['limits']['cpu'], '1')
check('secrets referenced', sorted(e['valueFrom']['secretKeyRef']['name'] for e in container['env']),
      ['riverstone-crm-secret', 'riverstone-db-secret'])

# Terraform
with open("terraform/main.tf") as f:
    cfg = hcl2.load(f)
resource_types = sorted(list(r.keys())[0].strip('"') for r in cfg['resource'])
check('terraform resource count', len(resource_types), 5)
check('s3 bucket declared', 'aws_s3_bucket' in resource_types, True)
check('iam role declared', 'aws_iam_role' in resource_types, True)

# Networking arithmetic
vpc = ipaddress.ip_network("10.0.0.0/16")
check('VPC total addresses', vpc.num_addresses, 65536)
subnets = list(vpc.subnets(new_prefix=24))
check('/24 subnets from a /16', len(subnets), 256)
check('usable hosts per /24', describe(str(subnets[0]))['usable_hosts'], 251)
check('exercise 2: /16 subnets', ipaddress.ip_network("10.20.0.0/16").num_addresses, 65536)

# Cost
always_on, scheduled = always_on_vs_scheduled()
check('always-on monthly cost', always_on, 17.52)
check('scheduled monthly cost', scheduled, 0.72)
check('cost ratio (Ex 8)', round(always_on / scheduled, 1), 24.3)
check('storage + compute total', round(round(277 * 0.023, 2) + scheduled, 2), 7.09)

# Workflow trigger simulation
wf = load_workflow(".github_workflows/deploy.yml")
check('PR targeting main', jobs_that_run(wf, 'pull_request', 'main'), ['test'])
check('push to main', sorted(jobs_that_run(wf, 'push', 'main')), sorted(['test', 'build-and-push', 'deploy']))
check('push to develop (Ex 5)', jobs_that_run(wf, 'push', 'develop'), [])
check('PR targeting develop (Ex 5)', jobs_that_run(wf, 'pull_request', 'develop'), [])

print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
