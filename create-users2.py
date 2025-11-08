#!/usr/bin/python3
# INET4031 – Interactive Dry-Run version
# Author: Mushtaaq Farah
# This version adds a simple prompt to choose dry-run (Y) or real run (N).
# - Dry-run (Y): Do NOT execute OS commands. Print what would run. Also print
#   skip and bad-line messages so you can fix the input file safely.
# - Real run (N): Execute OS commands. Do NOT print skip / bad-line messages

import os
import re
import sys

# ---- Interactive dry-run prompt ----
answer = input("Dry-run mode? (Y/N): ").strip().lower()
DRY_RUN = (answer == 'y')

def run_cmd(cmd: str) -> None:
    """
    Runs or echoes a command depending on DRY_RUN.
    """
    if DRY_RUN:
        print(f"[DRY-RUN] would run: {cmd}")
    else:
        os.system(cmd)

def main():
    # Read input lines from stdin (supports: ./create-users2.py < create-users.input)
    for line in sys.stdin:
        # Ignore completely empty lines
        if not line.strip():
            continue

        # Detect commented lines: lines starting with '#'
        match = re.match(r"^#", line)

        # Split colon-delimited fields: username:password:last:first:group1,group2
        fields = line.strip().split(':')

        # --- Skip logic & validation ---
        if match:
            # In DRY-RUN, explicitly say we're skipping; in real run, stay quiet
            if DRY_RUN:
                print(f"[DRY-RUN] skipping commented line: {line.strip()}")
            continue

        if len(fields) != 5:
            # Bad/malformed line — in DRY-RUN, tell the user; in real run, just skip
            if DRY_RUN:
                print(f"[DRY-RUN][ERROR] not enough fields ({len(fields)}): {line.strip()}")
            continue

        # Map fields to variables (per the assignment’s input format)
        username = fields[0]
        password = fields[1]
        last = fields[2]
        first = fields[3]
        # GECOS/comment field in /etc/passwd commonly stores "First Last,,,"
        gecos = "%s %s,,," % (first, last)

        # Parse groups list (comma-delimited). A single '-' means no secondary groups.
        groups = [g.strip() for g in fields[4].split(',')]

        # ---- Create the user (no password yet) ----
        print(f"==> Creating account for {username}...")
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos, username)
        run_cmd(cmd)

        # ---- Set the password non-interactively ----
        print(f"==> Setting the password for {username}...")
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password, password, username)
        run_cmd(cmd)

        # ---- Add user to each secondary group (if any) ----
        for group in groups:
            if group and group != '-':
                print(f"==> Assigning {username} to the {group} group...")
                cmd = "/usr/sbin/adduser %s %s" % (username, group)
                run_cmd(cmd)

if __name__ == '__main__':
    main()

