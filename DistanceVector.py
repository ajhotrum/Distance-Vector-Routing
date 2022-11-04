# Project 4 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data   
         
        # Get list of links 
        self.outgoing_links = outgoing_links
        self.incoming_links = incoming_links
        self.mylist = {self.name:0}
        self.mylist['origin'] = self.name

        # Go through each link and add weights
        for link in outgoing_links:
            self.mylist[link.name] = int(link.weight)
    

    # Method for sending initial message
    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py
        for neighbor in self.incoming_links:
            self.send_msg(self.mylist, neighbor.name)


    # Boolean method to check if a link is outgoing
    def is_outgoing_link(self, node):
        ol = False
        ol_weight = None
        # Iterate through links
        for i in range(len(self.outgoing_links)):
            if self.outgoing_links[i].name == node:
                # If outgoing, add weight
                ol = True
                ol_weight = self.outgoing_links[i].weight
        return ol, ol_weight


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages  

        # Set change flag to false.
        change = False

        # Update messages
        temp = []
        for i in self.messages:
            if i not in temp:
                temp.append(i)
        self.messages = temp

        # Iterate through messages
        for msg in self.messages:            
            
            # Get sender and distance
            sender = msg['origin']
            sender_dist = int(self.mylist[sender])
            
            # Check if outgoing link, if so get weight
            is_ol, ol_weight = self.is_outgoing_link(sender)
            if is_ol:
                sender_dist = int(ol_weight)

            # Iterate through nodes to check for changes and log distances
            for node in msg:
                if node != 'origin' and node != self.name:
                    node_value = int(msg[node])
                    new_dist = node_value + sender_dist

                    if node_value == -99 or new_dist <= -99:
                        new_dist = -99

                    if node not in self.mylist:
                        self.mylist[node] = new_dist
                        change = True

                    elif int(self.mylist[node]) > new_dist:
                        self.mylist[node] = new_dist
                        change = True
        
        # Empty queue
        self.messages = []

        # TODO 2. Send neighbors updated distances      
        if change:
            for neighbor in self.incoming_links:
                self.send_msg(self.mylist, neighbor.name)         


    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        

        res = ""
        for node, dist in self.mylist.items():
            if node != "origin" and node != 'paths':
                res += node + str(dist) + ","

        res = res[:-1]
        add_entry(self.mylist['origin'], res)        
