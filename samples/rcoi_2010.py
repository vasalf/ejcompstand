#!/usr/bin/python3

duration = int(input())
n = int(input())
m = int(input())

ok = [False for i in range(n)]
tries = [0 for i in range(n)]
time = [-1 for i in range(n)]

times_of_tries = [[] for i in range(n)]

for i in range(m):
    prob, status, submit_time = map(int, input().split())
    if submit_time > 120:
        submit_time -= 45
    prob -= 1
    if submit_time < duration:
        if status == 0:
            ok[prob] = True
            if time[prob] == -1 or submit_time < time[prob]:
                time[prob] = submit_time
        else:
            times_of_tries[prob].append(submit_time)

for i in range(n):
    if ok[i]:
        times_of_tries[i].sort()
        j = 0
        while j < len(times_of_tries[i]) and times_of_tries[i][j] <= time[i]:
            j += 1
        tries[i] = j
    else:
        tries[i] = len(times_of_tries[i])
        if tries[i] > 0:
            time[i] = times_of_tries[i][-1]

for i in range(n):
    print(int(not ok[i]), tries[i], time[i])

total_time = 0
for i in range(n):
    if ok[i]:
        total_time += tries[i] * 20 + time[i]

print(total_time)
