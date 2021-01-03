#Dveloped By: Luke McGlashan
#Last edit: 3/01/2021
#Description: contains functions and code needed to read a CSV file and output a data summary
#create a relevant JSON file and SQL insert statements using said CSV file

import csv
import json

#Sort data sets for easier viewing for summary
def sort_data(dataSet, length):
    sorted_devices = {}
    i = 0
    sorted_keys = sorted(dataSet, key=dataSet.get, reverse=True)
    for w in sorted_keys:
        sorted_devices[w] = dataSet[w]
        i += 1
        if i == length:
            break

    return sorted_devices

# Function to convert a CSV to JSON 
def make_JSON(csvFilePath):
    data = {}
    # Open a csv reader called DictReader 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
          
        # Convert each row into a dictionary  
        # and add it to data 
        for rows in csvReader:
            key = rows['user_pseudo_id']
            data[key] = rows

        # Open a json writer, and use the json.dumps()  
        # function to dump data
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf: 
            jsonf.write(json.dumps(data, indent=4))

        print("---JSON file has been generated--- \n\n")

# Function to convert a CSV to SQL insert statements 
def make_SQL(csvFilePath):
    data = {}
    tableName = input("Please input a name for the table: ")
    
    openFile = open(csvFilePath, 'r', encoding='utf-8')
    file = open(sqlFilePath, "w", encoding='utf-8')
    csvFile = csv.reader(openFile)
    header = next(csvFile)
    headers = map((lambda x: '`'+x+'`'), header)
    insert = 'INSERT INTO ' + tableName + ' (' + ", ".join(headers) + ")\nVALUES "
    
    for row in csvFile:
        values = map((lambda x: '"'+x+'"'), row)
        file.write(insert +"("+ ", ".join(values) +");\n\n" )
    openFile.close()
    print("---SQL insert statement file has been generated--- \n\n")

# Function to make data summary
def make_dataSummary(csvFilePath): 
    data = {}
    #Data summary data
    headers = ""
    AndroidUsers = 0
    IOSUsers = 0
    geoCountry = {}
    devices = {}
    deviceType = {}
    installSource = {}
    adTracking = {}
    languages = {}
    IOSDevices = {}
    IOSVersions = {}
    AndroidVersions = {}
    
    
    line_count = 0

    
    # Open a csv reader called DictReader 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
          
        # Convert each row into a dictionary  
        # and add it to data 
        for rows in csvReader: 
            # Select the Primary key, user_psuedo_id in this instance
            key = rows['user_pseudo_id']
            geokey = rows['geo_country']
            deviceskey = rows['device_brand_name']
            typekey = rows['device_category']
            installkey = rows['install_source']
            adkey = rows['is_limited_ad_tracking']
            languageKey = rows['device_language']
            IOSDevicesKey = rows['device_model_name']
            deviceOSKey = rows['device_os']
            versionKey = rows['device_os_version']
            data[key] = rows
            
            
            if geoCountry.get(geokey) == None:
                geoCountry[geokey] = 1
            else:
                geoCountry[geokey] += 1

            if devices.get(deviceskey) == None:
                devices[deviceskey] = 1
            else:
                devices[deviceskey] += 1

            if deviceType.get(typekey) == None:
                deviceType[typekey] = 1
            else:
                deviceType[typekey] += 1

            if installSource.get(installkey) == None:
                installSource[installkey] = 1
            else:
                installSource[installkey] += 1
            

            if adTracking.get(adkey) == None:
                adTracking[adkey] = 1
            else:
                adTracking[adkey] += 1

            if languages.get(languageKey) == None:
                languages[languageKey] = 1
            else:
                languages[languageKey] += 1
                
            if IOSDevices.get(IOSDevicesKey) == None and deviceOSKey == 'IOS':
                IOSDevices[IOSDevicesKey] = 1
            elif deviceOSKey == 'IOS':
                IOSDevices[IOSDevicesKey] += 1

            if IOSVersions.get(versionKey) == None and deviceOSKey == 'IOS':
                IOSVersions[versionKey] = 1
            elif deviceOSKey == 'IOS':
                IOSVersions[versionKey] += 1

            if AndroidVersions.get(versionKey) == None and deviceOSKey == 'ANDROID':
                AndroidVersions[versionKey] = 1
            elif deviceOSKey == 'ANDROID':
                AndroidVersions[versionKey] += 1     
            
            if deviceOSKey == 'ANDROID':
                AndroidUsers += 1
            elif deviceOSKey == 'IOS':
                IOSUsers += 1

            line_count += 1

    #Sort data summaries for clarity
    sorted_devices = sort_data(devices, 10)
    sorted_Countries = sort_data(geoCountry, 10)
    sorted_installations = sort_data(installSource, 5)
    sorted_languages = sort_data(languages, 10)
    sorted_IOSdevices = sort_data(IOSDevices, 10)
    sorted_IOSversions = sort_data(IOSVersions, 10)
    sorted_AndroidVersions = sort_data(AndroidVersions, 10)


    #Print out results  
    print(f'\nProcessed {line_count} Users.')  
    print(f'Number of IOS users: {IOSUsers}')
    print(f'Number of android users: {AndroidUsers}')
    print(f'Number of users based on device type: {deviceType}')
    getadtracking = adTracking.get('Yes')
    print(f'Most common sources of installations: \n {sorted_installations} \n')
    print(f'Top 10 device brands used: \n {sorted_devices} \n')
    print(f'Top 10 countries downloaded in: \n {sorted_Countries} \n')
    print(f'Top 10 languages: \n {sorted_languages} \n')
    print(f'Most used IOS devices (Top 10): \n {sorted_IOSdevices} \n')
    print(f'Most used IOS Versions (Top 10): \n {sorted_IOSversions} \n')
    print(f'Most used Android Versions (Top 10): \n {sorted_AndroidVersions} \n')
        
# Driver Code 
  
# File Paths
jsonFilePath = r'JSONoutput.json'
sqlFilePath = 'SQLoutput.txt'
command = ""

#Simple to use command line interface
while command != 'quit':
    print("Please type the command you wish to execute: ")
    print("json -- Creates a json file when provided an appropriate CSV file")
    print("data -- Makes a data summary of a provided CSV file")
    print("sql -- Creates an SQL file when provided an appropriate CSV file, also requires a table name")
    print("quit -- exits the program")
    command = input("Enter command: ")

    if command == 'json':
        file = input("Enter file path ")
        make_JSON(file)
    elif command == 'sql':
        file = input("Enter file path ")
        make_SQL(file)
    elif command == 'data':
        file = input("Enter file path ")
        make_dataSummary(file)
    elif command == 'quit':
        print("\n")
    else:
        print('---Invalid Command---')

print("----Ending Program----")


