import sys

class Util:
    def __init__(self):
        self.id = 0
        self.at = 0
        self.bt = 0
        self.ct = 0
        self.tat = 0
        self.wt = 0

# Array to store all the process information by implementing the above Util class
ar = [Util() for _ in range(100001)]

class Util1:
    def __init__(self):
        self.p_id = 0
        self.bt1 = 0

# Segment tree array to process the queries in nlogn
tr = [Util1() for _ in range(4 * 100001 + 5)]

# To keep an account of where
# a particular process_id is
# in the segment tree base array
mp = [0] * (100001)

# Comparator function to sort the
# struct array according to arrival time

# Function to update the burst time and process id
# in the segment tree
def update(node, st, end, ind, id1, b_t):
    if st == end:
        tr[node].p_id = id1
        tr[node].bt1 = b_t
        return
    mid = (st + end) // 2
    if ind <= mid:
        update(2 * node, st, mid, ind, id1, b_t)
    else:
        update(2 * node + 1, mid + 1, end, ind, id1, b_t)
    if tr[2 * node].bt1 < tr[2 * node + 1].bt1:
        tr[node].bt1 = tr[2 * node].bt1
        tr[node].p_id = tr[2 * node].p_id
    else:
        tr[node].bt1 = tr[2 * node + 1].bt1
        tr[node].p_id = tr[2 * node + 1].p_id

# Function to return the range minimum of the burst time
# of all the arrived processes using segment tree
def query(node, st, end, lt, rt):
    range = Util1()
    if end < lt or st > rt:
        return range
    if st >= lt and end <= rt:
        return tr[node]
    mid = (st + end) // 2
    lm = query(2 * node, st, mid, lt, rt)
    rm = query(2 * node + 1, mid + 1, end, lt, rt)
    if lm.bt1 < rm.bt1:
        return lm
    return rm

# Function to perform non_preemptive
# shortest job first and return the
# completion time, turn around time and
# waiting time for the given processes
def non_preemptive_sjf(n):
    # To store the number of processes
    # that have been completed
    counter = n

    # To keep an account of the number
    # of processes that have been arrived
    upper_range = 0

    # Current running time
    tm = min(sys.maxsize, ar[upper_range + 1].at)

    # To find the list of processes whose arrival time
    # is less than or equal to the current time
    while counter != 0:
        for _ in range(upper_range + 1):
            upper_range += 1
            if ar[upper_range].at > tm or upper_range > n:
                upper_range -= 1
                break
            update(1, 1, n, upper_range, ar[upper_range].id, ar[upper_range].bt)

        # To find the minimum of all the running times
        # from the set of processes whose arrival time is
        # less than or equal to the current time
        res = query(1, 1, n, 1, upper_range)

        # Checking if the process has already been executed
        if res.bt1 != sys.maxsize:
            counter -= 1
            index = mp[res.p_id]
            tm += res.bt1

            # Calculating and updating the array with
            # the current time, turn around time and waiting time
            ar[index].ct = tm
            ar[index].tat = ar[index].ct - ar[index].at
            ar[index].wt = ar[index].tat - ar[index].bt

            # Update the process burst time with
            # infinity when the process is executed
            update(1, 1, n, index, sys.maxsize, sys.maxsize)
        else:
            tm = ar[upper_range + 1].at

# Function to call the functions and perform
# shortest job first operation
def execute(n):
    # Sort the array based on the arrival times
    ar[1:n + 1] = sorted(ar[1:n + 1], key=lambda x: (x.at, x.id))
    for i in range(1, n + 1):
        mp[ar[i].id] = i

    # Calling the function to perform non-preemptive-sjf
    non_preemptive_sjf(n)

# Function to print the required values after
# performing shortest job first
def print_result(n):
    print("ProcessId Arrival Time Burst Time" +
          " Completion Time Turn Around Time Waiting Time")
    for i in range(1, n + 1):
        print(f"{ar[i].id}\t\t{ar[i].at}\t\t{ar[i].bt}\t\t{ar[i].ct}\t\t{ar[i].tat}\t\t{ar[i].wt}")

# Driver Code
if __name__ == "__main__":
    # Number of processes
    n = 5

    # Initializing the process id
    # and burst time
    for i in range(1, 4 * 100001 + 2):
        tr[i].p_id = sys.maxsize
        tr[i].bt1 = sys.maxsize

    # Arrival time, Burst time and ID
    # of the processes on which SJF needs
    # to be performed
    ar[1].at = 1
    ar[1].bt = 7
    ar[1].id = 1

    ar[2].at = 2
    ar[2].bt = 5
    ar[2].id = 2

    ar[3].at = 3
    ar[3].bt = 1
    ar[3].id = 3

    ar[4].at = 4
    ar[4].bt = 2
    ar[4].id = 4

    ar[5].at = 5
    ar[5].bt = 8
    ar[5].id = 5

    execute(n)

    # Print the calculated time
    print_result(n)
