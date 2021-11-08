import  csv

def write_file(politicianList):
    fileName = "SPANISH_POLITICIANS_SALARIES.csv"
    path ='../data/'
    filePath = path + fileName

    with open(filePath, 'w', newline='') as csvFile:
      writer = csv.writer(csvFile)
      for politicianData in politicianList:
          writer.writerow(politicianData)

def write_file_batch(politicianList, idx):
    fileName = "SPANISH_POLITICIANS_SALARIES" + str(idx) + ".csv"
    path ='../data/'
    filePath = path + fileName

    with open(filePath, 'w', newline='') as csvFile:
      writer = csv.writer(csvFile)
      for politicianData in politicianList:
          writer.writerow(politicianData)
