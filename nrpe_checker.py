#!/usr/bin/python
#/usr/lib/nagios/plugins/check_nrpe -t 200 -H 192.168.2.113 -c check_mem
import sys, getopt
import os

PATH_SCRIPT = '/usr/lib/nagios/plugins/'

#PATH_SCRIPT = '/tmp/'

def destination_checker(hostname):
   destination = ''
   first, second, third, fourth = str(hostname).split('.')
   if third == '2':
      destination = 'zeus'
   elif third == '6':
      destination = 'tryton'
   else:
      destination = 'unknow'
      sys.exit(2)
   return destination

def command_parametric(destination,timeout,hostname,command):
   if destination == "zeus":
      result = (os.system(PATH_SCRIPT+"check_nrpe -t "+timeout+" -H "+hostname+" -c "+command))
   if destination == "tryton":
      #print("command: "+PATH_SCRIPT + "check_nrpe -t "+timeout+" -H tryton.geeraert.eu -c check_nrpe_proxy -a "+hostname+" "+command)
      result = (os.system(PATH_SCRIPT + "check_nrpe -t "+timeout+" -H tryton.geeraert.eu -c check_nrpe_proxy -a "+hostname+" "+command))
   return result

def main(argv):

   try:
      opts, args = getopt.getopt(argv,"hi:o:Z:H:t:c:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'nrpe_checker.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'nrpe_checker.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-t"):
         timeout_in = arg
         #print("timeout_in "+timeout_in)
      elif opt in ("-H"):
         host_in = arg
         destination_server = destination_checker(host_in)
         #print("host_in "+host_in)
      elif opt in ("-c"):
         command_in = arg
         #print("command_in "+command_in)
      elif opt in ("-Z"):
         print("test parameters")
   exit_code = command_parametric(destination_server,timeout=timeout_in,hostname=host_in,command=command_in)
   sys.exit(os.WEXITSTATUS(exit_code))

if __name__ == "__main__":
   main(sys.argv[1:])