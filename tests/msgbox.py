import time, sys, os

print                "[stdout] before messagebox"
print >> sys.stderr, "[stderr] before messagebox"
sys.stdout.flush()
sys.stderr.flush()
x = int(sys.argv[1])
if x:
    time.sleep(x)
os.system('xmessage hello')

print                "[stdout] after messagebox"
print >> sys.stderr, "[stderr] after messagebox"
