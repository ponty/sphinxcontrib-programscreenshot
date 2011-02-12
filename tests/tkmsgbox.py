from Tkinter import *
import tkMessageBox
import sys,time,logging

#logging.basicConfig(level=logging.DEBUG)

root = Tk()
root.withdraw()

print                "[stdout] before messagebox"
print >> sys.stderr ,"[stderr] before messagebox"
sys.stdout.flush()
sys.stderr.flush()
x=int(sys.argv[1])
if x:
    #logging.debug('sleeping:' + str(x))
    time.sleep(x)
tkMessageBox.showinfo(message="message")

print                "[stdout] after messagebox"
print >> sys.stderr ,"[stderr] after messagebox"
