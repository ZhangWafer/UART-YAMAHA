import re
openFile=open("OutPut.NET","r")
readfile= openFile.readlines()
strList=[]
sortList=[]
for item in readfile:
    file = re.search("NET\d+=.+?\.", item)
    if(file is None): continue
    strList.append(item)
    sortList.append(((item.split('=')[1]).split(','))[0])
    print(file)
openFile2= open("Settle.NET","w")
count=0
while count<len(sortList):
    openFile2.writelines(strList[sortList[count]])