#!/usr/bin/python3

import sys
import os
import cgi, cgitb
import yaml
import pymysql


class Contest:
    def __init__(self, d):
        self.name = d["contest_name"]
        self.contest_id = d["contest_id"]
        self.scoring_type = d["contest_scoring_type"]
        
    def GetRow(self, uid, mysql_con):
        cursor = mysql_con.cursor()
        runs = cursor.execute("select prob_id, score, status from runs where user_id=" + str(user_id) + " and contest_id=" + str(self.contest_id) + ";")
        if self.scoring_type == "acm":
            s = "<tr><td>"
            s += self.name + "</td>"
            prob_num = 0
            runs = []
            for prob_id, score, status in cursor:
                runs.append((prob_id, score, status))
                prob_num = max(prob_num, prob_id)
            ok = [False] * prob_num
            failed = [0] * prob_num
            for prob_id, score, status in runs:
                if status == 0:
                    ok[prob_id - 1] = True
                else:
                    failed[prob_id - 1] += 1
            for i in range(prob_num):
                attr = ""
                if ok[i]:
                    t = "+"
                    attr = " class=\"ok\""
                elif failed[i]:
                    t = "-"
                else:
                    t = "."
                if failed[i]:
                    t += str(failed[i])
                s += "<td" + attr + ">" + t + "</td>"
            s += "</tr>"
        elif self.scoring_type == "olympiad":
            s = "<tr><td>" + self.name + "</td>"
            prob_num = 0
            runs = []
            for prob_id, score, status in cursor:
                runs.append((prob_id, score, status))
                prob_num = max(prob_num, prob_id)
            res = [0] * prob_num
            tried = [False] * prob_num
            for prob_id, score, status in runs:
                res[prob_id - 1] = max(res[prob_id - 1], score)
                if score >= 0:
                    tried[prob_id - 1] = True
            for i in range(prob_num):
                attr = ""
                if res[i] == 100:
                    attr = " class=\"ok\""
                s += "<td" + attr + ">" + str(res[i]) + "</td>"
            s += "</tr>"
        cursor.close()
        return s
        
         
class ContestGroup:
    def __init__(self, d):
        self.name = d["name"]
        self.contests = []
        for cntst in d["contests"]:
            self.contests.append(Contest(cntst))

    def GetTable(self, uid, mysql_con):
        rows = []
        for cntst in self.contests:
            s = cntst.GetRow(uid, mysql_con)
            if len(s):
                rows.append(s)
        if len(rows):
            ans = "<h1>" + self.name + "</h1>"
            ans += "<table border=1>"
            ans += "".join(rows)
            ans += "</table>"
        else:
            ans = ""
        return ans


### Some stuff to get normal encoding

def enc_print(string, encoding='utf8'):
    sys.stdout.buffer.write(str(string).encode(encoding) + b'\n')

### Some stuff to get GET data in a dict

def parse_GET_data():
    args = os.getenv("QUERY_STRING").split("&")
    ans = dict()
    for s in args:
        name, value = s.split("=")
        ans[name] = value
    return ans


cgitb.enable()

yaml_groups = yaml.load(open("./ejcompstand.yml", "r"))['contest_groups']
contest_groups = list(map(lambda k: ContestGroup(yaml_groups[k]), yaml_groups.keys()))

mysql_con = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', user='ejudge', password='ejudge', db='ejudge')

GET = parse_GET_data()
user_id = int(GET["user_id"])

enc_print("Content-type: text/html; charset=UTF-8\n")
enc_print("<html>")
enc_print("<head>")
enc_print("<title> Соревнования в ejudge </title>")
enc_print("<link rel=\"stylesheet\" href=\"/ejudge/ejcompstand.css\" type=\"text/css\" />")
enc_print("</head>")
enc_print("<body>")
for group in contest_groups:
    enc_print(group.GetTable(user_id, mysql_con))
enc_print("</body>")
enc_print("</html>")
