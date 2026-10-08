"""S3 bucket inventory -> CSV.

Handles pagination and large buckets; output columns:
key, size_bytes, storage_class, last_modified, etag
"""
import argparse
import csv

import boto3


def inventory_bucket(bucket: str, prefix: str = "", out: str = "inventory.csv") -> int:
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    count = 0
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["key", "size_bytes", "storage_class", "last_modified", "etag"])
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            for obj in page.get("Contents", []):
                w.writerow([
                    obj["Key"],
                    obj["Size"],
                    obj.get("StorageClass", "STANDARD"),
                    obj["LastModified"].isoformat(),
                    obj["ETag"].strip('"'),
                ])
                count += 1
    return count


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--bucket", required=True)
    p.add_argument("--prefix", default="")
    p.add_argument("--out", default="inventory.csv")
    args = p.parse_args()
    n = inventory_bucket(args.bucket, args.prefix, args.out)
    print(f"wrote {n} objects to {args.out}")


if __name__ == "__main__":
    main()
