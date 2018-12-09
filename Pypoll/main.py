# Modules
import csv
#import os

# open file
with open("election_data.csv", newline="") as inputcsv:
    
    csvreader = csv.reader(inputcsv, delimiter=",")

    #skip header
    next(csvreader)
    
     #initialize variables
    Vote_Count = 0
    
    #Create an dictionary 
    Candidate_dictionary = {}


    #loop thru each row of the csv
    for row in csvreader:
        Vote_Count += 1
        
        # hold candidate name
        Candidate_Name = row[2]
        # scan thru the dictionary looking for candidates
        if Candidate_Name in Candidate_dictionary:
            Candidate_dictionary[Candidate_Name] += 1
        else:
            Candidate_dictionary[Candidate_Name] = 1
   
    #end of for loop

    # Sort dictionary to find the winner
    sorted_Candidate_list = sorted(Candidate_dictionary,key=Candidate_dictionary.__getitem__,reverse=True)
    

 #Open output text file and write to text file
    with open("Output.txt","w") as text_file:
        
        #print to terminal and write to file
        print("Election Results")
        text_file.write("Election Results\n")
        print("----------------------------------")
        text_file.write("----------------------------------\n")
        print(f'Total Votes: {Vote_Count}')
        text_file.write(f'Total Votes: {Vote_Count}\n')
        print("----------------------------------")
        text_file.write("----------------------------------\n")
        #loop thru list and print each candidat's stats
        for item in sorted_Candidate_list:
            #Calculate vote percentage
            win_percentage = ((Candidate_dictionary[item] / Vote_Count) * 100)
            print(f'{item} : {win_percentage:.3f}% ({Candidate_dictionary[item]})')
            text_file.write(f'{item} : {win_percentage:.3f}% ({Candidate_dictionary[item]})\n')
        #End of loop
        print("----------------------------------")
        text_file.write("----------------------------------\n")
        print(f'Winner: {sorted_Candidate_list[0]}')
        text_file.write(f'Winner: {sorted_Candidate_list[0]}\n')
        print("----------------------------------")
        text_file.write("----------------------------------\n")

     
    
    