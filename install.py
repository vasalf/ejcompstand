#!/usr/bin/python3

from install_vars import *
import os

os.system("mkdir -p " + prefix + "/share/ejcompstand")
os.system("mkdir -p " + var_dir)
os.system("mkdir -p " + http_htdocs_dir + "/ejcompstand")

os.system("cp ejcompstand.py " + prefix + "/bin/ejcompstand")
os.system("cp ejcompstand.css " + prefix + "/share/ejcompstand/ejcompstand.css")
os.system("cp hatching.png " + prefix + "/share/ejcompstand/hatching.png")
os.system("cp ejcompstand.yml " + var_dir + "/ejcompstand.yml")
os.system("cp -R scripts/ " + var_dir + "/")
os.system("chmod +x " + var_dir + "/scripts/*")

os.system("ln -s " + prefix + "/share/ejcompstand/* " + http_htdocs_dir + "/ejcompstand/")
os.system("ln -s " + var_dir + "/ " + http_htdocs_dir + "/ejcompstand/conf")
os.system("ln -s " + prefix + "/bin/ejcompstand " + http_cgi_dir + "/ejcompstand")

