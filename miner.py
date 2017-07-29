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
# Use all material in this file at your own risk. Hiranmoy Basak
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
gJsonSite = "-"
gDebugMode = 0
gGpuNotHashing = 0
gLogFile = "/home/ethos/gpu_crash.log"



# ================================   functions  =============================
def DumpActivity(dumpStr):
  print dumpStr

  try:
    # writes input string in a file
    pLogFile = open(gLogFile, "a")
    pLogFile.write("%s @ %s\n" % (dumpStr, str(datetime.datetime.now())))
    pLogFile.close()
  except:
    print "File write error in - " + gLogFile



# ============================== process arguments ============================
def ProcessArguments():
  # arg#0: rig name
  # arg#1: json site
  # arg#2: (optional) set debug mode
  global gRigName, gJsonSite, gDebugMode

  argStr = ""

  argIdx = 0
  while (1):
    argIdx += 1
    if (argIdx >= len(sys.argv)):
      break

    arg = sys.argv[argIdx]

    if (argIdx == 1):
      gRigName = arg
    elif(argIdx == 2):
      gJsonSite = arg
    elif(argIdx == 3):
      gDebugMode = arg
      if (str(gDebugMode) == "1"):
        DumpActivity("debug mode")

    else:
      DumpActivity("invalid number of arguments, arg#0: rig name")

  DumpActivity("Rig name: " + gRigName + ", Json: " + gJsonSite)



# ===================================   run  ================================
ProcessArguments()

while 1:
  # wait for 4 min
  time.sleep(240)

  # read site content
  try:
    url = urlopen(gJsonSite).read()
  except:
     DumpActivity("invalid url")
     continue

  # convert site content to json
  try:
    result = json.loads(url)
  except:
     DumpActivity("invalid json")
     continue

  # extract data
  try:
    numGpus = result["rigs"][gRigName]["gpus"]
    numRunningGpus = result["rigs"][gRigName]["miner_instance"]
    hashRate =  result["rigs"][gRigName]["miner_hashes"]
  except:
     DumpActivity("invalid rig name")
     continue

  if (str(gDebugMode) == "1"):
    DumpActivity("Gpus: " + str(numRunningGpus) + "/" + str(numGpus) + " - " + str(hashRate))

  # check if any gpu is down
  if (int(numRunningGpus) != int(numGpus)):
    if (gGpuNotHashing == 1):
      # reboot
      DumpActivity("Rebooting (" + str(hashRate) + ")")
      os.system("sudo reboot")
    else:
      # wait for another 2 min before rebooting
      DumpActivity("One or more Gpu(s) might have crashed")
      gGpuNotHashing = 1
  else:
    # reset reboot pending counter
    gGpuNotHashing = 0
