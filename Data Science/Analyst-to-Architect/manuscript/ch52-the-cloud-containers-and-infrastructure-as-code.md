# Chapter 52. The Cloud, Containers & Infrastructure as Code

*Part 5 — Data Engineering, Integration & Scale*

> **Chapter at a glance**
>
> **You will learn to:** say what IaaS, PaaS, and SaaS rent you, and where the shared responsibility line falls for each · explain regions and availability zones · write a least-privilege access policy and read every field of it · plan a network with CIDR arithmetic you can do by hand · install Docker, build an image of Chapter 46's pipeline, and run it · run a small stack of containers with Docker Compose · read a Kubernetes CronJob, Deployment, and Service and say what each line does · write a small Terraform configuration, check it, and read its plan · build a CI/CD workflow and trace exactly which jobs run for a given event · keep secrets out of code and images · estimate what running a pipeline in the cloud actually costs · choose a deployment target that fits a company Riverstone's size.
>
> **Before you start:** Chapter 26 (the terminal, Git, pull requests, `.gitignore` and `.env`, GitHub Actions). Chapter 29 (tests with pytest). Chapter 34 (environment variables, IP addresses, ports, private address ranges, and WSL on Windows). Chapter 45 (the practice source and CRM API), Chapter 46 (the pipeline this chapter deploys), Chapter 47 (checks and incidents), Chapter 49 (storage and its cost), Chapter 51 (webhooks).
>
> **Time needed:** 20–26 hours of reading and practice, spread over three to four weeks. Docker (section 52.2) and Terraform (section 52.4) are hands-on and take the most time; read Kubernetes (section 52.3) for its vocabulary, and try it on your laptop only if you want to.
>
> **Tools:** Python 3.14 in the book's virtual environment, with `pyyaml`, `python-hcl2`, and `dockerfile-parse` (section 52.0); Docker (section 52.2); Terraform (section 52.4). No cloud account is needed.

> **A note on what actually runs in this chapter.** Everything that can run on a laptop runs for real, and its output is shown: the network arithmetic, a real Docker image of Chapter 46's pipeline, built and run until it delivers the 2 January Flash, a two-container Docker Compose stack, and Terraform's own checks and its plan. Some things need services a laptop doesn't have: a Kubernetes cluster, a cloud account, and a repository on GitHub with a cloud account behind it. Those files are still real and complete, and they're checked as far as a laptop allows: the Kubernetes files against Kubernetes' own rules, the workflow's trigger logic simulated in Python against the actual file. Faking the output of what wasn't run would be worse than saying so plainly, so anything that needs a cluster or a cloud account is marked **not executed**, in the same style Chapter 46 used for Airflow.

---

## Why this matters

Chapter 46 built a pipeline. Chapter 51 gave it something worth writing to. Right now, both of them exist only as files on your computer, running when you happen to type a command. Getting them to run reliably, on a schedule, reachable by the right people and nobody else, without your laptop being involved at all, is a different problem, and it's the one this chapter solves.

It's also where a great deal of a data engineer's actual working life happens. Job descriptions ask for "cloud experience" and "containers" more often than they ask for any single analytics tool, not because the cloud is more important than the data, but because nothing you've built in Part 5 runs anywhere real until it's deployed properly. This chapter takes Riverstone's pipeline from "works on my machine" to "works, reliably, on infrastructure someone else can also understand," using the same rigor the rest of this book has applied to data: nothing asserted that hasn't been checked.

---

## In plain English

Think about Riverstone opening a second warehouse in another city.

- **Cloud regions** are like choosing which city to build in: closer to your customers is faster, and rules differ by location.
- **The shared responsibility model** is like renting a unit in a business park: the landlord secures the building, the fence, and the road; you lock your own door and decide who gets a key.
- **Identity and access** is the list of who holds which keys: the delivery driver's key opens the loading bay, not the accounts office.
- **A container** is a warehouse's stock, packed identically every time, so it behaves the same wherever it's unloaded, rather than depending on what happens to already be in that particular building.
- **Kubernetes** is the logistics coordinator who decides which building gets which containers, replaces one that's damaged, and adds more when a big order comes in.
- **Infrastructure as Code** is a written building plan, not a verbal instruction to a contractor: anyone can read it, review it before it's built, and rebuild the exact same warehouse in a different city.
- **CI/CD** is the checklist that runs automatically before anything ships: inspected, tested, and only then loaded onto the truck.

---

## 52.0 Setting up

**Step 1. Your practice folder.** As in earlier chapters, copy the folder `companion/ch52` and paste it inside `work`, so you have `work/ch52`. It holds:

| File or folder | What it is | Section |
|---|---|---|
| `pipeline_image/` | Everything needed to build a container image of Chapter 46's pipeline: `Dockerfile`, `requirements.txt`, `.dockerignore`, `run_flash.py`, copies of `ingest.py` and `riverstone_pipeline.py` from Chapter 46, `docker-compose.yml`, and `.env.example` | 52.2 |
| `k8s/` | Two Kubernetes files: `pipeline-cronjob.yaml` and `flash-page.yaml` | 52.3 |
| `terraform/main.tf` | Storage and an identity for the pipeline, as code | 52.4 |
| `terraform_practice/main.tf` | A tiny configuration for practising reading a plan, with no cloud account | 52.4 |
| `.github/workflows/deploy.yml` | The CI/CD workflow | 52.5 |
| `simulate_workflow.py` | Works out which jobs of a workflow run for a given event | 52.5 |

`.github` and `.env.example` start with a dot, so your file browser may hide them. They're there; `ls -a` in a terminal shows them (Chapter 26, section 26.0).

**Step 2. Three small libraries.** Open a terminal, go into your practice folder, activate the book's virtual environment, and install the three parsers this chapter's checks use:

<!-- run: none -->
```
# terminal
$ cd work/ch52
$ source ../../.venv/bin/activate
$ python -m pip install pyyaml==6.0.3 python-hcl2==8.1.4 dockerfile-parse==2.0.1
```

- **`pyyaml`** reads YAML files, the format Docker Compose, Kubernetes, and GitHub Actions all use.
- **`python-hcl2`** reads HCL, the language Terraform files are written in (section 52.4).
- **`dockerfile-parse`** reads a Dockerfile (section 52.2) into Python lists and dictionaries.

On Windows PowerShell, activate with `..\..\.venv\Scripts\Activate.ps1`, as in Chapter 45. Add the three lines to your `requirements.txt`. Then create a notebook, `ch52.ipynb`, in `work/ch52`, choose the `.venv` kernel, and check the install in its first cell:

```python
import yaml, hcl2, dockerfile_parse
print("ok")
```

```
ok
```

`import yaml, hcl2, dockerfile_parse` loads the three libraries (each is imported under a slightly different name from the one you installed), and `print("ok")` runs only if all three loaded. If you see `ModuleNotFoundError` instead, the environment wasn't active when you installed: activate it and install again. Run every code block in this chapter as its own cell, top to bottom. Docker and Terraform are programs, not Python libraries; each is installed in the section that first uses it.

---

## 52.1 Cloud fundamentals

### What you rent: IaaS, PaaS, SaaS

Chapter 2 described the cloud in two sentences: computers, storage, and networks in someone else's data centre that you rent over the internet. The largest providers are Amazon Web Services (AWS), Microsoft Azure, and Google Cloud. Businesses rent at three levels, depending on how much they want to manage themselves:

| Level | You rent… | You still manage… | Examples | At Riverstone |
|---|---|---|---|---|
| **IaaS** (infrastructure as a service) | virtual computers, storage, and networks | the operating system, software, and data | a virtual server to run your own database | a virtual server (AWS calls it EC2) running the pipeline, which you patch and look after |
| **PaaS** (platform as a service) | a ready-to-use platform, such as a managed database | your data and how you use it | a cloud PostgreSQL service that handles backups and updates for you | a managed container service running the pipeline's container (section 52.8), or managed PostgreSQL (AWS calls it RDS) |
| **SaaS** (software as a service) | a finished application, used through a browser | your data and your settings | Gmail, Google Drive, Microsoft 365, CRM and accounting software | the CRM that Chapter 51 syncs to, and Gmail |

The further down the table, the less you manage. That moves the shared-responsibility line, later in this section.

**This chapter's examples use AWS**, the provider that appears most often in job listings. Every idea has an equivalent on the others, usually under a different name:

| What it is | AWS | Microsoft Azure | Google Cloud |
|---|---|---|---|
| Object storage (files, by name) | S3 | Blob Storage | Cloud Storage |
| Identity and access | IAM | Entra ID and role-based access control | Cloud IAM |
| Running containers without managing servers | ECS on Fargate | Container Apps | Cloud Run |
| Managed Kubernetes | EKS | AKS | GKE |
| A safe place for secrets | Secrets Manager | Key Vault | Secret Manager |

**S3** (Simple Storage Service) stores files, which AWS calls **objects**, in named containers called **buckets**. Chapter 49's sensor archive would live in one.

### Regions and availability zones

A **region** is a geographic area a cloud provider operates in (Mumbai, Singapore, Frankfurt). Each region contains multiple **availability zones**: physically separate data centers with independent power and networking, close enough for fast connections between them but far enough apart that one flooding or losing power doesn't take out the others.

Two decisions follow directly:

- **Choose a region near your users and your data's legal home.** Riverstone's customers, staff, and (per Chapter 45's note on data protection law) most of its personal data belong in an Indian region. AWS's Mumbai region is called `ap-south-1`; you'll see that name in section 52.4.
- **Spread anything that must stay up across at least two availability zones.** A pipeline running in one zone goes down when that zone has a bad afternoon; the same pipeline split across two zones usually doesn't.

### The shared responsibility model

Every major cloud provider splits security between itself and you. The provider secures the **cloud**: the physical data centers, the hardware, and the **virtualization layer** (the software that splits one physical server into many virtual machines, the kind of program Chapter 6 mentioned for running Windows on a Mac). You secure what you put **in** the cloud.

**The line moves with what you rent.** On IaaS you also patch the operating system; on PaaS the provider does; on SaaS you manage only your data, your users, and your settings. **What never moves:** your data, who can access it, and how you configure the service are always yours. A misconfigured storage bucket left open to the internet is never the provider's fault under this model, however it happened. Chapter 64 covers the governance side of this line in depth; this chapter is about not crossing it by accident.

![A grid with six layers down the left, from your data and who can access it at the top, through how you configure the service, application code, operating system and runtime, and the virtualization layer, to hardware and data centres at the bottom, and three columns, IaaS, PaaS and SaaS. Each cell says You or Provider. Under IaaS you manage the top four layers; under PaaS the top three; under SaaS only your data and your settings. A heavy line under each column marks where the split falls, lower for IaaS and higher for SaaS. A footer says the line moves with what you rent, but your data, who can access it, and how you configure the service are always yours.](figures/fig52-1-shared-responsibility.svg)

*Figure 52.1 — The provider draws the line differently for IaaS, PaaS, and SaaS, but data, access, and configuration are always the customer's.*

### Identity and access management (IAM)

**IAM** controls who, or what, can do what. Four words carry the whole idea:

- An **identity** is who is asking. It's either a **user** (a person with a login) or a **role**: an identity with no password that a program **assumes**, "puts on", to get **temporary credentials**, which expire on their own after a while, usually within an hour.
- A **policy** is a document that lists what an identity may do. AWS writes policies in JSON (Chapter 2).
- Each policy holds one or more **statements**, and each statement has three parts: an **Effect** (`Allow` or `Deny`), the **Actions** it covers, and the **Resources** they apply to.
- Every AWS resource has an **ARN** (Amazon Resource Name), its unique ID, such as `arn:aws:s3:::riverstone-sensor-archive-production` for a bucket.

The habit that matters most is **least privilege**: grant exactly the permissions a task needs, and no more, and prefer a role a pipeline assumes over a permanent password a person shares. For Riverstone's pipeline, that means a dedicated identity that can read and write the sensor archive's bucket and nothing else, not an administrator's full access borrowed for convenience. Here is that policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject", "s3:ListBucket"],
    "Resource": ["arn:aws:s3:::riverstone-sensor-archive-production",
                 "arn:aws:s3:::riverstone-sensor-archive-production/*"]
  }]
}
```

**Reading it, field by field.**

- **`"Version": "2012-10-17"`** is the version of AWS's policy language, not a date to keep up to date. Every current policy uses exactly this value.
- **`"Statement": [ ... ]`** is a list, in square brackets, even when it holds one statement.
- **`"Effect": "Allow"`** grants what follows. Anything not allowed is denied: AWS starts from "no".
- **`"Action"`** lists three things: read a file (`s3:GetObject`), write one (`s3:PutObject`), and list what's in the bucket (`s3:ListBucket`). Deleting (`s3:DeleteObject`) isn't there, so the pipeline can't delete anything.
- **`"Resource"`** names the bucket itself (listing applies to the bucket) and `/*`, every object inside it (reading and writing apply to objects).

Across the people and programs that touch the archive, least privilege looks like this:

| Who | Identity | May do |
|---|---|---|
| The pipeline | a role it assumes | `GetObject`, `PutObject`, `ListBucket` on this one bucket |
| An analyst | a user | `GetObject` and `ListBucket` on this bucket: read only |
| An administrator | a separate "break-glass" role, used only in an emergency and logged | everything, but nobody uses it day to day |

Section 52.4 creates the pipeline's role and this policy as code.

> **Watch out: "it's just for now" access outlives its reason.** Temporary broad permissions granted to unblock a deadline are one of the most common routes into cloud security incidents, because removing them is nobody's job once the deadline passes. Grant scoped access from the start; it costs a few extra minutes and no meetings six months later.

### Networking: VPCs, subnets, and security groups

A **VPC** (virtual private cloud) is your own isolated slice of the provider's network. Inside it, **subnets** divide the address space into smaller ranges, usually one **public** (reachable from the internet, for things like a **load balancer**: a front door that spreads incoming requests across several copies of a service) and one **private** (not directly reachable, for a pipeline and a database) per availability zone. A **security group** is a firewall attached to a resource, allowing only the specific traffic it needs.

Subnets are sized in **CIDR notation**: an address, a slash, and a number, such as `10.0.0.0/16`. This isn't a diagram to memorize; it's arithmetic you can check, first by hand.

> **CIDR by hand.** An IPv4 address (Chapter 34, section 34.9) is 32 bits (Chapter 2), written as four numbers from 0 to 255, such as `10.0.0.0`. The number after the slash says how many of those 32 bits are **fixed**: every address in the range starts with them. The rest are free.
>
> - `/16`: 16 bits fixed, 32 − 16 = 16 free, so 2¹⁶ = **65,536** addresses.
> - `/24`: 32 − 24 = 8 bits free, so 2⁸ = **256** addresses.
> - Splitting a `/16` into `/24`s fixes 24 − 16 = 8 more bits, so there are 2⁸ = **256** subnets.
>
> `10.0.0.0/16` sits inside `10.x.x.x`, one of the **private** ranges from Chapter 34: addresses used inside a network and never routed on the public internet.

Now the same arithmetic in Python, with its standard `ipaddress` module:

```python
import ipaddress

vpc = ipaddress.ip_network("10.0.0.0/16")
print(vpc.num_addresses)
print(2 ** (32 - 16))
```

```
65536
65536
```

- `import ipaddress` loads Python's built-in module for IP addresses; there's nothing to install.
- `ipaddress.ip_network("10.0.0.0/16")` turns the text into a network object that knows its own size.
- `.num_addresses` is how many addresses the range holds. The second line does the by-hand sum, and they agree.

Next, split it into `/24` subnets:

```python
subnets = list(vpc.subnets(new_prefix=24))
print(len(subnets), "subnets of", subnets[0].num_addresses, "addresses each")
print("first:", subnets[0], " second:", subnets[1], " last:", subnets[-1])
```

```
256 subnets of 256 addresses each
first: 10.0.0.0/24  second: 10.0.1.0/24  last: 10.0.255.0/24
```

- `vpc.subnets(new_prefix=24)` splits the network into pieces with a `/24` prefix. It hands them out one at a time, as a **generator** (Chapter 33), so `list(...)` collects them all into a list you can count and index.
- `subnets[0]`, `subnets[1]`, `subnets[-1]` are the first, second, and last. Each `/24` moves the third number along by one: `10.0.0.0`, `10.0.1.0`, up to `10.0.255.0`.

Finally, Riverstone's plan: two public and two private subnets, one of each per availability zone. **Before you run it, predict:** how many addresses of a 256-address subnet can the pipeline actually use?

```python
plan = {
    "public-a  (load balancer, zone A)": subnets[0],
    "public-b  (load balancer, zone B)": subnets[1],
    "private-a (pipeline, database, A)": subnets[2],
    "private-b (pipeline, database, B)": subnets[3],
}
for name, subnet in plan.items():
    usable = subnet.num_addresses - 5          # AWS reserves 5 addresses in every subnet
    print(f"{name}  {str(subnet):<12}  usable: {usable}")
print("remaining /24 subnets:", len(subnets) - len(plan))
```

```
public-a  (load balancer, zone A)  10.0.0.0/24   usable: 251
public-b  (load balancer, zone B)  10.0.1.0/24   usable: 251
private-a (pipeline, database, A)  10.0.2.0/24   usable: 251
private-b (pipeline, database, B)  10.0.3.0/24   usable: 251
remaining /24 subnets: 252
```

- `plan` is a dictionary from a subnet's job to the subnet itself; `.items()` gives each pair in turn.
- `subnet.num_addresses - 5` is the number of addresses you can actually give to machines. **AWS (and Azure) reserve five addresses in every subnet** for their own use: the network address, a router, DNS, one kept for the future, and the last address. **Google Cloud reserves four.** This chapter uses AWS's rule.
- `str(subnet):<12` turns the subnet into text and pads it to 12 characters, so the columns line up.

**Reading it.** Four `/24` subnets of 251 usable addresses each, far more than Riverstone's pipeline will ever need, and 252 left over for the future. What happens if you change `new_prefix=24` to `new_prefix=26`? Each subnet shrinks to 2⁶ = 64 addresses (59 usable), and there are 2¹⁰ = 1,024 of them. Exercise 4 asks when that's the better choice.

![A VPC of 10.0.0.0/16 containing two availability zones. Each zone has a public subnet, 10.0.0.0/24 in zone A and 10.0.1.0/24 in zone B, holding a load balancer, and below it a private subnet, 10.0.2.0/24 in zone A and 10.0.3.0/24 in zone B, holding the pipeline container and the database, each with 251 usable hosts. A footer explains that the public subnet accepts internet traffic on port 443, HTTPS, and the private subnet accepts traffic only from the public subnet's security group.](figures/fig52-2-vpc-subnets.svg)

*Figure 52.2 — Riverstone's VPC, matching the four subnets computed in this section: one public and one private subnet per availability zone.*

**The rule for security groups**, expressed the way Chapter 47 expressed data tests: **security groups deny all incoming traffic until you add a rule** (outgoing traffic is allowed by default), **so add only the specific rule a real need justifies.** The load balancer accepts HTTPS on port 443 (Chapter 34) from the internet. The pipeline's security group allows inbound traffic on its one port from the load balancer's security group specifically, not from `0.0.0.0/0` (every address on the internet). Riverstone's database's security group allows inbound traffic on its port, 5432, from the pipeline's security group, and nothing else.

---

## 52.2 Containers

### Why containers exist

"It works on my machine" is a symptom of one thing: the code depends on details of that machine, whether library versions, environment variables, or configuration files, that aren't written down anywhere. A **container** packages an application with everything it needs to run, as a single, versioned artifact that behaves identically wherever it's run.

An **image** is the packaged artifact; a **container** is a running instance of that image. You build an image once and run as many containers from it as you need. Images are shared through a **registry**, a library of images: **Docker Hub** is the public one, and every cloud has a private one. Each image has a name and a **tag**, written `name:tag`, such as `python:3.14-slim`; the tag says which version.

### Installing Docker, and your first container

**Docker** is the most common tool for building and running containers.

- **Windows and macOS:** install **Docker Desktop** from docker.com. It's free for personal use, education, and small businesses; larger companies need a paid plan, which your employer would arrange. On Windows it runs on WSL 2, the Linux layer Chapter 34 (section 34.1) installed, and its installer asks to use it.
- **Linux (and WSL, if you prefer not to use Docker Desktop):** install **Docker Engine** from your distribution's instructions on docs.docker.com. Add yourself to the `docker` group, so you don't need `sudo` for every command, then log out and in again.

Start Docker Desktop (Docker Engine starts on its own), open a terminal, and check it:

<!-- run: none -->
```
# terminal
$ docker --version
Docker version 29.3.1, build c2be9cc

$ docker run --rm hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

- **`docker --version`** proves the command is installed. Your version number will be newer or older; anything from the last year or two behaves the same for this chapter.
- **`docker run hello-world`** downloads a tiny image called `hello-world` from Docker Hub and starts a container from it. The container prints its message and stops. The first time, Docker also prints a few lines saying it can't find the image locally and is downloading it.
- **`--rm`** removes the stopped container afterwards, so finished containers don't pile up.
- The message names the two halves of Docker: the **client** (the `docker` command you type) and the **daemon** (a background program that does the work). If you see "Cannot connect to the Docker daemon", Docker Desktop isn't running: start it and try again.

### A Dockerfile for the Riverstone pipeline

A **Dockerfile** is a script that builds an image, one instruction at a time. The folder you build from is called the **build context**: Docker can copy only files inside it. So `pipeline_image/` holds everything the image needs, and nothing it doesn't:

| File | What it is |
|---|---|
| `ingest.py`, `riverstone_pipeline.py` | Chapter 46's pipeline, copied unchanged |
| `run_flash.py` | Runs the Flash once, for one day, and exits (below) |
| `requirements.txt` | The Python packages, pinned to the versions Chapters 45 and 46 used |
| `.dockerignore` | Files Docker must never copy into the image |
| `Dockerfile` | The build instructions |

Chapter 46's practice helpers, `mock_crm_api.py`, `make_files.py`, and `apply_day.py`, stand in for the ERP and the CRM. They're for testing, so they stay out of the image.

**What runs in the container.** Chapter 46 ran the pipeline under `dagster dev`, which keeps a web page and a scheduler running all day. That's the right tool on your laptop. Dagster's own documentation says it isn't for production, and it isn't what a once-a-day job needs anyway: in the cloud, the platform's scheduler starts the container at 6:30, the container builds the Flash, and it stops, so you pay for minutes, not days (section 52.7). `run_flash.py` does exactly that one job:

<!-- run: none -->
```python
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from riverstone_pipeline import defs

parser = argparse.ArgumentParser(description="Run the Daily Sales Flash for one day.")
parser.add_argument("--day", help="the day to build, as YYYY-MM-DD (default: yesterday, India time)")
args = parser.parse_args()
yesterday = datetime.now(ZoneInfo("Asia/Kolkata")) - timedelta(days=1)
day = args.day or yesterday.strftime("%Y-%m-%d")

job = defs.resolve_job_def("daily_flash_job")
result = job.execute_in_process(partition_key=day, raise_on_error=False)
print(f"Flash for {day}:", "succeeded" if result.success else "FAILED")
raise SystemExit(0 if result.success else 1)
```

**How it works, line by line.** You don't run this in the notebook; it runs inside the container.

- `argparse` reads an optional `--day` from the command line, as in Chapter 18 (section 18.15). `description=` and `help=` are the text `python run_flash.py --help` prints. `args.day` is `None` when `--day` isn't given.
- `yesterday` is now, in India time, minus one day (`timedelta`, `ZoneInfo`: Chapter 20). `strftime("%Y-%m-%d")` writes it as `2026-01-02`. `args.day or ...` uses the given day if there is one, otherwise yesterday: the same day Chapter 46's 6:30 schedule builds.
- `defs` is the `Definitions` object from `riverstone_pipeline.py`. `resolve_job_def("daily_flash_job")` fetches the job by name, as Chapter 46 fetched the schedule with `resolve_schedule_def`.
- `execute_in_process(partition_key=day, raise_on_error=False)` runs the whole job for that one day, in this process, like Chapter 46's `materialize()`.
- `raise SystemExit(0 if result.success else 1)` ends the program with **exit code** 0 if the run worked and 1 if it didn't (Chapter 26, section 26.0). The platform that starts the container reads that code to decide whether the morning's run failed.

`requirements.txt` pins every package:

```text
dagster==1.13.23
dagster-webserver==1.13.23
duckdb==1.5.6
psycopg2-binary==2.9.13
requests==2.33.1
python-dotenv==1.2.3
```

`psycopg2-binary` is the PostgreSQL driver Chapter 45 installed. The `-binary` version comes with everything it needs already compiled, so the image needs no C compiler and no system packages to install it. `dagster-webserver` is only for the local web page, later in this section.

`.dockerignore` lists what Docker must never copy into the image, the image-side twin of Chapter 26's `.gitignore`:

```text
.env
__pycache__/
warehouse/
outbox/
alerts/
exports/
```

`.env` holds your passwords (Chapter 45, section 45.2). An image can be copied to anyone who can pull it, so a password copied into one is as good as published. The four folders are data the pipeline writes, which belongs outside the image.

Here's the Dockerfile:

```dockerfile
FROM python:3.14-slim

RUN useradd --create-home pipeline

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ingest.py riverstone_pipeline.py run_flash.py ./
RUN mkdir warehouse exports outbox alerts /home/pipeline/dagster_home \
    && chown pipeline warehouse exports outbox alerts /home/pipeline/dagster_home

ENV PYTHONUNBUFFERED=1
ENV DAGSTER_HOME=/home/pipeline/dagster_home
ENV RIVERSTONE_SOURCE="dbname=riverstone_source"

USER pipeline

CMD ["python", "run_flash.py"]
```

**Every line, and why it's in that order.**

| Line | What it does |
|---|---|
| `FROM python:3.14-slim` | Starts from Docker Hub's official Python image, the version Chapter 17 installed. `slim` is a small Debian Linux with Python and little else: less to download, less to keep secure. |
| `RUN useradd --create-home pipeline` | `RUN` runs a command while the image is built. This one creates an ordinary user called `pipeline` with a home folder (`--create-home`), to run as later. It comes early because it never changes, so Docker can reuse it (caching, below). |
| `WORKDIR /app` | Makes `/app` the working folder for everything after it, creating it if needed, like `cd` that also creates the folder. |
| `COPY requirements.txt .` | Copies one file from the build context into the image. `.` means "the working folder", `/app`. |
| `RUN pip install --no-cache-dir -r requirements.txt` | Installs the packages. `--no-cache-dir` tells pip not to keep its download cache, which would only make the image bigger. |
| `COPY ingest.py riverstone_pipeline.py run_flash.py ./` | Copies the three program files. With several files, the destination must end in `/`, so `./` rather than `.`. |
| `RUN mkdir … \` | Creates the four folders the pipeline writes to, and Dagster's home folder. The `\` at the end of a line continues the command on the next line. |
| `&& chown pipeline …` | `&&` runs the second command only if the first worked (Chapter 26). `chown` gives the folders to the `pipeline` user, because everything created so far belongs to root. Chaining keeps both in one `RUN`, and one `RUN` makes one layer. |
| `ENV PYTHONUNBUFFERED=1` | `ENV` sets an environment variable in every container. This one makes Python print each line at once instead of saving lines up, so logs appear as they happen. |
| `ENV DAGSTER_HOME=…` | Where Dagster keeps its files when you run `dagster dev` in the container, later in this section. |
| `ENV RIVERSTONE_SOURCE="dbname=riverstone_source"` | A default that isn't secret. The real connection string, with its password, arrives when the container starts (section 52.6). |
| `USER pipeline` | Everything from here, including the running container, runs as `pipeline`, not root, so a flaw in the application can't easily take over the whole container. |
| `CMD ["python", "run_flash.py"]` | What runs when a container starts. The list form, with each word in quotes, runs the program directly; it's called the **exec form**. You can replace it when you start a container, as you'll do below. |

**Order matters for caching.** Docker builds an image in **layers**, one for each `RUN`, `COPY`, or `ADD` instruction, and it reuses a cached layer when nothing that affects it has changed. The packages are installed **before** the application code is copied. If the code were copied first, editing a single line of `ingest.py` would invalidate every layer after it, including the slow package install. Copying dependencies first means a code change rebuilds in seconds, not minutes.

![Seven numbered boxes in build order: 1, FROM python 3.14 slim, the base image; 2, RUN useradd, the user to run as, made once; 3, WORKDIR, COPY requirements.txt and RUN pip install, the dependencies, rebuilt only when requirements.txt changes; 4, COPY the three Python files, application code, what usually changes; 5, RUN mkdir and chown, the folders the pipeline writes to; 6, ENV and USER pipeline, settings and no longer root; 7, CMD python run_flash.py, what runs when a container starts. A footer says steps 1 to 3 rarely change, so Docker reuses them from its cache, and editing ingest.py rebuilds from step 4 down.](figures/fig52-3-dockerfile-layers.svg)

*Figure 52.3 — The Dockerfile's steps, in build order. Ordering dependencies before code is what makes rebuilds fast.*

### Building and running the image

In a terminal, go into `pipeline_image` and build:

<!-- run: none -->
```
# terminal
$ cd pipeline_image
$ docker build -t riverstone/pipeline:1.4.0 .
```

- **`docker build`** reads the `Dockerfile` in the build context and builds an image.
- **`-t riverstone/pipeline:1.4.0`** names and tags it. `riverstone/` is the owner's name, the way Docker Hub groups images; `1.4.0` is this version of the pipeline.
- **`.`** at the end is the build context: this folder.

The first build downloads the Python image and the packages, which takes a minute or two, and prints a line for each step, ending with `naming to docker.io/riverstone/pipeline:1.4.0 done`. Now list your images, and start a container just to ask who it runs as:

<!-- run: none -->
```
# terminal
$ docker image ls riverstone/pipeline
IMAGE                       ID             DISK USAGE   CONTENT SIZE   EXTRA
riverstone/pipeline:1.4.0   3834b8617d20        573MB          134MB

$ docker run --rm riverstone/pipeline:1.4.0 whoami
pipeline
```

- **`docker image ls riverstone/pipeline`** lists images with that name. The image takes 573 MB on disk; 134 MB is what gets downloaded, because the layers are compressed. Your ID will differ.
- **`docker run --rm riverstone/pipeline:1.4.0 whoami`**: anything after the image name replaces its `CMD`. `whoami` prints the current user: `pipeline`, not root, as the Dockerfile asked.

**Now run the pipeline in the container, for real.** It needs what it needed in Chapter 46: the practice source, `riverstone_source`, in your PostgreSQL; the practice CRM API; your `.env` file; and the folders. Set them up as Chapter 46's first run did (section 46.3): in its notebook, run `reset()` and then `apply_day(1)`, shut the notebook's kernel down so it lets go of the warehouse file, and start `python mock_crm_api.py` in a second terminal. Your `.env` from Chapter 45 names `host=localhost`, which is what the container needs. Then, in `work/ch46`:

<!-- run: none -->
```
# terminal
$ docker run --rm --network host --env-file .env -v ./exports:/app/exports -v ./warehouse:/app/warehouse -v ./outbox:/app/outbox riverstone/pipeline:1.4.0 python run_flash.py --day 2026-01-02 2> run.log
Flash for 2026-01-02: succeeded

$ echo $?
0

$ cat outbox/flash_2026-01-02.txt
Riverstone Daily Sales Flash - 2026-01-02
Orders booked: 2
Net bookings (excl. cancelled, net of discounts): Rs 38,710.00
```

**How it works, piece by piece.**

- **`--network host`** lets the container use your computer's own network, so `localhost` inside it means your computer, where PostgreSQL and the practice API are listening. On Linux this just works. On Docker Desktop, host networking must first be switched on (Settings, Resources, Network, *Enable host networking*; it needs Docker Desktop 4.34 or later and a free Docker sign-in).
- **`--env-file .env`** passes every line of your `.env` file to the container as environment variables. That's how the password reaches the pipeline without ever being in the image.
- **`-v ./exports:/app/exports`** mounts a **volume**: the folder `exports` on your computer appears inside the container as `/app/exports`. Anything the container writes there stays on your computer after the container is gone. The warehouse and outbox are mounted the same way, so the container reads and writes Chapter 46's own files.
- On Linux, if the run fails because it can't write to `warehouse` or `outbox`, your user ID differs from the container user's; `chmod a+w warehouse outbox` (Chapter 34, section 34.5) lets it write, for practice.
- **`python run_flash.py --day 2026-01-02`** replaces `CMD`, to build the practice day instead of yesterday.
- **`2> run.log`** sends Dagster's own messages (about 50 lines of its event log, which it writes to standard error) into a file (Chapter 34, section 34.2), leaving just the program's last line on screen.
- **`echo $?`** prints the exit code: 0, success, the value a scheduler would check.

**Reading it.** The container built 2 January's Flash, 2 orders for ₹38,710.00, the same numbers Chapter 46 produced on your laptop. Nothing in the container came from your computer except the settings you passed in and the folders you mounted: the Python, the packages, and the code are the image's own, which is the whole point.

**Watch the cache work.** Make a one-line change to `ingest.py` (add a comment at the end) and build again, this time with the tag `1.4.1`. The build prints a numbered line for each step; these are the lines for the five steps before the code:

<!-- run: none -->
```
# terminal
$ docker build -t riverstone/pipeline:1.4.1 .
#6 [3/7] WORKDIR /app
#6 CACHED
#7 [4/7] COPY requirements.txt .
#7 CACHED
#8 [2/7] RUN useradd --create-home pipeline
#8 CACHED
#9 [5/7] RUN pip install --no-cache-dir -r requirements.txt
#9 CACHED
#10 [6/7] COPY ingest.py riverstone_pipeline.py run_flash.py ./
#10 DONE 0.0s
#11 [7/7] RUN mkdir warehouse exports outbox alerts /home/pipeline/dagster_home     && chown pipeline warehouse exports outbox alerts /home/pipeline/dagster_home
#11 DONE 0.1s
```

`CACHED` means Docker reused the layer instead of rebuilding it. Everything up to the package install was reused, and only the code and the step after it were rebuilt, in a fraction of a second. (Docker sometimes prints the steps slightly out of order, as here; the `[n/7]` numbers give the real order.) What happens if you change `requirements.txt` instead? Step 5 and every step after it rebuild, and the packages download again. Delete the extra image when you're done: `docker image rm riverstone/pipeline:1.4.1`.

> **Try the web page too.** `dagster dev` works in the container, for looking around on your laptop: the Compose file below starts it. Two things make it laptop-only. Its web page and scheduler run all day, which costs money in the cloud for a job that needs minutes (section 52.7). And it keeps its run history in files inside the container, in `DAGSTER_HOME`, so the history disappears whenever the container is replaced. A production Dagster runs its web page and its scheduler as separate programs, with the history kept in a PostgreSQL database; Dagster's deployment guide covers it.

### Checking the Dockerfile with a parser

A **parser** reads a file into a structure a program can check: here, lists and dictionaries. Back in your notebook, in `work/ch52`:

```python
from dockerfile_parse import DockerfileParser

d = DockerfileParser("pipeline_image")
print(d.structure[0])
```

```
{'instruction': 'FROM', 'startline': 0, 'endline': 0, 'content': 'FROM python:3.14-slim\n', 'value': 'python:3.14-slim'}
```

- `DockerfileParser("pipeline_image")` points the parser at the folder; it reads the file called `Dockerfile` in it.
- `d.structure` is a list with one dictionary per instruction. The first one shows the shape: the instruction's name, its first and last line (counting from 0), the full text, and the `value` after the instruction's name. Comments, if the file had any, would appear as entries named `COMMENT`.

Now check the facts that matter:

```python
print("base image :", d.baseimage)
print("instructions:", [s["instruction"] for s in d.structure])
print("layers (RUN/COPY/ADD):", sum(1 for s in d.structure if s["instruction"] in ("RUN", "COPY", "ADD")))
print("runs as user:", [s["value"] for s in d.structure if s["instruction"] == "USER"])
```

```
base image : python:3.14-slim
instructions: ['FROM', 'RUN', 'WORKDIR', 'COPY', 'RUN', 'COPY', 'RUN', 'ENV', 'ENV', 'ENV', 'USER', 'CMD']
layers (RUN/COPY/ADD): 5
runs as user: ['pipeline']
```

- `d.baseimage` is the image named in `FROM`.
- The list comprehension collects every instruction's name, in order.
- `sum(1 for s in ... if ...)` counts the instructions that make a layer: five (two `COPY`, three `RUN`).
- The last line collects the value of every `USER` instruction: the container drops root.

**Reading it.** The parser confirms the file is well formed and lets you check facts about it, such as "it never runs as root", in a test. A **linter** goes further: a tool such as hadolint reads a Dockerfile and flags risky patterns, such as installing system packages without pinning their versions. You've also built the image for real, which is the final check.

### Running more than one container together

A single pipeline usually needs a database alongside it during development. **Docker Compose**, which comes with Docker Desktop (on Linux, install the `docker-compose-plugin` package), describes a small stack of containers as one file, `docker-compose.yml`. Compose reads its passwords from a `.env` file in the same folder. Copy `.env.example` to `.env` and put your own values in it:

```text
POSTGRES_PASSWORD=change-me-locally
CRM_API_TOKEN=practice-token-45
```

`.env` is in the `.gitignore` of your Chapter 26 repository and in `.dockerignore`, so it never reaches Git or an image. `.env.example`, with no real values, is the one you commit, so others know which settings to provide. Here's the Compose file:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: riverstone_source
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 10

  pipeline:
    build: .
    command: ["dagster", "dev", "-f", "riverstone_pipeline.py", "-h", "0.0.0.0", "-p", "3000"]
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      RIVERSTONE_SOURCE: "dbname=riverstone_source host=postgres user=postgres password=${POSTGRES_PASSWORD}"
      CRM_API_TOKEN: ${CRM_API_TOKEN}
    ports:
      - "3000:3000"
    restart: unless-stopped

volumes:
  pgdata:
```

**Line by line.**

| Line | What it means |
|---|---|
| `services:` | The containers in the stack, each under its own name. The names double as network names: inside the stack, the database is reachable at the host name `postgres`. |
| `image: postgres:16` | Use the official PostgreSQL 16 image from Docker Hub, the version the book uses. |
| `POSTGRES_DB: riverstone_source` | The image creates a database with this name on first start. Without it, only a database called `postgres` would exist, and the pipeline's connection would fail. It starts empty; the point here is the wiring. |
| `POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}` | `${NAME}` is filled in by Compose, when you run it, from your shell's environment or the `.env` file. The password is never written in this file. |
| `volumes: - pgdata:...` | Keeps the database's files, in the container's folder `/var/lib/postgresql/data`, in a **named volume** called `pgdata`, which Docker stores for you. The data survives when the containers are removed. |
| `ports: - "5433:5432"` | `laptop:container`. Port 5433 on your laptop reaches PostgreSQL's port 5432 in the container. Not 5432 on the laptop, because your own PostgreSQL already uses it. Handy locally; in the cloud a database port is never opened this way (section 52.1's security groups). |
| `healthcheck:` | How Docker tells whether PostgreSQL is ready: every 5 seconds (`interval`), up to 10 times (`retries`), it runs `pg_isready`, PostgreSQL's own "are you accepting connections?" command. `CMD-SHELL` means "run this as a shell command". |
| `build: .` | Build this service's image from the Dockerfile in this folder. |
| `command: [...]` | Replaces the image's `CMD` for this service: here, `dagster dev`, the web page and scheduler, on all network addresses (`-h 0.0.0.0`) and port 3000 (`-p 3000`), so the page is reachable from outside the container. |
| `depends_on: postgres: condition: service_healthy` | Start the pipeline only once the database's health check passes. Without the condition, Compose waits only for the database's container to *start*, and PostgreSQL may not accept connections for a few more seconds. |
| `RIVERSTONE_SOURCE: "... host=postgres ..."` | The connection string, pointing at the `postgres` service by name. |
| `restart: unless-stopped` | If the pipeline's container stops on its own, start it again, unless you stopped it. |
| `volumes: pgdata:` (at the bottom) | Declares the named volume used above. |

Check it with the parser before running it:

```python
import yaml

with open("pipeline_image/docker-compose.yml") as f:
    compose = yaml.safe_load(f)
print("services:", list(compose["services"]))
print("pipeline waits for:", compose["services"]["pipeline"]["depends_on"])
print("postgres health check:", compose["services"]["postgres"]["healthcheck"]["test"])
print("pipeline environment:", list(compose["services"]["pipeline"]["environment"]))
```

```
services: ['postgres', 'pipeline']
pipeline waits for: {'postgres': {'condition': 'service_healthy'}}
postgres health check: ['CMD-SHELL', 'pg_isready -U postgres']
pipeline environment: ['RIVERSTONE_SOURCE', 'CRM_API_TOKEN']
```

- `yaml.safe_load(f)` reads YAML into dictionaries and lists. `safe_load` refuses anything but plain data, which is the right default for files from anywhere.
- The prints walk the structure with keys, as with any dictionary.

**Reading it.** Two services, and the pipeline waits until PostgreSQL is actually ready, not just started. Both secrets arrive through environment variables from `.env`. Now run it, in `pipeline_image`:

<!-- run: none -->
```
# terminal
$ docker compose up -d
 Network pipeline_image_default Creating 
 Network pipeline_image_default Created 
 Volume pipeline_image_pgdata Creating 
 Volume pipeline_image_pgdata Created 
 Container pipeline_image-postgres-1 Creating 
 Container pipeline_image-postgres-1 Created 
 Container pipeline_image-pipeline-1 Creating 
 Container pipeline_image-pipeline-1 Created 
 Container pipeline_image-postgres-1 Starting 
 Container pipeline_image-postgres-1 Started 
 Container pipeline_image-postgres-1 Waiting 
 Container pipeline_image-postgres-1 Healthy 
 Container pipeline_image-pipeline-1 Starting 
 Container pipeline_image-pipeline-1 Started 

$ docker compose ps
NAME                        IMAGE                     COMMAND                  SERVICE    CREATED          STATUS                    PORTS
pipeline_image-pipeline-1   pipeline_image-pipeline   "dagster dev -f rive…"   pipeline   14 seconds ago   Up 7 seconds              0.0.0.0:3000->3000/tcp
pipeline_image-postgres-1   postgres:16               "docker-entrypoint.s…"   postgres   14 seconds ago   Up 13 seconds (healthy)   0.0.0.0:5433->5432/tcp
```

- **`docker compose up -d`** builds what needs building, creates a private network and the volume, and starts both containers. `-d` (detached) runs them in the background and gives you the prompt back. Notice `Waiting` then `Healthy`: the pipeline started only after the health check passed.
- **`docker compose ps`** lists the stack's containers and their state. For any container, `docker ps` does the same.

`docker compose logs pipeline` prints what the pipeline container has written; after a few seconds its last line reads `Serving dagster-webserver on http://0.0.0.0:3000`, and `http://127.0.0.1:3000` in your browser shows Chapter 46's graph. To stop:

<!-- run: none -->
```
# terminal
$ docker compose down
 Container pipeline_image-pipeline-1 Stopping 
 Container pipeline_image-pipeline-1 Stopped 
 Container pipeline_image-pipeline-1 Removing 
 Container pipeline_image-pipeline-1 Removed 
 Container pipeline_image-postgres-1 Stopping 
 Container pipeline_image-postgres-1 Stopped 
 Container pipeline_image-postgres-1 Removing 
 Container pipeline_image-postgres-1 Removed 
 Network pipeline_image_default Removing 
 Network pipeline_image_default Removed 
```

`docker compose down` stops and removes the containers and the network, but not the named volume, so the database's data is still there next time. (`docker stop <name>` stops a single container.)

---

## 52.3 Orchestrating containers

### What Kubernetes actually solves

Running one container by hand is easy. Running many, across many machines, so that a crashed one restarts, traffic reaches a healthy one, and a busy period gets more capacity automatically, is what **Kubernetes** does. It's worth understanding even for a company Riverstone's size, because it's the vocabulary most cloud job descriptions and most managed platforms are built on. **Read this section for its vocabulary.** Trying it on your laptop is optional, and described at the end of the section.

| Object | What it is |
|---|---|
| **Cluster** | A group of machines that Kubernetes manages as one |
| **Node** | One machine in the cluster |
| **Pod** | The smallest deployable unit: one or more containers that always run together, on the same node |
| **Job** | Runs a Pod until it finishes successfully, once |
| **CronJob** | Creates a Job on a schedule, like the scheduler in Chapter 46 |
| **Deployment** | Keeps a stated number of copies (**replicas**) of a Pod running all the time, and rolls out new versions |
| **Service** | A stable network address in front of a changing set of Pods, so other things can find them reliably |
| **Secret** | A piece of sensitive configuration (a token, a password), stored separately from the container image |
| **Namespace** | A way of dividing one cluster into separate areas, for different teams or environments |

You describe the objects you want in YAML files called **manifests**, and Kubernetes makes the cluster match them.

### A CronJob for the Daily Sales Flash

The Flash is a batch job: it should start at 6:30 every morning, run once, and stop. That's a **CronJob**. Here is the smallest one that would work:

<!-- run: none -->
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: daily-flash
  namespace: riverstone
spec:
  schedule: "30 6 * * *"
  timeZone: "Asia/Kolkata"
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: pipeline
              image: riverstone/pipeline:1.4.0
```

**Line by line.**

- **`apiVersion: batch/v1`** says which part of Kubernetes' vocabulary the object comes from, and which version of it. Batch objects (Job, CronJob) are in `batch/v1`; Deployments are in `apps/v1`; the oldest, core objects, such as Service, just say `v1`.
- **`kind: CronJob`** is the type of object.
- **`metadata:`** names it: `name: daily-flash`, and `namespace: riverstone`, the area of the cluster it lives in, so Riverstone's objects stay apart from everyone else's.
- **`spec:`** (specification) is what you want. **`schedule: "30 6 * * *"`** is the same cron expression Chapter 46's schedule printed: minute 30, hour 6, every day. **`timeZone: "Asia/Kolkata"`** makes that 6:30 India time; without it, the cluster's own clock decides, often UTC.
- **`concurrencyPolicy: Forbid`** says never to start a run while the previous one is still going. A Flash must never be built twice at once (Chapter 46's idempotency lessons).
- **`jobTemplate:`** is the Job to create each morning, and inside it, **`template:`** is the Pod that Job runs. The nesting reads: a CronJob makes Jobs, a Job makes a Pod.
- **`restartPolicy: OnFailure`** restarts the container if it exits with a non-zero code: `run_flash.py`'s exit code, doing its job.
- **`containers:`** is a YAML list: each item starts with `- `. This Pod has one container, named `pipeline`, started from the image built in section 52.2. The container runs the image's `CMD`, so each morning it builds yesterday.

A real run needs two more things: its secrets, and limits on what it may use. Added to the container, they make the companion file `k8s/pipeline-cronjob.yaml`:

<!-- run: none -->
```yaml
            - name: pipeline
              image: riverstone/pipeline:1.4.0
              env:
                - name: RIVERSTONE_SOURCE
                  valueFrom:
                    secretKeyRef:
                      name: riverstone-db-secret
                      key: connection-string
                - name: CRM_API_TOKEN
                  valueFrom:
                    secretKeyRef:
                      name: riverstone-crm-secret
                      key: token
              resources:
                requests:
                  cpu: "250m"
                  memory: "512Mi"
                limits:
                  cpu: "1"
                  memory: "1Gi"
```

- **`env:`** sets environment variables in the container, a list of `name` plus where the value comes from. **`valueFrom: secretKeyRef:`** takes it from a Kubernetes Secret: the one `name`d `riverstone-db-secret`, its entry with the `key` `connection-string`. The values never appear in this file, which you can safely commit.
- **`resources.requests`** is what the Pod is guaranteed, and what the cluster uses to choose a node with room for it. **`limits`** is the ceiling. `m` means thousandths of a CPU core, so `250m` is a quarter of a core and `"1"` a whole one. `Mi` and `Gi` are mebibytes and gibibytes, the binary units of Chapter 2 (1 Mi = 1,024 × 1,024 bytes).

Check the whole file:

```python
with open("k8s/pipeline-cronjob.yaml") as f:
    cron = yaml.safe_load(f)
pod = cron["spec"]["jobTemplate"]["spec"]["template"]["spec"]
container = pod["containers"][0]
print(cron["kind"], cron["metadata"]["name"], "in namespace", cron["metadata"]["namespace"])
print("schedule:", cron["spec"]["schedule"], cron["spec"]["timeZone"])
print("image   :", container["image"])
print("secrets :", [e["valueFrom"]["secretKeyRef"]["name"] for e in container["env"]])
print("cpu request/limit:", container["resources"]["requests"]["cpu"], "/", container["resources"]["limits"]["cpu"])
```

```
CronJob daily-flash in namespace riverstone
schedule: 30 6 * * * Asia/Kolkata
image   : riverstone/pipeline:1.4.0
secrets : ['riverstone-db-secret', 'riverstone-crm-secret']
cpu request/limit: 250m / 1
```

- `pod = ...` walks down the nesting, CronJob to Job to Pod, once, so the next lines stay short.
- `container["env"]` is a list of dictionaries; the list comprehension picks each one's Secret name.

**Reading it.** One CronJob, 6:30 India time, the image from section 52.2, two Secrets referenced and never inlined. A parser checks that the YAML is well formed, not that Kubernetes would accept it. For that, a tool called kubeconform checks manifests against Kubernetes' own rules without a cluster; it was run on both of this section's files and reported `Valid: 3, Invalid: 0` (the second file holds two objects).

### Services that run all the time: Deployment and Service

A CronJob suits work that starts and stops. A web page must answer at any moment, so it runs all the time, usually in more than one copy. Suppose Riverstone later adds a small internal web page showing the latest Flash (Exercise 11 imagines it), called `flash-page`. It keeps no data of its own: it reads the warehouse. That's `k8s/flash-page.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flash-page
  namespace: riverstone
spec:
  replicas: 2
  selector:
    matchLabels:
      app: flash-page
  template:
    metadata:
      labels:
        app: flash-page
    spec:
      containers:
        - name: web
          image: riverstone/flash-page:1.0.0
          ports:
            - containerPort: 8080
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: flash-page
  namespace: riverstone
spec:
  selector:
    app: flash-page
  ports:
    - port: 80
      targetPort: 8080
  type: ClusterIP
```

**Line by line, the new parts.**

- **`replicas: 2`** keeps two copies running. If one crashes, or its node fails, Kubernetes starts a replacement, and the other keeps answering meanwhile.
- **Labels** are name tags: `labels: app: flash-page` under `template.metadata` puts the tag `app=flash-page` on every Pod the Deployment makes. **`selector: matchLabels: app: flash-page`** tells the Deployment which Pods are its own, so it can count them. The two must match, or Kubernetes rejects the Deployment.
- **`containerPort: 8080`** records the port the web page listens on inside the container.
- **`readinessProbe`** is how Kubernetes decides a Pod is ready for traffic: it asks for `/healthz` on port 8080 every few seconds, starting 5 seconds after the container starts (`initialDelaySeconds`), and sends a Pod traffic only while the answer is a success. **The path must be one the application actually serves**; this page would serve `/healthz` for exactly this purpose. Check before you deploy: Dagster's web server, for example, answers `/server_info`. A **liveness probe**, written the same way, goes one step further: when it fails, Kubernetes restarts the container.
- **`---`** separates two YAML documents in one file: the Deployment, then the Service.
- **The Service** finds its Pods by the same label (`selector: app: flash-page`) and gives them one stable name, `flash-page`, on port 80, forwarding to port 8080 (`targetPort`) on whichever Pod is ready.
- **`type: ClusterIP`** means the Service is reachable only from inside the cluster, which suits an internal page. To reach something from the internet you'd use `type: LoadBalancer`, which asks the cloud for a load balancer like the one in Figure 52.2, or an **Ingress**, one shared entrance for several services.

![A Deployment box, flash-page, with replicas 2 and selector app flash-page, and a Service box, flash-page, port 80 to 8080, with the same selector. Arrows from both point to two Pod boxes, each labelled app flash-page. The Deployment's arrows say it keeps two Pods with this label; the Service's arrows say it sends traffic to Pods with this label. A footer says the three labels must match exactly, and a typo in one leaves the Service with no Pods to send to, with no error from Kubernetes.](figures/fig52-4-labels.svg)

*Figure 52.4 — Labels are how a Deployment counts its Pods and how a Service finds them.*

**Why the Flash isn't a Deployment with two replicas.** Two copies suit a web page because either copy can answer any request. A scheduled job is the opposite: if two copies each ran Chapter 46's 6:30 schedule, the Flash would be built and sent **twice** every morning. Replicas are for services that keep no state of their own; a job that must run exactly once belongs in a CronJob, or on a scheduler outside the cluster.

Check the file:

```python
with open("k8s/flash-page.yaml") as f:
    deployment, service = yaml.safe_load_all(f)
print(deployment["kind"], "replicas:", deployment["spec"]["replicas"])
print("labels match:", deployment["spec"]["selector"]["matchLabels"] == deployment["spec"]["template"]["metadata"]["labels"]
      == service["spec"]["selector"])
print(service["kind"], "port", service["spec"]["ports"][0]["port"], "->", service["spec"]["ports"][0]["targetPort"],
      f"({service['spec']['type']})")
```

```
Deployment replicas: 2
labels match: True
Service port 80 -> 8080 (ClusterIP)
```

- `yaml.safe_load_all(f)` reads every document in the file, one per `---`; `deployment, service = ...` unpacks the two.
- The second print compares the three label dictionaries in one chained `==`: `True` only if all three are equal.

### Secrets for the cluster

Both CronJob Secrets have to exist in the cluster before the first run. A Secret can be written as a manifest:

<!-- run: none -->
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: riverstone-crm-secret
  namespace: riverstone
stringData:
  token: replace-me
```

**Never commit a file like this with a real value in it.** A Secret is only **base64-encoded** when Kubernetes stores it (a reversible way of writing bytes as text, not encryption), and anyone who reads the file or the Git history has the token. Create Secrets from your `.env` file instead, so the value never lands in a file you might commit:

<!-- run: none -->
```
# terminal
$ kubectl create secret generic riverstone-crm-secret --namespace riverstone --from-env-file=.env
```

`kubectl create secret generic` makes a Secret named `riverstone-crm-secret`, with one entry per line of `.env`. Typing a value directly on the command line with `--from-literal=token=...` also works, but, as Chapter 34 warned about `export`, it lands in your shell's history. Section 52.6 covers the better options.

### Trying it on your laptop (optional, not executed here)

The book's practice machine can't run Kubernetes' own containers, so nothing in this subsection is executed here, and no output is shown. These steps are for your laptop, with Docker running.

1. Install **kind** ("Kubernetes in Docker", a whole cluster inside one Docker container) and **kubectl**, Kubernetes' command-line tool, from their documentation at kind.sigs.k8s.io and kubernetes.io.
2. `kind create cluster` creates a one-node cluster; `kubectl get nodes` lists it, with `Ready` in the status column.
3. `kind load docker-image riverstone/pipeline:1.4.0` copies your image into the cluster, which can't see your laptop's images otherwise.
4. `kubectl create namespace riverstone`, then create the two Secrets, as above.
5. `kubectl apply -f k8s/pipeline-cronjob.yaml` creates the CronJob. **`apply`** means "make the cluster match this file"; run it again after editing the file and it changes only what differs.
6. `kubectl get cronjobs -n riverstone` lists it with its schedule. `kubectl create job flash-now --from=cronjob/daily-flash -n riverstone` starts one run now, without waiting for 6:30; `kubectl get pods -n riverstone` shows its Pod, and `kubectl logs <pod name> -n riverstone` shows what the container printed. In the cluster, `localhost` means the Pod itself, so the connection string in `riverstone-db-secret` must name a database the Pod can reach.
7. For `flash-page.yaml` you'd need an image of that page. With one, `kubectl get pods` would list two Pods; `kubectl delete pod <one of them>` and a second `kubectl get pods` shows a new Pod with a new name taking its place: the Deployment keeping its promise of two.
8. `kind delete cluster` removes everything.

### When you don't need it

Kubernetes solves problems that come with scale and many services. Riverstone, with one pipeline, doesn't have that problem yet. A single managed container service (Chapter 46's job, deployed as one container on a managed platform such as AWS ECS on Fargate, which can start a container on a schedule) is simpler, cheaper, and has almost nothing to operate. **Reach for Kubernetes when you have several services that need to be scheduled, scaled, and networked together**, not because the term appears in job postings. Section 52.8 returns to this choice directly.

---

## 52.4 Infrastructure as Code

Clicking through a cloud provider's console to create a bucket works once. It doesn't tell the next person what was created, why, or how to make an identical one in another region. **Infrastructure as Code (IaC)** describes infrastructure in files that can be reviewed, versioned, and applied repeatably, the same discipline Chapter 29 taught for application code.

**Terraform** is the most widely used tool for this, and it works with every major cloud provider through the same workflow: write configuration, run `terraform plan` to see exactly what would change, and `terraform apply` to make it happen. Terraform keeps a **state file** recording what it created, which is how it knows the difference between "create this" and "this already exists, leave it alone." Terraform talks to each cloud through a **provider**, a plug-in it downloads. (OpenTofu, a free fork of Terraform, reads the same files with the command `tofu` instead of `terraform`.)

### Installing Terraform

- **Windows:** `winget install Hashicorp.Terraform` in PowerShell.
- **macOS:** `brew install hashicorp/tap/terraform` with Homebrew.
- **Linux and WSL:** follow the instructions for your distribution at developer.hashicorp.com/terraform/install.

Then check:

<!-- run: none -->
```
# terminal
$ terraform -version
Terraform v1.16.4
on linux_amd64
```

Your version may be newer; this chapter's files were checked with 1.16.4, and any recent version reads them. `linux_amd64` is the operating system and processor type; yours may say `windows_amd64` or `darwin_arm64` (a Mac).

### A configuration for the sensor archive, in four parts

Terraform files are written in **HCL** (HashiCorp Configuration Language) and end in `.tf`. The companion's `terraform/main.tf` creates the storage behind Chapter 49's sensor archive and the identity that's allowed to touch it. It has four parts.

**Part 1: settings, state, provider, and variables.**

<!-- run: none -->
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "riverstone-tfstate"
    key          = "platform/terraform.tfstate"
    region       = "ap-south-1"
    use_lockfile = true
  }
}

provider "aws" {
  region = var.aws_region
}

variable "aws_region" {
  description = "AWS region for Riverstone's data platform"
  type        = string
  default     = "ap-south-1" # Mumbai
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}
```

- HCL is made of **blocks**: a type, sometimes one or two labels in quotes, then settings inside `{ }`, each written `name = value`. `#` starts a comment.
- **`terraform { required_providers { ... } }`** says which providers this configuration needs. `source = "hashicorp/aws"` is the AWS provider, published by HashiCorp, Terraform's maker. `version = "~> 6.0"` accepts any 6.x version (6.0 or later, but below 7.0), so a future 7.0 with breaking changes can't arrive by surprise.
- **`backend "s3" { ... }`** says where the **state** lives: not on your laptop, but in an S3 bucket (`bucket`), under a file name (`key`), in Mumbai (`region`). `use_lockfile = true` makes Terraform write a small lock file next to the state while it works, so two people running Terraform at once can't corrupt each other's changes. (Older setups lock with a DynamoDB table instead.) The state bucket is created once, by hand or by a separate small configuration, before this one is used.
- **`provider "aws" { region = var.aws_region }`** configures the provider. **Credentials never go in this file.** The provider finds them in your environment: variables such as `AWS_PROFILE`, or a login made with AWS's own command-line tool. In CI they come from a role (section 52.5).
- **`variable "aws_region" { ... }`** declares an input: a `description` for people, a `type`, and a `default` used when nobody sets it. `var.aws_region` reads it. Variables let one file build Mumbai `production` or Singapore `staging` without editing.

**What the state holds.** The state file records every resource Terraform created and every attribute of it, including, for some resources, **passwords and keys in plain text**. So keep it in an encrypted, access-controlled bucket, never in Git: add `*.tfstate`, `*.tfstate.backup`, and `.terraform/` to your `.gitignore`.

**Part 2: the bucket, with versioning.**

<!-- run: none -->
```hcl
resource "aws_s3_bucket" "sensor_archive" {
  bucket = "riverstone-sensor-archive-${var.environment}"

  tags = {
    Project     = "analyst-to-architect"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_s3_bucket_versioning" "sensor_archive" {
  bucket = aws_s3_bucket.sensor_archive.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

- **`resource "aws_s3_bucket" "sensor_archive"`** has two labels: the **type** of thing to create (an S3 bucket, from the AWS provider) and a **name** that Terraform uses for it inside your files. The name never appears in AWS.
- **`"riverstone-sensor-archive-${var.environment}"`**: `${ ... }` inside a string inserts a value, so this becomes `riverstone-sensor-archive-production`. Bucket names are shared across all of AWS, which is why they're long and specific.
- **`tags = { ... }`** attaches labels to the bucket, a **map** of names to values. Tags are how a company finds, and pays for, what each project owns (Chapter 65, section 65.4).
- **`aws_s3_bucket.sensor_archive.id`** is a **reference**: `type.name.attribute`, the ID of the bucket above. A reference also tells Terraform the order: it must create the bucket before it can turn versioning on for it.
- **`versioning_configuration { status = "Enabled" }`** is a **nested block**, a block inside a resource. Versioning keeps every version of every object, so an overwritten or deleted file can be brought back. Versioning is what let Chapter 49's team restore the deleted days in its closing story; there it happened to be on, and here it's on by design.

**Part 3: what happens to old versions.**

<!-- run: none -->
```hcl
resource "aws_s3_bucket_lifecycle_configuration" "sensor_archive" {
  bucket = aws_s3_bucket.sensor_archive.id

  rule {
    id     = "old-versions-to-cold-storage"
    status = "Enabled"

    filter {}

    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER"
    }
  }
}
```

- A **lifecycle configuration** is a set of rules S3 applies to objects automatically. This one has one `rule`, with an `id` for people and `status = "Enabled"`.
- **`filter {}`**, empty, means "apply to every object in the bucket". A filter could name a folder instead.
- **`noncurrent_version_transition`** acts only on **previous versions**: when a file is overwritten, the old version becomes "noncurrent", and 90 days after that (`noncurrent_days`) it moves to `GLACIER`, a cold storage class that is much cheaper to keep and slower and dearer to read back. The current data never moves. That keeps versioning's safety net without paying hot-storage prices for it.

**Part 4: the pipeline's identity.**

<!-- run: none -->
```hcl
resource "aws_iam_role" "pipeline_role" {
  name = "riverstone-pipeline-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "ecs-tasks.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "pipeline_s3_access" {
  name = "sensor-archive-read-write"
  role = aws_iam_role.pipeline_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["s3:GetObject", "s3:PutObject", "s3:ListBucket"]
      Resource = [
        aws_s3_bucket.sensor_archive.arn,
        "${aws_s3_bucket.sensor_archive.arn}/*"
      ]
    }]
  })
}

output "bucket_name" {
  value = aws_s3_bucket.sensor_archive.bucket
}
```

A role has **two** policies, and they answer different questions:

| Policy | Question it answers | Here |
|---|---|---|
| **Trust policy** (`assume_role_policy`) | *Who* may put this role on? | Containers run by AWS ECS, the managed container service Riverstone deploys to (section 52.8) |
| **Permission policy** (`aws_iam_role_policy`) | *What* may the role do, once on? | Section 52.1's three actions, on this one bucket |

- **`jsonencode({ ... })`** turns an HCL map into JSON text. Read it as "write this out as the JSON policy of section 52.1": `Version`, `Statement`, `Effect`, `Action`, `Resource` are the same fields.
- **`Principal = { Service = "ecs-tasks.amazonaws.com" }`** is the **principal**, who is trusted: the ECS service, starting a container. On Kubernetes on AWS (EKS), the trust policy would name the cluster's identity provider instead.
- **`Action = "sts:AssumeRole"`** is the permission to put the role on. **STS** (Security Token Service) is the part of AWS that hands out temporary credentials.
- **`role = aws_iam_role.pipeline_role.id`** attaches the permission policy to the role above. **`aws_s3_bucket.sensor_archive.arn`** is the bucket's ARN, which AWS assigns when it creates the bucket; the reference fills it in.
- **`output "bucket_name"`** prints the created bucket's name after `apply`, so other configurations (or a human) can use it without hunting through a console.

### Checking it, for real

Terraform checks its own files without a cloud account. In a terminal, in `work/ch52/terraform`:

<!-- run: none -->
```
# terminal
$ terraform init -backend=false
$ terraform fmt -check
$ terraform validate
Success! The configuration is valid.
```

- **`terraform init`** prepares the folder. It downloads the AWS provider into a hidden `.terraform/` folder, printing `Installing hashicorp/aws v6.66.0...` (or a newer 6.x), and records the exact version and its checksums in `.terraform.lock.hcl`, which you do commit, so everyone gets the same provider. It ends with `Terraform has been successfully initialized!`. **`-backend=false`** skips connecting to the state bucket, which you don't have yet. Without it, `init` would try to reach S3 and stop.
- **`terraform fmt -check`** checks the layout (indentation, lined-up `=` signs) and prints nothing when it's already right. Without `-check`, `fmt` fixes the layout for you.
- **`terraform validate`** checks that every block, setting, and reference is valid for this provider version: a misspelled setting or a reference to a resource that doesn't exist fails here.

The same file, read into Python:

```python
import hcl2

with open("terraform/main.tf") as f:
    cfg = hcl2.load(f)
print("top-level blocks:", list(cfg.keys()))
print("resources:", [list(r.keys())[0].strip('"') for r in cfg["resource"]])
print("variables:", [list(v.keys())[0].strip('"') for v in cfg["variable"]])
print("outputs  :", [list(o.keys())[0].strip('"') for o in cfg["output"]])
```

```
top-level blocks: ['terraform', 'provider', 'variable', 'resource', 'output', '__comments__']
resources: ['aws_s3_bucket', 'aws_s3_bucket_versioning', 'aws_s3_bucket_lifecycle_configuration', 'aws_iam_role', 'aws_iam_role_policy']
variables: ['aws_region', 'environment']
outputs  : ['bucket_name']
```

- `hcl2.load(f)` reads the file into dictionaries: one key per block type, each holding a list of blocks.
- `cfg["resource"]` is a list of one-key dictionaries, `{'"aws_s3_bucket"': {...}}`. `list(r.keys())[0]` takes the key. The parser keeps the quotation marks from `resource "aws_s3_bucket"`, so `.strip('"')` removes them.
- `__comments__` is the parser keeping the file's comments. Ignore it.

**Reading it.** Five resources, two variables, one output: the configuration you just read, part by part.

### Plan, apply, and why review matters

- **`terraform plan`** shows what would change, without changing anything. Reading a plan carefully, especially any line that destroys something, is the single habit that prevents most infrastructure incidents. `terraform plan -out=plan.tfplan` saves the plan, and `terraform apply plan.tfplan` then does exactly what was reviewed, nothing more.
- **`terraform apply`** makes the change, after showing the plan and asking for confirmation (or automatically in CI, once a plan has been reviewed).
- **State** must be stored somewhere shared and locked (the `backend` block above), not on a laptop, or two people running Terraform at once can corrupt each other's changes.
- **Every change goes through a pull request** (Chapter 26), reviewed like any other code change, precisely because "it's just infrastructure" is how the closing story in this chapter goes wrong.

### Reading a plan

`terraform plan` compares the configuration with the state and with what really exists, and prints what it would do. This plan is real: for resources that don't exist yet, Terraform needs to ask AWS nothing, so it was run with no account at all. Here are the first lines of its 130, one resource, and the last line:

<!-- run: none -->
```
Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_s3_bucket_versioning.sensor_archive will be created
  + resource "aws_s3_bucket_versioning" "sensor_archive" {
      + bucket = (known after apply)
      + id     = (known after apply)
      + region = "ap-south-1"

      + versioning_configuration {
          + mfa_delete = (known after apply)
          + status     = "Enabled"
        }
    }

Plan: 5 to add, 0 to change, 0 to destroy.
```

- **`+`** means create. The other symbols are **`~`** update in place, **`-`** destroy, and **`-/+`** destroy and create again (replace), for a change that can't be made in place.
- **`(known after apply)`** is a value AWS decides when it creates the resource, such as the bucket's ID.
- **`Plan: 5 to add, 0 to change, 0 to destroy.`** is the summary. **Read the whole plan anyway**: the summary tells you *that* something will be destroyed, not *what*.

### Practice: what a destroy looks like

The companion's `terraform_practice/main.tf` uses `terraform_data`, a resource built into Terraform that creates nothing outside it, so it needs no provider download and no cloud account. Its two resources stand in for two firewall rules. In `work/ch52/terraform_practice`, run `terraform init`, then `terraform apply` and type `yes`. Then delete the second resource block, `rule_pipeline_to_database`, from `main.tf`, and plan again. This is the whole plan, apart from its closing note.

<!-- run: none -->
```
# terminal
$ terraform plan
terraform_data.rule_https_from_internet: Refreshing state... [id=1bf20d3e-1853-90ca-7e0d-5d31525208f5]
terraform_data.rule_pipeline_to_database: Refreshing state... [id=bc1847c9-674b-e6ff-747b-39b57bf3b9b9]

Terraform used the selected providers to generate the following execution
plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # terraform_data.rule_pipeline_to_database will be destroyed
  # (because terraform_data.rule_pipeline_to_database is not in configuration)
  - resource "terraform_data" "rule_pipeline_to_database" {
      - id     = "bc1847c9-674b-e6ff-747b-39b57bf3b9b9" -> null
      - input  = "allow 5432 from the pipeline to the database" -> null
      - output = "allow 5432 from the pipeline to the database" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.
```

(The plan ends with a note about saving it with `-out`; see below. Your IDs will differ.) **Reading it.** Terraform wants to destroy the rule **because it is not in configuration**: to Terraform, the file is the truth, and anything it manages that the file no longer mentions should go. Keep that sentence in mind for this chapter's closing story. `terraform destroy` removes everything a configuration created; run it here to clean up.

> **Simplification note.** `main.tf` passes `terraform validate`, and its plan is real, but it has never been applied to a real AWS account in producing this book. It creates the storage and the identity; the rest of a deployment, such as the container registry, the ECS cluster, the task definition that tells ECS how to run the image, and the 6:30 schedule, would be more resources in the same style. Treat it as a correct starting point to adapt, not as a file to copy and apply unread.

---

## 52.5 CI/CD

**Continuous integration** runs checks (tests, linting) automatically on every change. **Continuous deployment** (or delivery) takes a change that passes those checks and ships it, automatically or with one approval. Together, **CI/CD** is what makes "every change is reviewed and tested before it reaches production" true by construction, rather than by everyone remembering to do it.

Chapter 26 (section 26.8) built a one-job check with **GitHub Actions**. Here's a three-job workflow for Riverstone's pipeline, `.github/workflows/deploy.yml`. GitHub runs workflows only from the `.github/workflows/` folder of a repository.

```yaml
name: Riverstone pipeline CI/CD

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: actions/setup-python@v7
        with:
          python-version: "3.14"
      - run: python -m pip install -r pipeline_image/requirements.txt pytest
      - run: python -m pytest tests/

  build-and-push:
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
      - uses: aws-actions/configure-aws-credentials@v6
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ap-south-1
      - id: ecr
        uses: aws-actions/amazon-ecr-login@v2
      - name: Build and push the image
        env:
          IMAGE: ${{ steps.ecr.outputs.registry }}/riverstone/pipeline:${{ github.sha }}
        run: |
          docker build -t "$IMAGE" pipeline_image/
          docker push "$IMAGE"

  deploy:
    needs: build-and-push
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: aws-actions/configure-aws-credentials@v6
        with:
          role-to-assume: ${{ secrets.AWS_DEPLOY_ROLE_ARN }}
          aws-region: ap-south-1
      - id: ecr
        uses: aws-actions/amazon-ecr-login@v2
      - id: render
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition-family: riverstone-daily-flash
          container-name: pipeline
          image: ${{ steps.ecr.outputs.registry }}/riverstone/pipeline:${{ github.sha }}
      - uses: aws-actions/amazon-ecs-deploy-task-definition@v2
        with:
          task-definition: ${{ steps.render.outputs.task-definition }}
```

**Line by line, the parts Chapter 26 didn't cover.**

| Line | What it means |
|---|---|
| `on: pull_request: branches: [main]` | Run for a pull request whose **target** is `main`, whatever branch it comes from. |
| `on: push: branches: [main]` | Run when commits land on `main`, which is what merging a pull request does. |
| `permissions: id-token: write` | Lets the workflow ask GitHub for a signed statement of which repository and branch it is: the key to the passwordless AWS login below. `contents: read` lets it read the code and nothing more. |
| `test:` | Installs the pipeline's packages plus pytest and runs the tests in `tests/`, the tests Chapter 29 (section 29.7) taught you to write. |
| `needs: test` | This job waits for `test` and runs only if it succeeded. |
| `if: github.event_name == 'push' && ...` | A condition. `github.event_name` is what started the workflow (`push` or `pull_request`); `github.ref` is the branch, written `refs/heads/main`. `&&` means both must be true. Values inside `${{ ... }}`, and conditions in `if:`, are GitHub's **expressions**, worked out before the job starts. |
| `uses: aws-actions/configure-aws-credentials@v6` | A prepared action from AWS, pinned to major version 6, as Chapter 26 pinned its actions. With `role-to-assume`, it logs in to AWS by **OpenID Connect (OIDC)**: GitHub vouches for the workflow, and AWS hands back temporary credentials for the named role. No AWS password is stored anywhere. `with:` passes the action its settings. |
| `${{ secrets.AWS_DEPLOY_ROLE_ARN }}` | Reads a repository **secret**, which you add on GitHub under the repository's Settings, *Secrets and variables*, *Actions*. GitHub stores it encrypted and hides it in logs (section 52.6). This one holds the ARN of a deploy role, with its own trust and permission policies, set up once in Terraform. |
| `id: ecr` and `uses: aws-actions/amazon-ecr-login@v2` | Logs Docker in to **ECR**, AWS's private image registry. Without a login, `docker push` is refused. `id: ecr` names the step so later steps can read its **outputs**: `steps.ecr.outputs.registry` is the registry's address. |
| `env: IMAGE: ...` | An environment variable for this step: the full image name, registry plus `riverstone/pipeline`, tagged with `github.sha`, the commit's ID, so every image says exactly which code it holds. |
| `run: \|` | The `\|` lets `run:` hold several lines, one command each: build the image, then push it to the registry. |
| `environment: production` | Ties the job to a GitHub **environment** called `production`, which can require a named person's approval before the job runs. |
| `amazon-ecs-render-task-definition@v1` | Fetches the current **task definition**, ECS's recipe for running the container (image, memory, the role from section 52.4), for the family `riverstone-daily-flash`, and writes a copy with the new image in it. |
| `amazon-ecs-deploy-task-definition@v2` | Registers that copy as a new revision. Given no ECS service to update, it only registers, which is what a scheduled task needs. |

**Not executed here.** `build-and-push` and `deploy` need an AWS account, a registry, and the ECS resources, so they're shown as GitHub Actions would run them. The daily schedule that starts the task at 6:30 (on AWS, an EventBridge Scheduler schedule) is set up once, like the bucket; whether it picks up a newly registered revision by itself depends on how the schedule names the task definition, so check your scheduler's documentation and write the answer into your runbook (Project, step 8). The file was checked with actionlint, a checker for workflow files, which reported no problems.

### Working out exactly what runs, for real

Reading a workflow file and knowing what it will actually do for a given event is a skill worth having independently of any specific tool. `simulate_workflow.py` applies the workflow's own rules in Python. Its core is two functions:

<!-- run: none -->
```python
def matches_trigger(workflow, event_name, branch):
    on = workflow.get(True) or workflow.get("on")   # PyYAML can read a bare 'on:' as True
    if event_name not in on:
        return False
    branches = (on[event_name] or {}).get("branches")
    return not branches or branch in branches

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
```

- **`matches_trigger`** looks the event up in the `on:` block, then checks the branch against its `branches:` list, if there is one. YAML treats the bare word `on` as "true", so PyYAML may store the key as `True`, which is why the first line tries both.
- **`jobs_that_run`** goes through the jobs in order. A job runs if every job it `needs` runs and its `if:` condition is true. `eval_if` (in the file) handles the two tests this workflow uses, on `github.event_name` and `github.ref`, joined by `&&`.
- It deliberately **doesn't** model the rest of GitHub's rules: path filters, tags, manual runs (`workflow_dispatch`), schedules, or a job that fails. It answers one question, "which jobs would start?", for this kind of workflow.

```python
from simulate_workflow import load_workflow, jobs_that_run

wf = load_workflow(".github/workflows/deploy.yml")
cases = [
    ("pull_request", "main", "a pull request targeting main"),
    ("push", "main", "a direct push to main"),
    ("push", "develop", "a push to a branch other than main"),
]
for event, branch, description in cases:
    print(f"{description:<38} -> {jobs_that_run(wf, event, branch)}")
```

```
a pull request targeting main          -> ['test']
a direct push to main                  -> ['test', 'build-and-push', 'deploy']
a push to a branch other than main     -> []
```

**Reading it, and why each result is correct.**

- **A pull request targeting main** triggers the workflow (the `pull_request` rule matches), so `test` runs. `build-and-push` has `if: github.event_name == 'push' && ...`, which is false for a pull request, so it, and `deploy` after it, don't run. This is exactly right: **you want tests to run on every proposed change, and deployment to happen only once it's merged.**
- **A direct push to main** matches the `push` trigger, `test` runs, its condition is satisfied so `build-and-push` runs, and `deploy`'s condition is satisfied too: all three run in order, because `needs:` makes each wait for the one before it to succeed.
- **A push to any other branch** matches nothing in the `on:` block at all: the workflow doesn't start.

**Try the test job for real.** Copy `.github/workflows/deploy.yml`, `pipeline_image/`, and a `tests/` folder with at least one pytest test into your Chapter 26 repository, push a branch, and open a pull request to `main`. The **Actions** tab shows the workflow: `test` runs and should pass, and the other two jobs show as skipped, exactly as the simulation said. (Merging would then start `build-and-push`, which fails at the AWS login without an account. That's expected.)

### What good CI/CD adds beyond "it runs"

- **Fail fast, fail clearly.** A failed test should stop the pipeline from deploying, with a message that says what broke, not a general failure.
- **Environments with protection rules.** The `environment: production` line can require a named approver before that job runs, which is where a human checkpoint belongs for the highest-stakes step.
- **Rollback is a redeploy, not a rescue mission.** Every image is tagged with its commit (`${{ github.sha }}`), so rolling back is deploying the previous commit's image, a normal, tested action rather than an emergency improvisation.

---

## 52.6 Secrets, done properly

Chapter 45 said tokens don't belong in code. Here's the full version of where they do belong, tying together everything this chapter has built:

| Layer | Where the secret lives | Not here |
|---|---|---|
| **Local development** | A `.env` file, listed in `.gitignore` and `.dockerignore`, never committed | Hardcoded in a script |
| **Docker and Docker Compose** | Passed in when the container starts (`--env-file .env`, or `${VARIABLE}` in the Compose file) | Baked into the image with `ENV` or `COPY` |
| **Kubernetes** | A Secret object (better: sealed or provider-managed, since raw Secrets are only base64-encoded) | A ConfigMap, or committed YAML |
| **CI/CD** | The platform's own encrypted secrets store (GitHub Actions secrets, and similar in every CI tool), or no secret at all, with OIDC | A workflow file, even a private one |
| **Cloud infrastructure** | A managed secrets service (AWS Secrets Manager, Azure Key Vault, Google Secret Manager) | A Terraform variable's default value, or the state file in Git |

The common failure across every layer is the same: a secret that was "just for testing" ends up committed to Git, and Git remembers everything, including in a repository's history, forever, even after the file is deleted. **Rotate a leaked credential immediately, and treat "leaked to the wrong channel" the same as "leaked publicly."** Chapter 47's incident process (section 47.8) applies directly: detect, classify severity, contain by rotating, fix, review.

---

## 52.7 Cost

Chapter 49 estimated the sensor archive's storage cost. Compute, and how you run it, changes the total more than storage usually does. Price the pipeline's container on **AWS Fargate** in Mumbai, which bills for the CPU and memory a container reserves, for as long as it runs:

```python
FARGATE_VCPU_HOUR = 0.04256    # $ per vCPU per hour: AWS price list, Asia Pacific (Mumbai), checked 29 Sep 2026
FARGATE_GB_HOUR = 0.004655     # $ per GB of memory per hour, same source
price_per_hour = 0.5 * FARGATE_VCPU_HOUR + 1 * FARGATE_GB_HOUR    # half a vCPU and 1 GB
print(f"${price_per_hour:.4f} an hour")
```

```
$0.0259 an hour
```

- A **vCPU** is one virtual CPU core. The container is sized like section 52.3's requests: half a core (`0.5`) and 1 GB of memory (`1`).
- By hand: 0.5 × 0.04256 = 0.02128, plus 0.004655, is 0.025935, about 2.6 cents an hour.

Now run it two ways: always on, or only for the hour or so a day the pipeline needs (generously; the Flash itself takes a minute or two). **Before you run it, predict** the ratio between the two.

```python
HOURS_PER_MONTH = 730                              # 24 × 365 ÷ 12
always_on = price_per_hour * HOURS_PER_MONTH
scheduled = price_per_hour * 30                    # about an hour a day
print(f"always on : ${always_on:.2f} a month")
print(f"scheduled : ${scheduled:.2f} a month")
print(f"ratio     : {always_on / scheduled:.1f} times")
```

```
always on : $18.93 a month
scheduled : $0.78 a month
ratio     : 24.3 times
```

- By hand: 0.025935 × 730 = 18.93; × 30 = 0.78; and the ratio is simply 730 ÷ 30 = 24.3, whatever the price.

Add Chapter 49's storage. Chapter 49 priced S3 in AWS's US East region, at $0.023 per GB-month; in Mumbai, where section 52.4 puts the bucket, S3 Standard lists at $0.025 for the first 50 TB (AWS price list, checked 29 September 2026):

```python
S3_GB_MONTH = 0.025
storage = 277 * S3_GB_MONTH                        # Chapter 49's rollout archive: 277 GB
total = storage + scheduled
print(f"storage : ${storage:.2f} a month")
print(f"compute : ${scheduled:.2f} a month")
print(f"total   : ${total:.2f} a month")
```

```
storage : $6.93 a month
compute : $0.78 a month
total   : $7.70 a month
```

**Reading it.** A container running around the clock costs about **24 times more** than the same container running only when the pipeline needs it. This is the same lesson as Chapter 49's storage-scanning arithmetic, applied to compute: **the cheapest infrastructure decision is usually "don't run it when nothing needs it,"** not a smaller container. Scheduled or serverless compute (a container that starts on a trigger and stops when it's done, Chapter 46's job model exactly) is very often the right default for a batch pipeline. An always-on service is for things that must answer requests at any moment, though even a webhook receiver (Chapter 51) can be serverless (section 52.8), paying per request rather than per hour.

**And the platform has a price too.** A managed Kubernetes cluster charges for itself, before it runs anything:

```python
EKS_CLUSTER_HOUR = 0.10        # $ per cluster per hour: AWS price list, Mumbai, checked 29 Sep 2026
cluster = EKS_CLUSTER_HOUR * HOURS_PER_MONTH
print(f"cluster fee alone           : ${cluster:.2f} a month")
print(f"the same job on Kubernetes  : ${cluster + scheduled + storage:.2f} a month")
print(f"always on, 2 copies, on K8s : ${cluster + 2 * always_on + storage:.2f} a month")
```

```
cluster fee alone           : $73.00 a month
the same job on Kubernetes  : $80.70 a month
always on, 2 copies, on K8s : $117.79 a month
```

**Reading it.** Total estimate for Riverstone's pipeline and its sensor archive, run as a scheduled container: **about $8 a month**. The same job on managed Kubernetes costs about ten times as much, and an always-on pipeline in two copies there about fifteen times as much: the price of the platform, not the pipeline. It's a small number for a real reason: most of what this book has built runs briefly, once a day, on a modest amount of data. That won't stay true forever, and knowing how to estimate it, rather than guessing, is what lets you notice when it stops being true.

> **Simplification note.** These are list prices for Linux containers on x86 processors, before taxes, free tiers, or discounts, and they change; check your provider's price page or calculator before relying on them. The estimate also leaves out small items such as the container registry's storage and log storage, and the one-minute minimum Fargate bills for each run.

---

## 52.8 Choosing a deployment target

| Option | Service level | Fits | Operational cost |
|---|---|---|---|
| **A single managed container service** (AWS ECS on Fargate, AWS App Runner, Google Cloud Run, Azure Container Apps) | PaaS | One or a few independent services, including scheduled jobs, like Riverstone's pipeline today | Very low: little to configure, scales automatically within limits |
| **A managed orchestrator** (AWS ECS with several services, Google Cloud Run for services with more control) | PaaS | A handful of services that need to talk to each other, without full Kubernetes complexity | Low to moderate |
| **Managed Kubernetes** (EKS, GKE, AKS) | PaaS for the cluster's control, IaaS-like for its nodes | Many services, teams, and workloads sharing a platform | Moderate to high: someone has to own cluster upgrades, networking, and access |
| **Self-managed Kubernetes** on virtual servers | IaaS | Rarely justified below significant scale, or strict on-premises requirements | High: you own everything a managed service would have handled |
| **Serverless functions** (AWS Lambda, Google Cloud Functions) | FaaS (functions as a service), a form of PaaS | Short, event-triggered tasks (a webhook receiver, a small transform) | Very low, pay-per-invocation |

For Riverstone today, one scheduled container on a managed container service is the right size: on AWS, an ECS task on Fargate, started at 6:30 India time, using the role from section 52.4 and the image the CI/CD workflow in section 52.5 builds and registers. It costs a few dollars a month (section 52.7) and needs nobody dedicated to operating it. The Kubernetes files in section 52.3 are worth having written and understood, because the vocabulary is universal and the day this company runs ten services instead of one, the migration is a known, well-trodden path rather than a redesign from nothing.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Granting broad access "for now" | Permissions nobody remembers to remove | Scope access narrowly from the start (52.1) |
| A security group open to the whole internet | Anyone can reach a database or pipeline | Allow only the specific source that needs it (52.1) |
| Copying application code before installing dependencies in a Dockerfile | Every build reinstalls everything, even for a one-line code change | Copy dependency files first, install, then copy code (52.2) |
| Running a container process as root | A vulnerability inside the container has full control of it | Create and switch to a non-root user (52.2) |
| No `.dockerignore` | `.env`, with its passwords, is copied into the image | List `.env` and data folders in `.dockerignore` (52.2) |
| `depends_on` without a health check | The pipeline starts before the database accepts connections, and fails on its first connection | `condition: service_healthy` and a `healthcheck` (52.2) |
| Running a scheduler in several replicas | The job runs once per copy: two Flashes every morning | A CronJob or a platform schedule for batch jobs; replicas only for services with no state of their own (52.3) |
| A readiness probe on a path the application doesn't serve | The Pod never receives traffic, or the probe proves nothing | Probe a path the application actually serves for that purpose (52.3) |
| Reaching for Kubernetes for one service | Complexity with nothing to show for it | Use it when several services need scheduling together (52.3, 52.8) |
| Clicking through a console instead of writing IaC | Nobody can reproduce what exists, or review a change before it happens | Terraform (or equivalent), reviewed like code (52.4) |
| Applying Terraform without reading the plan | An unexpected `destroy` runs in production | Read every plan; treat `-` lines as a stop sign (52.4) |
| Storing Terraform state on a laptop, or in Git | Two people's changes corrupt each other; secrets in the state leak | Shared, locked, encrypted remote state (52.4) |
| Secrets in a committed file, "just this once" | The credential is in Git history forever, even after deletion | A secrets store at every layer (52.6); rotate immediately if it happens |
| Running compute around the clock for a job that runs once a day | A bill many times larger than necessary | Scheduled or serverless compute for batch work (52.7) |
| No environment protection on the deploy step | A merge to main ships straight to production with no checkpoint | Required approval on the production environment (52.5) |

---

## In the real world: the afternoon the warehouse went dark

Riverstone's contract data engineer was cleaning up the Terraform for the pipeline's network, and removed one security group rule he believed unused. He ran `terraform apply`, saw the familiar list of small changes, and confirmed it without reading past the first few lines.

The plan had listed that removal, and, further down, a second one: a rule a previous engineer had added by hand in the cloud console months earlier. Terraform managed the security group's whole list of rules, so a rule that wasn't in the file looked exactly like a rule that shouldn't exist, and the plan said it would delete it, on a line nobody had scrolled down to see. That second rule was the one letting the pipeline reach the database.

Twenty minutes later, Meera couldn't load the sales dashboard, and the morning's Flash hadn't been sent. Restoring the rule took ten minutes once the cause was found, and finding the cause took two hours, because nothing had logged **why** connectivity had disappeared, only that it had.

The fixes were the ones this chapter has built toward. Every resource that existed was **imported** into Terraform, so the file and reality agreed completely, with no manual console changes left unrecorded anywhere. Every `apply` after that went through a pull request, with the **plan's full output posted for review**, not just a summary. And a Chapter 47-style check was added: a scheduled test that tries a real database connection from a throwaway container and alerts within minutes if it fails, rather than waiting for a missed report to be the first sign.

At the retrospective, the engineer made the point himself before anyone else needed to. "The plan told me exactly what was about to happen. I didn't read it, because it looked routine."

**What made this work.**

- **The cause was a gap between reality and the code describing it** (people call it **drift**), not a bug in Terraform, which did precisely what it was told.
- **Reading the plan is the review step**, and skipping it is the same mistake as merging code no one looked at.
- **Importing everything into code** closed the gap for good, rather than patching this one incident.
- **A synthetic connectivity check** meant the next version of this failure would be caught in minutes, not discovered by a missing report.

---

## Project: deploy Riverstone's pipeline

**Goal:** a complete, reviewed deployment package for the Chapter 46 pipeline: a container image you have built and run, a Compose file for local development, orchestration files, infrastructure as code, and a CI/CD workflow, checked as far as a laptop allows, with an honest runbook for what remains to actually deploy it.

### Tools you'll need

- **Python 3.14** in the book's virtual environment, with `pyyaml`, `python-hcl2`, and `dockerfile-parse` (section 52.0).
- **Docker** Desktop or Docker Engine, with Compose (section 52.2).
- **Terraform** (section 52.4), or OpenTofu.
- **Your Chapter 26 GitHub repository**, for the workflow's test job.
- **Optional:** kind and kubectl, to try section 52.3 on your laptop.
- **The Chapter 52 companion folder** (`companion/ch52/`), copied to `work/ch52` (section 52.0), and your Chapter 46 practice folder, `work/ch46`, with PostgreSQL, the practice source, and the practice CRM API as in Chapter 46.
- **Versions used for the outputs shown:** Python 3.11.15 for the notebook cells (the outputs are the same on 3.14), PyYAML 6.0.3, python-hcl2 8.1.4, dockerfile-parse 2.0.1; Docker 29.3.1 with Compose 5.1.1; the image's Python 3.14 with Dagster 1.13.23; Terraform 1.16.4 with the AWS provider 6.66.0; PostgreSQL 16.

**Option A: Riverstone.** Extend the companion files.

**Option B: your own project.** Any application you've built in this book, containerized the same way.

**Steps**

1. **Write a Dockerfile** for a pipeline of your choice, ordered for caching, running as a non-root user, with a `.dockerignore` and no secrets baked in. Check it with `dockerfile-parse`, then build it and run it until it produces its output.
2. **Write a docker-compose.yml** for local development, with secrets from `.env` and a health check on the database. Check it with PyYAML, run it with `docker compose up -d`, and stop it with `docker compose down`.
3. **Write a Kubernetes CronJob** for the same job, and write down, in your own words, what would happen if its Pod crashed halfway through, and why a Deployment with two replicas would be wrong for it.
4. **Write a small Terraform configuration** for one piece of infrastructure your project needs (storage, a role, a network rule). Run `terraform init -backend=false`, `fmt`, and `validate`, and write the IAM policy with the narrowest permissions you can justify.
5. **Write a CI/CD workflow** with at least a test job and a deploy job gated on the test passing and the branch being `main`. Simulate its trigger logic in Python for three events, as this chapter did, and run the test job for real in your Chapter 26 repository.
6. **Write your secrets plan**: where each secret lives at each layer, referencing section 52.6's table.
7. **Estimate the monthly cost** of running it, using section 52.7's approach with your provider's current prices, and compare an always-on option with a scheduled one.
8. **Write the deployment runbook**: the exact steps a person would follow to deploy this for real, including what they'd check in the Terraform plan before approving it, how the schedule finds the newest image, and what they'd do if the deploy step failed.

**Stretch goals**

- Run section 52.3's CronJob in a kind cluster, and start one run with `kubectl create job --from=cronjob/...`.
- If you have a free-tier cloud account, apply the Terraform configuration to a throwaway project and destroy it afterward, reading every line of both plans.
- Add a synthetic health check to your CI/CD workflow, in the style of this chapter's closing story.

---

## Recap

- **IaaS, PaaS, and SaaS** rent you progressively more, and leave you progressively less to manage.
- **Regions and availability zones** are about geography and independence; spread anything critical across at least two zones.
- The **shared responsibility model** moves its line with what you rent, but your data, who can access it, and how you configure the service are always yours.
- **Least privilege** IAM: a role with a trust policy (who may use it) and a permission policy (what it may do), scoped to one resource.
- **CIDR arithmetic** by hand: a `/16` VPC split into `/24` subnets gives 2⁸ = 256 subnets of 256 addresses, 251 usable under AWS's rule.
- **Containers** package an application with everything it needs; **Dockerfiles** should install dependencies before copying code, keep secrets out with `.dockerignore`, and run as a non-root user. You built one and ran Chapter 46's Flash in it.
- **Docker Compose** runs a small stack; a health check makes the pipeline wait until its database is ready.
- **Kubernetes** objects (CronJob, Deployment, Service, Secret) solve scheduling, healing, and networking for many services. Batch jobs are CronJobs; replicas are for services with no state of their own.
- **Infrastructure as Code**, checked with `validate` and read with `terraform plan` before every `apply`, makes infrastructure reviewable, versioned, and reproducible; anything the file doesn't mention, Terraform plans to destroy.
- **CI/CD** runs tests on every change and deploys only what passes; a workflow's trigger and `if` conditions can be traced precisely, as this chapter did.
- **Secrets** belong in a dedicated store at every layer, never in code, images, or committed files, and a leak anywhere means an immediate rotation.
- **Compute cost is dominated by whether something runs when nothing needs it**: the same container cost about 24 times more running constantly than running on Riverstone's actual schedule, and a Kubernetes cluster costs more than the whole pipeline.
- **Choose the simplest deployment target that fits today's number of services**, and treat Kubernetes as a destination to grow into, not a default to start with.

---

## Key terms

IaaS · PaaS · SaaS · region · availability zone · shared responsibility model · IAM (identity and access management) · identity · role · temporary credentials · policy · statement · ARN · least privilege · trust policy · permission policy · VPC (virtual private cloud) · subnet · CIDR notation · load balancer · security group · container · image · registry · tag · Docker · Dockerfile · build context · layer · build cache · `.dockerignore` · volume · exit code · Docker Compose · health check · Kubernetes · cluster · node · Pod · Job · CronJob · Deployment · replica · label and selector · Service · readiness probe · liveness probe · Secret (Kubernetes) · namespace · manifest · resource requests and limits · Infrastructure as Code (IaC) · Terraform · HCL · provider · state file · backend · plan · apply · drift · CI/CD · continuous integration · continuous deployment · GitHub Actions · workflow trigger · job · OIDC · secrets manager · serverless · managed container service

*(All terms are defined in the Glossary, Appendix A.)*

---

## Check yourself

- [ ] You can say what IaaS, PaaS, and SaaS rent you, and where the shared responsibility line falls for each.
- [ ] You can explain regions and availability zones in your own words.
- [ ] You can read an IAM policy field by field, and write one that grants the narrowest access a task needs.
- [ ] You can compute how many usable addresses a given CIDR range provides, and split a VPC into subnets by hand.
- [ ] You can explain why containers solve "it works on my machine", and the difference between an image and a container.
- [ ] You can write a Dockerfile ordered for caching, running as a non-root user, then build and run it.
- [ ] You can run a two-container stack with Docker Compose that waits for its database to be ready.
- [ ] You can read a Kubernetes CronJob, Deployment, and Service and say what each line does, and say which one a batch job needs.
- [ ] You can check a Terraform configuration with `validate`, and read a plan's `+`, `~`, `-`, and `-/+` lines.
- [ ] You can trace exactly which jobs in a CI/CD workflow run for a given event, using its actual trigger and `if` conditions.
- [ ] You can name where a secret should live at every layer, from a laptop to production.
- [ ] You can estimate the cost difference between always-on and scheduled compute.
- [ ] You can recommend a deployment target for a company of a given size, and say when Kubernetes earns its complexity.

---

## Exercises

### Warm-up

1. A cloud provider's storage bucket is left publicly readable by mistake. Whose responsibility is that under the shared responsibility model, and why?
2. A VPC is `10.20.0.0/16`. How many total addresses does it contain, and how many `/24` subnets can it be split into?
3. In a Dockerfile, which should come first: `COPY requirements.txt .` and `RUN pip install`, or `COPY . .` (copying all the application code)? Explain why in terms of build caching.

### Core

4. A `/24` subnet is created for a database that will only ever need 40 addresses. Using the reservation rule from section 52.1, how many usable addresses does it actually get, and what does that suggest about right-sizing a subnet?
5. Using this chapter's CI/CD workflow, trace what happens for a pull request from a feature branch targeting a branch called `develop` (not `main`). Which jobs run, and why?
6. Explain the difference between a Kubernetes `resources.requests` value and a `resources.limits` value, using the CronJob's CPU values (`250m` requested, `1` as the limit) as your example.
7. The Terraform example in section 52.4 grants the pipeline's role `s3:GetObject`, `s3:PutObject`, and `s3:ListBucket` on one bucket. Using section 52.1's least-privilege rule, explain why `s3:DeleteObject` and access to other buckets are deliberately left out.
8. A container costs $0.05 an hour. Its job runs for about 2 hours a day. Using the cost model in section 52.7, calculate its monthly cost always on and scheduled, the ratio between them, and explain in one sentence why the ratio is smaller than section 52.7's 24.3.
9. In the closing story, `terraform plan` correctly showed the security group rule as something to be destroyed, and the engineer still caused an outage. What does this tell you about the limits of tooling alone, and what process change actually fixed it?

### Stretch

10. Design the IAM setup for a second pipeline that needs to read from the sensor archive bucket but must never be able to write to it. Write the policy statement's `Action` and `Resource` fields the way section 52.4 did, and explain what would go wrong if you granted it the existing role instead of a new one.
11. Riverstone's pipeline grows from one service to four: ingestion, the Dagster web interface, a webhook receiver from Chapter 51, and a small internal dashboard. Using section 52.8, make the case for moving to a managed orchestrator or Kubernetes at this point, and say what you'd want to see before agreeing.
12. Write a GitHub Actions workflow (or extend this chapter's one) that adds a `staging` deployment on every push to a `staging` branch, separate from the existing `production` deployment on `main`. Trace, as this chapter did, which jobs would run for a push to `staging`.

### Think about it (no code needed)

13. "Faking output would be worse than saying so plainly." Explain why a book that claims to have run code it hasn't would be more damaging to a reader than one that clearly labels what wasn't executed, using an example from earlier in this book (Chapter 46) if it helps.
14. A colleague argues that since the cloud is so cheap for a company Riverstone's size (a few dollars a month), cost discipline doesn't matter yet and can wait until the company is bigger. Argue against that position using this chapter's ideas.

---

## Answers

**1.** It's the **customer's** responsibility. Under the shared responsibility model, the provider secures the underlying infrastructure and, for a managed storage service, the software of the service itself, but **configuration of that service**, including who can read a bucket, is squarely the customer's job at every service level. "Your data, who can access it, and how you configure the service are always yours" draws the line exactly here.

**2.** A `/16` has 32 − 16 = 16 bits free, so 2¹⁶ = **65,536** total addresses. Splitting into `/24` subnets uses 24 − 16 = 8 more bits per subnet, so 2⁸ = **256** subnets.

**3.** **`COPY requirements.txt .` and `RUN pip install` should come first.** Docker caches each instruction's result and reuses it if nothing that affects it has changed. If `COPY . .` (all the code) came first, then editing any single application file would invalidate that layer and every layer after it, forcing a full dependency reinstall on every code change. Installing dependencies from a separate, rarely-changing file first means that layer stays cached across nearly every rebuild, as the `CACHED` lines in section 52.2 showed.

**4.** The subnet still gets a full `/24` of 256 addresses, minus AWS's 5 reserved addresses, leaving **251 usable addresses**, of which only 40 will ever be used. This suggests the subnet is oversized for its purpose: a smaller `/26` (64 addresses, 59 usable after reservations; 60 on Google Cloud) would comfortably fit 40 hosts with room to grow, leaving far more of the address space free for other subnets rather than reserving a needlessly large range for a small, fixed need.

**5.** **Nothing runs.** The workflow's `on:` block only triggers on `pull_request` targeting `main` and `push` to `main`. A pull request targeting `develop` doesn't match the `pull_request` trigger's `branches: [main]` restriction at all, so the workflow never starts, and none of `test`, `build-and-push`, or `deploy` run.

**6.** **`requests`** is what Kubernetes guarantees will be available to the container and uses when deciding which node to schedule it on: `250m` means a quarter of one CPU core is reserved for it. **`limits`** is the ceiling the container is never allowed to exceed: `1` means it can burst up to a full core under load, but no further, even if more is available on the node. A container using more than its request but less than its limit is normal; one hitting its limit gets throttled (for CPU) or killed and restarted (for memory).

**7.** Granting only `GetObject`, `PutObject`, and `ListBucket` on this one bucket means the role can read and write sensor data and see what's in the bucket, which is everything the pipeline actually does. Leaving out `s3:DeleteObject` means a bug in the pipeline, or a compromised credential, **cannot delete data**; it can still overwrite a file, but with the bucket's versioning (also in this configuration) the previous version is kept, which makes accidental or malicious data loss far harder. Leaving out access to other buckets means even a fully compromised pipeline credential can't touch Riverstone's other cloud storage, containing the blast radius of any single failure to exactly the one resource that needed access, which is least privilege in practice, not just in principle.

**8.** Always on: 0.05 × 730 = **$36.50** a month. Scheduled: 2 hours × 30 days = 60 hours, × 0.05 = **$3.00** a month. The ratio is 730 ÷ 60 ≈ **12.2 times**. It's smaller than 24.3 because the job itself runs twice as long each day, so there are half as many idle hours to stop paying for: the ratio depends only on how many of the month's 730 hours the job actually needs, not on the price.

**9.** It shows that **tooling correctly informing you is not the same as the information being acted on**: `terraform plan` did exactly its job, and the outage still happened, because the output wasn't read carefully. The process change that actually fixed it wasn't a better tool, it was **making the plan's full output part of a reviewed pull request**, so a second person, not under the time pressure of "just tidying up," had a chance to notice the destructive line before it was applied. Importing the hand-made rule into Terraform closed the drift that caused the surprise in the first place. Tools reduce the chance of an unreviewed mistake; only a review step catches the mistake a tool correctly reported and a person missed.

**10.** A sample policy statement: `Action = ["s3:GetObject", "s3:ListBucket"]`, `Resource = [aws_s3_bucket.sensor_archive.arn, "${aws_s3_bucket.sensor_archive.arn}/*"]`, attached to a separate `aws_iam_role` from the existing pipeline role, with its own trust policy. Granting the **existing** role instead would give this new, read-only pipeline the same `PutObject` write access as the original pipeline, which violates least privilege for no reason: if this second pipeline is ever compromised or has a bug, it would be able to write or corrupt data it was only ever supposed to read, an entirely avoidable risk once you've noticed it needs a distinct, narrower role.

**11.** The case for moving up: with **four services** that need independent scaling, restarting, and internal networking (the dashboard talking to the pipeline's data, say), a single managed container service starts to mean four separate deployments to coordinate by hand, with no shared service discovery, health checking, or rollout strategy between them, exactly the coordination problem Kubernetes (or a lighter managed orchestrator like ECS with several services) exists to solve. Before agreeing, you'd want to see: that the four services genuinely need to talk to each other (if they're fully independent, four separate simple deployments may still be simpler than one shared platform); that someone is willing to own cluster upgrades and access control ongoing, not just the initial setup; and a cost comparison, since a managed cluster has a baseline cost of its own ($73 a month for the EKS control plane alone in section 52.7, before any work runs), which only pays off once the coordination problem is real. You'd also check which services keep state: the webhook receiver and the Dagster web interface would need their state moved to a shared database before running in more than one copy.

**12.** A sample extension adds `staging` to both `branches:` lists in `on:`, and a new job, `deploy-staging`, with `if: github.event_name == 'push' && github.ref == 'refs/heads/staging'`, its own build step (or a `build-and-push` whose `if:` accepts both branches), and its own `environment: staging` with protection rules suited to a lower-stakes environment (perhaps no required approval, unlike production). Tracing a push to `staging`: the `push` trigger now matches, so `test` runs (it has no `if:`), and only the staging jobs satisfy their `if` conditions, while the production `build-and-push` and `deploy` jobs, still conditioned on `refs/heads/main`, correctly don't run. Without adding `staging` to `on:`, nothing would run at all, as in Exercise 5.

**13.** A book that quietly presents fabricated output as if it were real teaches the reader a false picture of what actually happens when code runs, which is far worse than a gap honestly marked, because the reader has no way to know which parts to distrust. Chapter 46 marked its `run_failure_sensor` and Airflow examples as not executed, precisely so a reader building on this book's examples knows exactly which parts have been proven to work as shown and which are correct-looking illustrations still needing their own testing in a real environment. This chapter did the same for its Kubernetes steps and the AWS jobs of its workflow. Once a single fabricated output is discovered, a reader reasonably starts doubting every other output in the book, even the ones that were genuinely verified, which destroys far more trust than the honest gap ever would.

**14.** Three things from this chapter argue against waiting. First, **habits formed on a small bill are the habits that scale**: a team that never learns to distinguish always-on from scheduled compute, or to read a cost estimate before deploying, doesn't suddenly develop that discipline when the bill crosses some threshold, they carry the same unexamined choices into a much larger number. Second, the **24-times cost difference** in section 52.7 between always-on and scheduled compute is a *ratio*, not an absolute; it applies exactly as much at Riverstone's current scale as it will at ten times the scale, and the sooner the right default is in place, the more total waste is avoided across the company's whole future, not just today's few dollars. The platform choice matters the same way: the same job on a Kubernetes cluster cost about ten times as much. Third, cost estimation is itself a skill, exactly like the reconciliation habits Chapter 47 taught for data: the point of estimating early isn't the money saved on a small bill, it's building the muscle of noticing *when something has stopped being small*, which only works if you've been checking all along, not starting the habit the day the number becomes alarming.

---

## Where this leads

- **Chapter 65, FinOps: The Economics of Data Platforms,** returns to cost management at the level of an entire organization's cloud spend.
- **Chapter 64, Security, Privacy, Governance & Responsible AI,** builds on the shared responsibility model and least-privilege access from section 52.1.
- **Chapter 60, Designing Whole Systems,** returns to choosing platforms at the whole-company scale that section 52.8 only began; **Chapter 63, Automation Architecture & Governance,** to which tool runs which automation.
- **Chapter 46**'s pipeline, **Chapter 47**'s checks, **Chapter 49**'s storage, **Chapter 50**'s streaming jobs, and **Chapter 51**'s syncs are all things this chapter's infrastructure would actually run.
- **Part 8:** cloud, containers, and deployment questions appear in the data engineering interview chapters, and the system design cases in Chapter 77, section 77.7, ask how you'd run and monitor a pipeline end to end.
