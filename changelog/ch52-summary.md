# Chapter 52 summary: The Cloud, Containers & Infrastructure as Code

**Findings:** 44 content rows (52.1–52.44) and 6 open visual rows (V52.4, V52.6, V52.10, V52.11, V52.12, V52.14). **48 Verified, 2 Fixed** (52.15 kubectl steps shown without output; 52.31 kept as one chapter), **0 left Open**.

## What changed
- **Cloud basics rebuilt for a first-time reader:** new §52.0 Setting up; §52.1 opens with IaaS/PaaS/SaaS (Ch 2's parked table, landed, with an "At Riverstone" column), an AWS-equivalents table, IAM built from zero with a JSON policy read field by field, CIDR done by hand before Python, and the corrected shared-responsibility model (the line moves; data, access and configuration never do). Figure 52.1 redrawn as an IaaS/PaaS/SaaS grid.
- **Docker is now hands-on and real:** install, `hello-world`, a new Dockerfile (Python 3.14, no apt layer thanks to psycopg2-binary, non-root user created early, `.dockerignore`), a one-shot `run_flash.py` instead of `dagster dev`, and a real container run that built the 2 January Flash (2 orders, ₹38,710.00, matching Ch 46). A real cached rebuild shows the caching lesson. Compose fixed (database name, health check, `service_healthy`) and run for real.
- **Kubernetes corrected:** the pipeline is a **CronJob** (06:30 IST, `Forbid`), not a 2-replica Deployment that would send two Flashes; a separate stateless Deployment + Service example teaches labels/selectors (new Figure 52.4), probes and ClusterIP. kubectl steps for kind are given, not executed.
- **Terraform:** four explained parts, `~> 6.0`, S3 backend with lockfile, lifecycle `filter {}` and correct noncurrent-version wording, trust vs permission policy; `init -backend=false`, `fmt`, `validate` and a real offline `plan` shown; a no-account `terraform_data` practice produces a real destroy plan that sets up the rewritten closing story.
- **CI/CD:** workflow moved to `.github/workflows/`, line-by-line table, OIDC login, ECR login, ECS task-definition deploy (one target, ECS on Fargate, across §52.3–52.8); simulator core shown.
- **Cost:** inline model with dated AWS price-list numbers (Mumbai): about **$8/month** scheduled, $18.93 always-on compute, $73 for an EKS cluster alone.
- Cross-refs fixed (Ch 65 title, Ch 60/63), prerequisites listed, Appendix G note removed, Ch 50 mentions corrected per coordinator.

## Skipped or partial, and why
- **52.31** Split into 52A/52B not done: structural decision for Abhishek. Applied the finding's fallback (one chapter, Time needed 20–26 h, K8s read-for-vocabulary).
- **52.15** No kubectl output shown: kind can't run in the book's sandbox, and outputs are never invented.
- **52.30** The Actions test job wasn't run on GitHub (no repository here); the reader is told how.
- **52.23** Optional current-data transition to cold storage not added.

## Option picks
52.8 (A) delete apt layer · 52.9 one-shot job command · 52.17 CronJob ("better") · 52.22/52.29 ECS throughout (recommended) · 52.28 ECR login (follows 52.22) · 52.31 one-chapter fallback.

## Time needed
12–16 h → **20–26 h over three to four weeks** (installs and real Docker, Compose and Terraform runs added; roughly +3 h Docker, +2 h Terraform, +2 h setup, IAM and CIDR, +1 h CI/CD).

## Verification
verify_python 15/15 outputs, 0 mismatches · all terminal outputs captured from real runs (Docker 29.3.1, Compose 5.1.1, Terraform 1.16.4, AWS provider 6.66.0) · kubeconform: 3 resources valid · actionlint: clean · checks/ch52_check.py all pass · check_code_teaching 0 flags · fig_check 0 under 7 pt · build 51 pp, layout_check clean.
