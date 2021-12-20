# LoadBalancer

A load balancer is a device that distributes network or application traffic across a number of servers. Load balancers are used to increase capacity (concurrent users) and reliability of applications.

The Client Program receives the user’s command, then sends the command to the Load Balancer, waits for the reply, and prints the reply for the user, and wait for another command. A Client program only talks to the Load Balancer on port 8000 and does not have any information about other components of the network. User commands can be:

Library Service Registration: User can sign up for the library service of IUT by sending the character "L" followed by the student number. Example: L,9021403
Dormitory Service Registration: User can sign up for the dormitory service of IUT by sending the character "D" followed by the student number. Example: D,9021403
Pool Service Registration: User can sign up for the IUT pool by sending the character "P" followed by the student number. Example: P,9021403


• LB (Load Balancer): This is the new part of the network. A Load Balancer (LB) is a program to listen on port 8000. It constantly waits for incoming connections from CPs.
Once a CP is connected, the LB parses the request and finds out the service that student needs. Subsequently, the LB notifies the responsible Service Program (SR) and waits for the SR reply. After receiving the reply from the SR, the LB sends the reply back to the client. Pay attention to the fact that LB does not know how much does it take for a SP to handle the CP’s command, it may even take up to seconds. So, the LB should be able to work concurrently.

