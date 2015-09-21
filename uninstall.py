#!/usr/bin/python3

from install_vars import *
import os

os.system("rm -f " + prefix + "/bin/ejcompstand")
os.system("rm -Rf " + prefix + "/share/ejcompstand")
os.system("rm -Rf " + http_htdocs_dir + "/ejcompstand")
os.system("rm -f " + http_cgi_dir + "/ejcompstand")

