#!/usr/bin/python3

import sys
import os
import cgi, cgitb
import yaml
import pymysql


class Contest:
    def __init__(self, d):
        for s in d.keys():
            setattr(self, s, d[s])
        self.name = d["contest_name"]
        self.prob_num = d["prob_num"]
        self.contest_id = d["contest_id"]
        self.scoring_type = d["contest_scoring_type"]
        
    def GetRow(self, uid, mysql_con, cell_num):
        cursor = mysql_con.cursor()
        runs = cursor.execute("select prob_id, score, status from runs where user_id=" + str(user_id) + " and contest_id=" + str(self.contest_id) + ";")
        if self.scoring_type == "acm":
            s = "<tr><td>"
            s += self.name + "</td>"
            prob_num = self.prob_num
            runs = []
            for prob_id, score, status in cursor:
                runs.append((prob_id, score, status))
            ok = [False] * prob_num
            failed = [0] * prob_num
            for prob_id, score, status in runs:
                if status == 0:
                    ok[prob_id - 1] = True
                elif not ok[prob_id - 1]:
                    failed[prob_id - 1] += 1
            for i in range(prob_num):
                attr = ""
                if ok[i]:
                    t = "+"
                    attr = " class=\"ok\""
                elif failed[i]:
                    t = "-"
                    attr = " class=\"fail\""
                else:
                    t = "."
                if failed[i]:
                    t += str(failed[i])
                s += "<td" + attr + ">" + t + "</td>"
            if prob_num < cell_num:
                s += "<td colspan=" + str(cell_num - prob_num) + " class=\"disabled\"></td>"
            s += "<td class=\"sum\">" + str(sum(map(int, ok))) + "</td>"
            s += "<td>" + str(sum(failed)) + "</td>"
            s += "</tr>"
        elif self.scoring_type == "olympiad":
            s = "<tr><td>" + self.name + "</td>"
            prob_num = self.prob_num
            runs = []
            for prob_id, score, status in cursor:
                runs.append((prob_id, score, status))
            res = [0] * prob_num
            tried = [False] * prob_num
            ok = [False] * prob_num
            for prob_id, score, status in runs:
                res[prob_id - 1] = max(res[prob_id - 1], score)
                if score >= 0:
                    tried[prob_id - 1] = True
                if status == 0:
                    ok[prob_id - 1] = True
            for i in range(prob_num):
                attr = ""
                if ok[i]:
                    attr = " class=\"ok\""
                elif tried[i]:
                    attr = " class=\"fail\""
                if not(ok[i] or tried[i]):
                    s += "<td>.</td>"
                else:
                    s += "<td" + attr + ">" + str(res[i]) + "</td>"
            if prob_num < cell_num:
                s += "<td colspan=" + str(cell_num - prob_num) + " class=\"disabled\"></td>"
            s += "<td class=\"sum\">" + str(sum(res)) + "</td>"
            s += "</tr>"
        cursor.close()
        return s
        
         
class ContestGroup:
    def __init__(self, d):
        self.name = d["name"]
        self.numeration = d["prob_numeration"]
        self.contests = []
        self.prob_num = 0
        self.scoring_type = "None"
        self.sort_by = d["sort_by"] if "sort_by" in d else "name"
        for cntst in d["contests"]:
            self.contests.append(Contest(cntst))
        for cntst in self.contests:
            self.prob_num = max(self.prob_num, cntst.prob_num)
            assert self.scoring_type == "None" or self.scoring_type == cntst.scoring_type
            self.scoring_type = cntst.scoring_type
        self.contests.sort(key=lambda x: getattr(x, self.sort_by))

    def GetTable(self, uid, mysql_con):
        rows = []
        for cntst in self.contests:
            s = cntst.GetRow(uid, mysql_con, self.prob_num)
            if len(s):
                rows.append(s)
        if len(rows):
            ans = "<h1>" + self.name + "</h1>"
            ans += "<table border=1>"
            ans += "<tr><td>P</td>"
            if self.numeration == "latin":
                first = ord("A")
            else:
                first = ord("1")
            for i in range(self.prob_num):
                ans += "<td>" + chr(first + i) + "</td>"
            ans += "<td class=\"sum\">" + chr(0x03a3) + "</td>"
            if self.scoring_type == "acm":
                ans += "<td>S</td>"
            ans += "</tr>"
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

GET = parse_GET_data()
user_id = int(GET["user_id"])

if "conf" in GET:
    config_file = "../ejcompstand/" + GET["conf"]
else:
    config_file = "../ejcompstand/ejcompstand.yml"


yaml_groups = yaml.load(open(config_file, "r", encoding="utf-8"))['contest_groups']
contest_groups = list(map(lambda k: ContestGroup(yaml_groups[k]), yaml_groups.keys()))
contest_groups.sort(key=lambda x: x.name)

mysql_con = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', user='ejudge', password='ejudge', db='ejudge')

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
