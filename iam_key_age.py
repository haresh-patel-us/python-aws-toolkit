"""IAM access-key age check.

Flags users whose active access keys are older than the threshold —
a standard credential-hygiene control.
"""
import argparse
from datetime import datetime, timezone

import boto3


def old_keys(max_age_days: int):
    iam = boto3.client("iam")
    now = datetime.now(timezone.utc)
    flagged = []
    for user in iam.list_users()["Users"]:
        name = user["UserName"]
        for key in iam.list_access_keys(UserName=name)["AccessKeyMetadata"]:
            if key["Status"] != "Active":
                continue
            age = (now - key["CreateDate"]).days
            if age > max_age_days:
                flagged.append({
                    "user": name,
                    "key_id": key["AccessKeyId"][-4:],  # last 4 only — never print full keys
                    "age_days": age,
                })
    return flagged


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--max-age-days", type=int, default=90)
    args = p.parse_args()
    for f in old_keys(args.max_age_days):
        print(f"user={f['user']} key=...{f['key_id']} age={f['age_days']}d")
    print("done")


if __name__ == "__main__":
    main()
