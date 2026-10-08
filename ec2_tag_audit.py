"""EC2 tag-compliance audit across regions.

Reports instances missing any of the required tags. Exit code 1 when
violations are found so CI/scheduled jobs can alert on it.
"""
import argparse
import sys

import boto3

REQUIRED_TAGS = {"Owner", "Environment"}


def audit_region(region: str):
    ec2 = boto3.client("ec2", region_name=region)
    paginator = ec2.get_paginator("describe_instances")
    violations = []
    for page in paginator.paginate():
        for res in page["Reservations"]:
            for inst in res["Instances"]:
                tags = {t["Key"] for t in inst.get("Tags", [])}
                missing = REQUIRED_TAGS - tags
                if missing:
                    violations.append({
                        "region": region,
                        "instance_id": inst["InstanceId"],
                        "state": inst["State"]["Name"],
                        "missing_tags": sorted(missing),
                    })
    return violations


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--regions", nargs="+", default=["us-east-1"])
    p.add_argument("--required-tags", nargs="*", default=sorted(REQUIRED_TAGS))
    args = p.parse_args()

    global REQUIRED_TAGS
    REQUIRED_TAGS = set(args.required_tags)

    all_violations = []
    for region in args.regions:
        all_violations.extend(audit_region(region))

    for v in all_violations:
        print(f"{v['region']:>12} {v['instance_id']:<20} {v['state']:<10} missing={','.join(v['missing_tags'])}")

    print(f"\n{len(all_violations)} instance(s) out of tag compliance")
    sys.exit(1 if all_violations else 0)


if __name__ == "__main__":
    main()
