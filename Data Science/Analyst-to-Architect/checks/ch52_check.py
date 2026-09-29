# Analyst to Architect - Chapter 52 checks. Run from the book root:
#   python3 checks/ch52_check.py
# Needs pyyaml, python-hcl2 and dockerfile-parse (section 52.0). No Docker, Kubernetes, Terraform or cloud
# account: this re-checks the chapter's files and arithmetic. The real Docker and Terraform runs are recorded
# in changelog/ch52.md. Riverstone Supplies is fictional; every name and number is invented.
import os, sys, ipaddress
os.chdir('companion/ch52'); sys.path.insert(0, '.')
import yaml, hcl2
from dockerfile_parse import DockerfileParser
from simulate_workflow import load_workflow, jobs_that_run

ok = True
def check(label, got, exp):
    global ok
    good = (got == exp); ok &= good
    print(('OK  ' if good else 'FAIL'), label, got, '' if good else f'(expected {exp})')

# Dockerfile
d = DockerfileParser("pipeline_image")
check('base image', d.baseimage, 'python:3.14-slim')
check('layers (RUN/COPY/ADD)', sum(1 for s in d.structure if s['instruction'] in ('RUN', 'COPY', 'ADD')), 5)
check('runs as non-root user', [s['value'] for s in d.structure if s['instruction'] == 'USER'], ['pipeline'])
check('no apt-get (psycopg2-binary)', any('apt-get' in s['value'] for s in d.structure), False)
check('.dockerignore keeps .env out', '.env' in open('pipeline_image/.dockerignore').read().split(), True)
for f in ['ingest.py', 'riverstone_pipeline.py']:
    check(f'{f} same as Chapter 46', open(f'pipeline_image/{f}').read() == open(f'../ch46/{f}').read(), True)

# docker-compose
with open("pipeline_image/docker-compose.yml") as f:
    compose = yaml.safe_load(f)
check('compose services', sorted(compose['services']), ['pipeline', 'postgres'])
check('pipeline waits for healthy db', compose['services']['pipeline']['depends_on'], {'postgres': {'condition': 'service_healthy'}})
check('db name created', compose['services']['postgres']['environment']['POSTGRES_DB'], 'riverstone_source')

# Kubernetes
with open("k8s/pipeline-cronjob.yaml") as f:
    cron = yaml.safe_load(f)
check('cronjob schedule', (cron['spec']['schedule'], cron['spec']['timeZone']), ('30 6 * * *', 'Asia/Kolkata'))
container = cron['spec']['jobTemplate']['spec']['template']['spec']['containers'][0]
check('cpu request/limit', (container['resources']['requests']['cpu'], container['resources']['limits']['cpu']), ('250m', '1'))
with open("k8s/flash-page.yaml") as f:
    dep, svc = yaml.safe_load_all(f)
check('labels match', dep['spec']['selector']['matchLabels'] == dep['spec']['template']['metadata']['labels'] == svc['spec']['selector'], True)

# Terraform
with open("terraform/main.tf") as f:
    cfg = hcl2.load(f)
check('terraform resources', [list(r.keys())[0].strip('"') for r in cfg['resource']],
      ['aws_s3_bucket', 'aws_s3_bucket_versioning', 'aws_s3_bucket_lifecycle_configuration', 'aws_iam_role', 'aws_iam_role_policy'])

# Networking arithmetic
vpc = ipaddress.ip_network("10.0.0.0/16")
check('VPC total addresses', vpc.num_addresses, 2 ** 16)
subnets = list(vpc.subnets(new_prefix=24))
check('/24 subnets from a /16', len(subnets), 256)
check('usable per /24 (AWS)', subnets[0].num_addresses - 5, 251)
check('Ex 4: usable per /26 (AWS)', ipaddress.ip_network("10.0.0.0/26").num_addresses - 5, 59)
check('/26 subnets from a /16', len(list(vpc.subnets(new_prefix=26))), 1024)

# Cost (AWS price list, Mumbai, checked 29 Sep 2026)
price = 0.5 * 0.04256 + 1 * 0.004655
check('price per hour', round(price, 4), 0.0259)
check('always on', round(price * 730, 2), 18.93)
check('scheduled', round(price * 30, 2), 0.78)
check('ratio', round(730 / 30, 1), 24.3)
check('storage 277 GB', round(277 * 0.025, 2), 6.93)
check('total', round(277 * 0.025 + price * 30, 2), 7.70)
check('EKS job', round(73 + price * 30 + 277 * 0.025, 2), 80.70)
check('EKS 2 always on', round(73 + 2 * price * 730 + 277 * 0.025, 2), 117.79)
check('Ex 8', (round(0.05 * 730, 2), round(0.05 * 60, 2), round(730 / 60, 1)), (36.5, 3.0, 12.2))

# Workflow trigger simulation
wf = load_workflow(".github/workflows/deploy.yml")
check('PR targeting main', jobs_that_run(wf, 'pull_request', 'main'), ['test'])
check('push to main', jobs_that_run(wf, 'push', 'main'), ['test', 'build-and-push', 'deploy'])
check('push to develop', jobs_that_run(wf, 'push', 'develop'), [])
check('PR targeting develop (Ex 5)', jobs_that_run(wf, 'pull_request', 'develop'), [])

print('ALL CHECKS PASSED' if ok else 'SOME CHECKS FAILED')
