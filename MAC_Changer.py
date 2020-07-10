#!/usr/bin/env python

import subprocess
import optparse
import random
import re           #regular expression
import sys

def getArguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="mac_address", help="New MAC address or type 'r' to get a random one")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("An interface must be specified, use --help for more info")
    if not options.mac_address:
        parser.error("Specify the Mac address you want or type 'r' to get random one")
    return options

def macChanger(interface, mac_address):
    if(mac_address == 'r'): 
        addrEnding = random.randint(10, 99)
        mac_address = '00:11:00:11:22:{}'.format(addrEnding)
        random_mac_adr_flag = True
    else:
        random_mac_adr_flag = False

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])

    return random_mac_adr_flag

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])  # this returns what commands returns

    # And now the most interseting comes i going to learn how to search for some peaces of code within large text ignoring the rest
    # RegEx - Regular Expresions

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)  # search for patern within the ifconfig_result

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not search for Mac address.")

def check_if_interface_exist(interface):
    ifconfig_result = subprocess.check_output(["ifconfig"]) #store the result from the command in the variable

    interface_search_result = re.search(r"\b" + interface, ifconfig_result) #search for pattern within the ifconfig_result

    if interface_search_result:
        return True
    else:
        return False

#######################################################################################


options = getArguments()    #getting the interface and the mac from the user

if not check_if_interface_exist(options.interface):     #if there is no such interface kill the script
    print("There is no such interface: " + options.interface)
    sys.exit()

print("The initial value of Mac address is: " + str(get_current_mac(options.interface)))    #printing the initial mac

random_mac_adr_flag = macChanger(options.interface, options.mac_address)    #Change the Mac

if not random_mac_adr_flag:         #only if the mac was not random
    if get_current_mac(options.interface) == options.mac_address: #search mac and that that what was typed by the user are the same
        print("[+] The Mac Address has been changed properly.")
    else:
        print("[-] Failed to change the Mac Address.")