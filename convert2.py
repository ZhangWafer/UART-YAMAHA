import re,os

#fileName = input("请输入文件名：")
fileName="t1763r1a.net"
with open(fileName, 'r') as f:
    subject = f.read()


match = re.search(r"NumberOfNets=(?P<nets>\d+)", subject)
if match:
    result = match.group("nets")
    nets = int(result)
    print(nets)
else:
    print('文件中没有找到线路数！')
    exit()

result = re.findall(r"P\d+={.+?}", subject)
pcs = len(result)
print(pcs)
if pcs == 0:
    print('文件中没有找到 PCS 数！')
    exit()

grp = nets // pcs
print(grp)

result = re.findall(r"N\d+={(?P<num>\d+):(?P<pins>.*?),}(\((?P<base>.*?)\))?(\[(?P<list>.*?)?\])?", subject, re.DOTALL)
if nets != len(result):
    print('文件中没有找到 PCS 数！')
    exit()

result = [[item[0], item[1].replace("\n", ""), item[3]] for item in result]


#写入到文件
writefile=open('OutPut2.NET','w')
index=1

#写PIECE:1,48,2049,2087这种
maxMinList=[]
maxMinList2000=[]
for i, item in enumerate(result):
        allList = item[1].split(",")
        for item1 in allList:
            if(int(item1)<2000):
                maxMinList.append(int(item1))
            else:
                maxMinList2000.append(int(item1))
        if i%grp==grp-1:
            writefile.writelines(
                str.format("PIECE:{0},{1},{2},{3}\n", min(maxMinList), max(maxMinList), min(maxMinList2000),
                           max(maxMinList2000)))
            maxMinList = []
            maxMinList2000 = []
            twelveCount = 0

#写NET1=7这种
for item in result:
    num = int(item[0])
    writefile.writelines("NET"+str(index)+"="+str(item[1]+".\n"))
    index = index+1
    print(item)


result = re.findall(r"N\d+={(?P<num>\d+):(?P<pins>.*?),}(\((?P<base>.*?)\))?(\[(?P<list>.*?)?\])?", subject, re.DOTALL)
#写EXR4W:1,2,5,6这种
EXR4WpositionRecord=[]
sigleList=[]

#数据记录位置
for index in range(grp):
    item=result[index]
    print(len(item))
    if len(item)<6:
        EXR4WpositionRecord.append("")
        print("ss")
    else:
        allListTemp = []
        allListTemp= item[1].split(',')
        print( item[5].strip('()'))

        sigleList=item[4].strip('[]').split(")")
        EXR4WpositionRecord.append("")
        for selectedd in sigleList:
            sigleList2 = selectedd.strip(',(').split(",")
            for item in sigleList2:
                if item in allListTemp:
                    EXR4WpositionRecord[index] += str(allListTemp.index(item)) + ','
                if not item=="":
                    if item == sigleList2[-1]:
                        EXR4WpositionRecord[index] +="*"


for index in range(nets):
    item = result[index]
    contentList = item[1].split(',')  # (1,2,``全部的数字
    if EXR4WpositionRecord[index % 9]=="" :
        if len(contentList)<4:
            pass
        elif len(contentList)==4:
            if  item[4].strip('[]')=="":
                pass
            else:
                 writefile.writelines("EXR4W:" +item[1]+".\n")
    else:
        listSplit=(EXR4WpositionRecord[index % 9])[:-1].split('*')
        for index2 in range(len(listSplit)):
            listSplit2=listSplit[index2][:-1].split(",")
            Longstring=""
            for index2 in range(len(listSplit2)):
                # print(listSplit[index])
                # ssss=int(listSplit[index])
                # print(contentList[ssss])
                Longstring = Longstring+contentList[int(listSplit2[index2])]+","
            writefile.writelines("EXR4W:"+Longstring[:-1]+".\n")

writefile.writelines("%END")
   # if item[]

#else:

    #writefile.writelines("EXR4W:"+)