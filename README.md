# Python AWS Toolkit

Portfolio sample: practical boto3 utilities for day-to-day AWS operations —
the kind of scripts I keep in a platform team's toolbox. Each script is
self-contained, paginates correctly, and prints machine-readable output.

## Scripts

- `s3_inventory.py` — inventory every object in a bucket (prefix, size,
  storage class, last modified) and write a CSV report
- `ec2_tag_audit.py` — scan EC2 instances across regions and report ones
  missing required tags (Owner, Environment)
- `iam_key_age.py` — list IAM users with access keys older than N days
  (credential-hygiene check I run on a schedule)

## Run

```bash
pip install -r requirements.txt
python s3_inventory.py --bucket my-bucket --out inventory.csv
python ec2_tag_audit.py --regions us-east-1 us-west-2
python iam_key_age.py --max-age-days 90
```

Credentials come from the standard boto3 chain (env vars, `~/.aws/credentials`,
or instance role) — nothing is hardcoded.
