#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#              Copyright 2017 Hiranmoy Basak
#
#                  All Rights Reserved.
#
#                  THIS WORK CONTAINS
#       PROPRIETARY INFORMATION WHICH Is THE PROPERTY
#            OF HIRANMOY BASAK OR ITS LICENSOR
#            AND IS SUBJECT TO LICENSE TERMS.
#
#*****************************************************************/
#
#
# WARRANTY:
# Use all material in this file at your own risk. Hiranmoy Basak.
# makes no claims about any material contained in this file.
#
# Author: Hiranmoy Basak (hiranmoy.iitkgp@gmail.com)



import os
import sys
import time
import datetime
import json

from urllib import urlopen



gRigName = "-"
gGpuNotHashing = 0
gLogFile = "/home/ethos/gpu_crash.log"



# ================================   functions  =============================
def DumpActivity(dumpStr):
  print dumpStr

  try:
    pLogFile = open(gLogFile, "a")
    pLogFile.write("%s @ %s\n" % (dumpStr, str(datetime.datetime.now())))
    pLogFile.close()
  except:
    print "File write error in - " + gLogFile



# ============================== process arguments ============================
def ProcessArguments():
  global gRigName

  argStr = ""

  argIdx = 0
  while (1):
    argIdx += 1
    if (argIdx >= len(sys.argv)):
      break

    arg = sys.argv[argIdx]

    if (argIdx == 1):
      gRigName = arg
    else:
      DumpActivity("invalid number of arguments, arg#0: rig name")

  DumpActivity("Rig name: " + gRigName)



# ===================================   run  ================================
ProcessArguments()

# sleep for 3 min before checking for crash
time.sleep(180)

while 1:
  url = urlopen('http://indian.ethosdistro.com/?json=yes').read()
  result = json.loads(url)

  numGpus = result["rigs"][gRigName]["gpus"]
  numRunningGpus = result["rigs"][gRigName]["miner_instance"]

  DumpActivity("Gpus: " + str(numRunningGpus) +"/" + str(numGpus))


  if (int(numRunningGpus) != int(numGpus)):
    if (gGpuNotHashing == 1):
      # reboot
      DumpActivity("Rebooting")
      os.system("sudo reboot")
    else:
      DumpActivity("One or more Gpu(s) might have crashed")
      gGpuNotHashing = 1
  else:
    gGpuNotHashing = 0


  # wait for 2 min
  time.sleep(120)
