# INET4031 – Add Users Script

## Program Description
This Python script automates the process of adding multiple Linux user accounts and assigning them to groups on an Ubuntu system. Normally, a system administrator would have to manually run commands like `adduser`, `passwd`, and `adduser <user> <group>` for each new account. This program reads a colon-delimited input file and uses those same commands automatically for each user, saving time and reducing mistakes.

## Program User Operation

### Input File Format
Each non-comment line in the input file contains **5 colon-delimited fields** in this order:

```

username:password:last:first:group1,group2

```

**Rules:**
- Lines starting with `#` are comments and are **skipped** by the program.
- Each line must have **exactly 5 fields**. Lines with missing fields are ignored.
- Use `-` in the groups field if you don’t want the user added to any groups.
- You can list multiple groups separated by commas (e.g., `group01,group02`).

**Example Input File:**
```

user04:pass04:Last04:First04:group01
user05:pass05:Last05:First05:group02
user06:pass06:Last06:First06:group01,group02
user07:pass07:Last07:First07:-
#user08:pass08:Last08:First08:group01
user09:Last09:First09:group09

````

### Command Execution
Before running the program, make sure it’s executable:
```bash
chmod +x create-users.py
````

To run the script and actually create the users:

```bash
sudo ./create-users.py < create-users.input
```

This script will:

1. Create a new Linux user account using `adduser --disabled-password --gecos`.
2. Set the password for that user automatically using `passwd`.
3. Add the user to any specified secondary groups using `adduser <user> <group>`.

You’ll see printed messages showing what the script is doing at each step.

### “Dry Run” Mode

Before making any real changes, you can test the code by doing a **dry run**.
Leave all the `os.system(cmd)` lines **commented out**, and then run:

```bash
./create-users.py < create-users.input
```

This will only print the commands that *would* be run, without creating users or changing anything on the system.

After verifying that everything looks correct, **uncomment** the `os.system(cmd)` lines to perform a real run.

### Verification

Once the script has been run for real, verify that the users and groups were created successfully:

```bash
grep user0 /etc/passwd
grep user0 /etc/group
```

**Expected Results:**

* `/etc/passwd` should show the new user accounts with their information.
* `/etc/group` should show the appropriate group memberships for those users.

### Notes

* Requires Python 3 (`#!/usr/bin/python3` at the top of the file).
* Designed for Ubuntu or Debian systems that use `adduser` and `passwd`.
* Make sure any groups referenced in the input file (like `group01`, `group02`) already exist on the system before running the script.
* Always perform a dry run before a real run to verify that the script works as expected.

````

---

**Usage:**
```bash
cd ~/inet_4031_adduser_script
nano README.md
# Paste everything above
# Then press Ctrl+O, Enter, Ctrl+X to save and exit
git add README.md
git commit -m "Add full README.md for user creation automation script"
git push
````
