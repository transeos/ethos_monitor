#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#
# WARRANTY:
# Use all material in this file at your own risk. Hiranmoy Basak
# makes no claims about any material contained in this file.
#
# Contact: hiranmoy.iitkgp@gmail.com



import os
import sys
import time
import datetime
import json
import commands

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
  # arg#0: (optional) set debug mode
  global gDebugMode

  argStr = ""

  argIdx = 0
  while (1):
    argIdx += 1
    if (argIdx >= len(sys.argv)):
      break

    arg = sys.argv[argIdx]

    if (argIdx == 1):
      if (str(arg) == "-debug"):
        gDebugMode = 1
        DumpActivity("debug mode")


def GetPanelInfo():
  global gRigName, gJsonSite

  commandOutput1 = commands.getstatusoutput('\grep http /var/run/ethos/url.file')
  gJsonSite = commandOutput1[1]
  gJsonSite = gJsonSite+"/?json=yes"

  commandOutput2 = commands.getstatusoutput("grep hostname /var/run/ethos/stats.file | sed 's/.*://g'")
  gRigName = commandOutput2[1]

  DumpActivity("Rig name: " + gRigName + ", Json: " + gJsonSite)



# ===================================   run  ================================
ProcessArguments()
GetPanelInfo()

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
    status = result["rigs"][gRigName]["condition"]
  except:
    DumpActivity("invalid rig name")
    continue

  if (str(gDebugMode) == "1"):
    DumpActivity("<" + status + "> Gpus: " + str(numRunningGpus) + "/" + str(numGpus) + " - " + str(hashRate))

  if (status == "unreachable"):
    gGpuNotHashing = 0
    DumpActivity("[Warning] panel is not updating")
    continue;

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
