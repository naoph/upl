#! /usr/bin/env python3

import argparse
import hashlib
import os
import subprocess

import yaml

def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("extension", nargs="?")
    args = parser.parse_args()

    # Determine remote information
    conf_file = os.path.expanduser("~/.upl.yml")
    try:
        conf = yaml.safe_load(open(conf_file).read())
        r_host = conf["hostname"]
        r_dir  = conf["uploads_directory"]
        r_pref = conf["http_prefix"]
    except:
        print("Please use this config format at ~/.upl.yml:")
        print()
        print("hostname: server.org")
        print("uploads_directory: /usr/share/nginx/uploads/")
        print("http_prefix: https://files.server.org/")
        print()
        return 1

    # Determine truncated file hash
    filehash = hashlib.sha256(open(args.file, "rb").read()).hexdigest()
    shorthash = filehash[:16]

    # Determine eventual remote extension
    if not args.extension is None:
        extension = args.extension
    else:
        extension = args.file.split(".")[-1:][0]

    # Determine eventual remote paths
    newname = "{0}.{1}".format(shorthash, extension)
    newpath = os.path.join(r_dir, newname)
    newurl = os.path.join(r_pref, newname)

    # Upload
    cmd = ["scp", args.file]
    cmd.append("{0}:{1}".format(r_host, newpath))
    subprocess.call(cmd)
    print(newurl)

    # Finish
    return 0

if __name__ == "__main__":
    main()
