#!/usr/bin/python


# -*- Python -*-

#*****************************************************************
#
#              Copyright 2017 Hiranmoy Basak
#
#                  All Rights Reserved.
#
#           THIS WORK CONTAINS TRADE SECRET And
#       PROPRIETARY INFORMATION WHICH Is THE PROPERTY
#            OF HIRANMOY BASAK OR ITS LICENSOR
#            AND IS SUBJECT TO LICENSE TERMS.
#
#*****************************************************************/
#
# No part of this file may be reproduced, stored in a retrieval system,
# Or transmitted in any form Or by any means --- electronic, mechanical,
# photocopying, recording, Or otherwise --- without prior written permission
# of Hiranmoy Basak.
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

while 1:
  url = urlopen('http://indian.ethosdistro.com/?json=yes').read()
  result = json.loads(url)

  numGpus = result["rigs"][gRigName]["gpus"]
  numRunningGpus = result["rigs"][gRigName]["miner_instance"]

  DumpActivity("Gpus: " + str(numRunningGpus) +"/" + str(numGpus))


  if (numRunningGpus != numGpus):
    if (gGpuNotHashing == 1):
      # reboot
      DumpActivity("Rebooting")
      os.system("r")

    gGpuNotHashing = 1


  # wait for 2 min
  time.sleep(120)
