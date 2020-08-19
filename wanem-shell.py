#!/usr/bin/python3

####### Karls WAN EMULATOR Shell #######
### Used for POC Labs to give End-Users a simple
### shell to manipulate wan emulation LQM Metrics
### This is a simple wrapper for TC QDISC
import os

### Command examples
#
#   Show current LQM Stats for all branches
#   show
#
#   Show current LQM Stats for all branch2
#   show br2
#
#   Set Latency on Branch 1 INET2 to 50ms, Jitter to 20ms, loss to 0 percent
#   set br1 inet2 50 20 0
#
#   Set Latency on Branch2 mpls to 5ms, Jitter to 2ms, loss to 5 percent
#   set br2 inet2 5 2 5
#
#
verbs = {
'br1' : { 'inet1': 'eth-inet.15', 'inet2': 'eth-inet.16', 'mpls': 'eth-mpls.17', },
'br2' : { 'inet1': 'eth-inet.25', 'inet2': 'eth-inet.26', 'mpls': 'eth-mpls.27', },
'dc1' : { 'inet1': 'eth-inet.55', 'inet2': 'eth-inet.56', 'mpls': 'eth-mpls.57', },
'dc2' : { 'inet1': 'eth-inet.65', 'inet2': 'eth-inet.66', 'mpls': 'eth-mpls.67', },
}

readline = ""
while readline.lower() != "exit":
    readline = input("wanem> ").lower()
    readline = readline.strip()
    if readline == "show":
        for site in verbs:
            for interface in verbs[site]:
                command = "sudo tc qdisc show dev " + verbs[site][interface]
                output = os.popen(command).read().strip()
                outsplit = output.split()
                if ('delay' in outsplit) and ('loss' in outsplit):
                    print("Interface",site,interface) 
                    latency = outsplit[outsplit.index("delay") + 1]
                    latency = latency.replace("ms","")
                    jitter = outsplit[outsplit.index("delay") + 2]
                    jitter = jitter.replace("ms","")
                    loss = outsplit[outsplit.index("loss") + 1]
                    loss = loss.replace("%","")
                    
                    print("  Latency(ms) :",latency)
                    print("  Jitter(ms)  :",jitter)
                    print("  Loss(%)     :",loss)          
                    
                else:
                    latency = "UNCONFIGURED"
                    loss = "UNCONFIGURED"
                    jitter = "UNCONFIGURED"
                    print("Interface",site,interface) 
                    print("  Latency(ms) :",latency)
                    print("  Jitter(ms)  :",jitter)
                    print("  Loss(%)     :",loss)    
    elif readline.startswith("show"):
        splitlines = readline.split()
        if len(splitlines) != 2:
            print("Usage: show                  Shows all site config")
            print("       show [sitename]       Shows config for specific site")
        else:
            if splitlines[1] in verbs.keys():
                site = splitlines[1]
                for interface in verbs[site]:
                    command = "sudo tc qdisc show dev " + verbs[site][interface]
                    output = os.popen(command).read().strip()
                    outsplit = output.split()
                    if ('delay' in outsplit) and ('loss' in outsplit):
                        print("Interface",site,interface) 
                        latency = outsplit[outsplit.index("delay") + 1]
                        latency = latency.replace("ms","")
                        jitter = outsplit[outsplit.index("delay") + 2]
                        jitter = jitter.replace("ms","")
                        loss = outsplit[outsplit.index("loss") + 1]
                        loss = loss.replace("%","")
                        
                        print("  Latency(ms) :",latency)
                        print("  Jitter(ms)  :",jitter)
                        print("  Loss(%)     :",loss)           
                            
                    else:
                        latency = "UNCONFIGURED"
                        loss = "UNCONFIGURED"
                        jitter = "UNCONFIGURED"
                        print("Interface",site,interface) 
                        print("  Latency(ms) :",latency)
                        print("  Jitter(ms)  :",jitter)
                        print("  Loss(%)     :",loss)    
            else:
                print("Error! Site not found")
    elif readline.startswith("set"):
        splitlines = readline.split()
        if len(splitlines) != 6:
            print("Usage: set [site] [interface] [latency] [jitter] [loss]      Set LQM for a branch")
            print()
        else:
            site        = splitlines[1]
            interface   = splitlines[2]
            latency     = splitlines[3] + "ms"
            jitter      = splitlines[4] + "ms"
            loss        = splitlines[5] + "%"
            
            print("Attempting to change interface",site,interface) 
            print("  Latency(ms) :",latency)
            print("  Jitter(ms)  :",jitter)
            print("  Loss(%)     :",loss)    

            # Add NETEM in case the interface is unconfigured
            command = "sudo tc qdisc add dev " + verbs[site][interface] + " root netem 2>&1"
            output = os.popen(command).read().strip()

            #set latency both add and change just in case its unconfigured
            command_set = "sudo tc qdisc change dev " + verbs[site][interface] + " root netem delay " + latency + " " + jitter + " 25% " + " loss " + loss + " 25%"
            output = os.popen(command_set).read().strip()

            #Show changed output
            command = "sudo tc qdisc show dev " + verbs[site][interface]
            output = os.popen(command).read().strip()
            outsplit = output.split()
            if ('delay' in outsplit) and ('loss' in outsplit):
                print("New interface config for",site,interface) 
                latency = outsplit[outsplit.index("delay") + 1]
                latency = latency.replace("ms","")
                jitter = outsplit[outsplit.index("delay") + 2]
                jitter = jitter.replace("ms","")
                loss = outsplit[outsplit.index("loss") + 1]
                loss = loss.replace("%","")
                
                print("  Latency(ms) :",latency + "ms")
                print("  Jitter(ms)  :",jitter + "ms")
                print("  Loss(%)     :",loss + "%") 
                print()
            else:
                print("Unknown error making change. Did you set the inputs correctly? (Note if deconfiguring interfaces to 0, this is normal)")
                print("Command Attempted:",command_set)
                print()
    elif (readline.strip() == ""):
        pass
    elif (readline.strip() == "exit"):
        pass
    else:    
        print("Valid verbs: [show, set, help]")
        print("EXAMPLES")
        print()
        print(" Show current LQM Stats for all branches")
        print(" wanem> show")
        print()
        print(" Show current LQM Stats for branch1")
        print(" wanem> show br1")
        print()
        print(" Set Latency on Branch 1 INET2 to 50ms, Jitter to 20ms, loss to 0 percent")
        print(" wanem> set br1 inet2 50 20 0")
        print()
        print(" Set Latency on Branch2 mpls to 5ms, Jitter to 2ms, loss to 5 percent")
        print(" wanem> set br2 mpls 5 2 5")
        print()
        print(" Set Latency on DC1 inet1 to 0ms, Jitter to 0ms, loss to 0 percent")
        print(" wanem> set dc1 inet1 0 0 0")
        print()
