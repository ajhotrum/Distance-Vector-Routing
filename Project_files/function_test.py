change = False
print(" ")

###############

messages = [{'origin': 'ATT', 'GSAT': -8, 'ATT': 0, 'UGA': -50, 'VONA': -11}, {'origin': 'GSAT', 'GSAT': 0, 'UGA': 0, 'ATT': 7, 'VZ': 5, 'VONA': -3}, {'origin': 'ATT', 'GSAT': -8, 'ATT': 0, 'UGA': -50, 'VONA': -11}, {'origin': 'GSAT', 'GSAT': 0, 'UGA': 0, 'ATT': 7, 'VZ': 5, 'VONA': -3}]
print("Messages: ",messages)

mylist = {'origin': 'UGA', 'GSAT': 50, 'UGA': 0, 'ATT': 50}
print("My List: ", mylist)
##################

incoming_links = ['ATT', 'GSAT']
name = 'UGA'


temp = []
for i in messages:
    if i not in temp:
        temp.append(i)
messages = temp


# For each message received
for msg in messages:  

    # Get the sender          
    sender = msg['origin']

    # Get the distance from current node to sender # Maybe something to check out
    sender_dist = int(mylist[sender])

    # For each node in the message 
    for node in msg:
        
        # Ignore if the node is the current node
        if node != "origin" and node != name:

            # Get the node value
            node_value = int(msg[node])

            # Get the total distance to that node
            new_dist = node_value + sender_dist 

            if node == "GSAT" or node == "ATT":
                print(node, " Value: ", node_value)  
                print("Current Distance: ", mylist[node]) 
                print("Sender: ", sender)
                print("Sender Distance: ", sender_dist)
                print("New Distance: ", new_dist)
                print(" ")
                d = input()     

            # If it is an outgoing link, keep the value the same
            #if is_ol:
            #    new_dist = int(ol_weight) + sender_dist          

            # If the node value is -99 or less, just set the new distance to -99
            if node_value == -99 or new_dist <=-99:
                new_dist = -99

            # If the node is not in the list, add it
            if node not in mylist:
                mylist[node] = new_dist
                change = True

            # If the new distance is less than what is currently stored, update the value.
            elif int(mylist[node]) > new_dist:
                mylist[node] = new_dist
                change = True
            

print("My List: ", mylist)
#if name == "VZ":
#d = input()


# Empty queue
messages = []