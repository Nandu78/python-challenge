# Modules
import csv
#import os

# open file
with open("budget_data.csv", newline="") as inputcsv:
    
    csvreader = csv.reader(inputcsv, delimiter=",")

    #skip header
    _ = next(csvreader)
    
    #initialize variables
    month_counter = 0
    net_amount = 0
    average_change = 0
    greatest_increase_in_profit = 0
    greatest_decrease_in_profit = 0


    #loop thru each row of the csv
    for row in csvreader:
        month_counter += 1
        net_amount += int(row[1])
        # save greatest increase in profit
        if int(row[1]) > greatest_increase_in_profit:
            greatest_increase_in_profit = int(row[1])
            increase_month = row[0]

        # save greatest decrease in profit
        if int(row[1]) < greatest_decrease_in_profit:
            greatest_decrease_in_profit = int(row[1])
            decrease_month = row[0]
    #end of for loop
     
    #calculate average change       
    average_change = net_amount / month_counter

    #Open output text file and write to text file
    with open("Output.txt","w") as text_file:
        text_file.write("Financial Analysis\n")
        text_file.write("----------------------------------\n" )
        text_file.write(f'Total Months: {month_counter}\n' )
        text_file.write(f'Total: ${net_amount}\n')
        text_file.write(f'Average Change: ${average_change}\n')
        text_file.write(f'Greatest Increase in Profits: {increase_month} (${greatest_increase_in_profit})\n')
        text_file.write(f'Greatest Decrease in Profits: {decrease_month} (${greatest_decrease_in_profit})\n')

    #print to terminal
    print("Financial Analysis")
    print("----------------------------------")
    print(f'Total Months: {month_counter}')
    print(f'Total: ${net_amount}')
    print(f'Average Change: ${average_change}')
    print(f'Greatest Increase in Profits: {increase_month} (${greatest_increase_in_profit})')
    print(f'Greatest Decrease in Profits: {decrease_month} (${greatest_decrease_in_profit})')
