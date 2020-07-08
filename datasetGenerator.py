import sys
import os
import numpy as np
import random

SEPARATOR    = ","

TYPE_CLASS_A = 0
TYPE_CLASS_B = 1

def loadParametersCSVFile(filename):
    print ("loading file: ",filename)
    lines = []
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    return lines
	
def buildDictionary(lines):
    dict = {}
    for line in lines:
        line = line.replace("\n","")
        if line.startswith("Parameters"):   # Skip the header
            continue
        pos = line.find(SEPARATOR)
        
        if pos > 0:
            dict[line[:pos]] = line[pos+1:].split(SEPARATOR)
    return dict

def generateMeasure(low, high):
    return random.uniform(low, high)

def generateSingleRow(dict, type):
    measures = []
    measure = 0.0

    # Process each row of the parameter csv file
    for parameter in dict:
        # Skip the header row
        if parameter != None and parameter !="parameters":
            fields = dict[parameter]
            classA = float(fields[0])
            classA_range_low = float(fields[1].split("-")[0])
            classA_range_high = float(fields[1].split("-")[1])
            unknown_low =  float(fields[2].split("-")[0])
            unknown_high =  float(fields[2].split("-")[1])
            classB = float(fields[3])
            classB_range_low = float(fields[4].split("-")[0])
            classB_range_high = float(fields[4].split("-")[1])
            
            #print("====>",classA,classA_range_low,classA_range_high,unknown_low,unknown_high,classB,classB_range_low,classB_range_high)
            if type == TYPE_CLASS_A:
                measure = generateMeasure(unknown_high, classA * 1.3)
            elif type == TYPE_CLASS_B:
                measure = generateMeasure(classB_range_low * 0.7, unknown_low)

            measures.append(round(measure,1))

    measures.append(type)

    print("---->",measures)
    return measures

def createOutputDataset(dataset, filename):
    print("Creating output dataset",filename)
    f = open(filename,"w")
    for line in dataset:
        f.write(line+"\n")
    f.close()

def main():    
    #################################################################################
    # Load command line parameters
    #################################################################################
    parameters_csvfile = sys.argv[1]
    generated_csvfile = sys.argv[2]
    class_A_quantity = int(sys.argv[3])
    class_B_quantity = int(sys.argv[4])

    #################################################################################
    # Load input CSV parameters file
    #################################################################################
    lines = loadParametersCSVFile(parameters_csvfile)
    print("\nparameters list:\n",lines)

    #################################################################################
    # Convert the CSV into a dictionary for easier processing
    #################################################################################
    dict = buildDictionary(lines)
    print("\nparameters dictionary:\n",dict)

    quit = False
    dataset_list = []
    current_class_A = 0
    current_class_B = 0

    #################################################################################
    # Extract the header of the CSV file from dictionary
    #################################################################################    
    dataset_list.append(str(dict.keys()).replace("[","").replace("]","").replace("(","").replace(")","").replace("dict_keys","").replace("'","").replace(", ",",")+",class")

    print("\noutput dataset header:\n",dataset_list)

    #################################################################################
    # Loop until generating all requested classes in random order
    #################################################################################    
    while quit == False:
        if current_class_A < class_A_quantity and np.random.randint(2) == 1:
            row = generateSingleRow(dict,TYPE_CLASS_A)
            current_class_A += 1
            dataset_list.append(str(row).replace("[","").replace("]",""))

        if current_class_B < class_B_quantity and np.random.randint(2) == 0:
            row = generateSingleRow(dict,TYPE_CLASS_B)
            current_class_B += 1
            dataset_list.append(str(row).replace("[","").replace("]",""))

        if current_class_B >= class_B_quantity and current_class_A >= class_A_quantity:
            quit = True

    #################################################################################
    # Generate the output Dataset from the output rows list
    #################################################################################    
#   print("Rows Generated:")
#   for row in dataset_list:
#     print(row)

    createOutputDataset(dataset_list, generated_csvfile)

#################################################################################
# If insuficient parameters show command line, otherwise process the input parameters CSV file
#################################################################################    
if len(sys.argv) < 5:
    print("Sintax: datasetgenerator parameters_csvfile generated_csvfile <CLASSA quantity>  <CLASSB quantity>")
else:
    main()

