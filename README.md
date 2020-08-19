# wanem-shell
A basic shell replacement for basic wan emulator functions for CGX POC


# Karls WAN EMULATOR Shell
 Used for POC Labs to give End-Users a simple
 shell to manipulate wan emulation LQM Metrics
 This is a simple wrapper for TC QDISC

### Command examples

   Show current LQM Stats for all branches
   show

   Show current LQM Stats for all branch2
   show br2

   Set Latency on Branch 1 INET2 to 50ms, Jitter to 20ms, loss to 0 percent
   set br1 inet2 50 20 0

   Set Latency on Branch2 mpls to 5ms, Jitter to 2ms, loss to 5 percent
   set br2 inet2 5 2 5

