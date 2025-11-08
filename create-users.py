#!/usr/bin/python3

# INET4031
# Mushtaaq Farah
# November 8th, 2025
# November 8th, 2025

import os #used to execute system commands like adduser, passwd, and add to groups.
import re #used for regex to detect comment lines that begin with '#'
import sys #used to read input lines from stdin

def main():
# Process the input file line-by-line from standard input
    for line in sys.stdin:

        #Detect and skip commented lines.
	#WHY: Lines that start with '#' are intentional comments/instructions; the script shoul not try to create users for those lines.
        match = re.match("^#",line)

        #Split the current line on ':' into expected fields.
	#Expected order: username, password, last, first, groups
        fields = line.strip().split(':')

        #Validate the line before using it:
	# - Skip if it's a comment (match != None)
	# - Skip if it does not have exactly 5 fields (prevents index errors/bad data from creating partial or incorrecnt accounts).
        if match or len(fields) != 5:
            continue

        #Map fields to meaningful variables.
	#The GECOS/comment field in /etc/passwd typically stores "Full Name" and other optional values, so we format "First Last,,," like adduser expects.
        username = fields[0]
        password = fields[1]
	# fields[3] is first name, fields[2] is last name (per the assignment's file format)
        gecos = "%s %s,,," % (fields[3],fields[2])

        #Parse the secondary groups list:
	#Comma-delimited names; a single '-' means "no secondary groups".
        groups = fields[4].split(',')

        #---Create the user account (no password yet)---
        print("==> Creating account for %s..." % (username))
        #Build the adduser command:
	#--disabled-password lets us create the account first, and we set the password in the next step.
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        #print cmd
        os.system(cmd) #actually create the user account

        #---Set the user's password non-interactively---
        print("==> Setting the password for %s..." % (username))
        #This echoes the password twice (newline separate) and pipes it to passwd.
	# sudo is used because setting another user's password requires privilege.
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        #print cmd
        os.system(cmd)

	#---Add the user to each seconary group (if applicable)---
        for group in groups:
            #If groups field is '-', there are no secondary groups to add.
            if group != '-':
                print("==> Assigning %s to the %s group..." % (username,group))
		# The Debian/Ubuntu-friendly way: add an existing user to an existing group
                cmd = "/usr/sbin/adduser %s %s" % (username,group)
                #print cmd
                os.system(cmd)

if __name__ == '__main__':
    main()
