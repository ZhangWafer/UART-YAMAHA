import re,os

fileName = input("请输入文件名：")
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
singleEnable=False
for index in range(grp):
    selectThing = result[index]
    if not selectThing[5] =="":
        singleEnable=True

if nets != len(result):
    print('文件中没有找到 PCS 数！')
    exit()

result = [[item[0], item[1].replace("\n", ""), item[3]] for item in result]


def single(result):


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

    # 数据记录位置
    for index in range(grp):
        item = result[index]
        print(len(item))
        if len(item) < 6:
            EXR4WpositionRecord.append("")
            print("ss")
        else:
            allListTemp = []
            allListTemp = item[1].split(',')
            print(item[5].strip('()'))

            sigleList = item[4].strip('[]').split(")")
            EXR4WpositionRecord.append("")
            for selectedd in sigleList:
                sigleList2 = selectedd.strip(',(').split(",")
                for item in sigleList2:
                    if item in allListTemp:
                        EXR4WpositionRecord[index] += str(allListTemp.index(item)) + ','
                    if not item == "":
                        if item == sigleList2[-1]:
                            EXR4WpositionRecord[index] += "*"

    for index in range(nets):
        item = result[index]
        contentList = item[1].split(',')  # (1,2,``全部的数字
        if EXR4WpositionRecord[index % 9] == "":
            if len(contentList) < 4:
                pass
            elif len(contentList) == 4:
                if item[4].strip('[]') == "":
                    pass
                else:
                    writefile.writelines("EXR4W:" + item[1] + ".\n")
        else:
            listSplit = (EXR4WpositionRecord[index % 9])[:-1].split('*')
            for index2 in range(len(listSplit)):
                listSplit2 = listSplit[index2][:-1].split(",")
                Longstring = ""
                for index2 in range(len(listSplit2)):
                    # print(listSplit[index])
                    # ssss=int(listSplit[index])
                    # print(contentList[ssss])
                    Longstring = Longstring + contentList[int(listSplit2[index2])] + ","
                writefile.writelines("EXR4W:" + Longstring[:-1] + ".\n")


def double(result):
    # match = re.search(r"NumberOfNets=(?P<nets>\d+)", subject)
    # if match:
    #     result = match.group("nets")
    #     nets = int(result)
    #     print(nets)
    # else:
    #     print('文件中没有找到线路数！')
    #     exit()
    #
    # result = re.findall(r"P\d+={.+?}", subject)
    # pcs = len(result)
    # print(pcs)
    # if pcs == 0:
    #     print('文件中没有找到 PCS 数！')
    #     exit()
    #
    # grp = nets // pcs
    # print(grp)
    #
    # # result = re.findall(r"N\d+={(?P<num>\d+):(?P<pins>.*?),}(\((?P<base>.*?)\))?(\[(?P<list>.*?)?\])?", subject,
    # #                     re.DOTALL)
    # result = re.findall(r"N\d+={(?P<num>\d+):(?P<pins>.*?),}(\((?P<base>.*?)\))?", subject, re.DOTALL)
    # if nets != len(result):
    #     print('文件中没有找到 PCS 数！')
    #     exit()
    #
    # result = [[item[0], item[1].replace("\n", ""), item[3]] for item in result]

    #写入到文件
    writefile=open('OutPut.NET','w')
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
        if (num == 1) or (num % 2 == 0):
            writefile.writelines("NET"+str(index)+"="+str(item[1]+".\n"))
            index = index+1
            print(item)
        else:
            print('错误的线路' + item)

    #写EXR4W:1,2,5,6这种
    resultList=[]
    resultListIndex=0
    for item in result:
        num = int(item[0])
        if (num % 2==0):
          #  writefile.writelines("EXR4W:"+)
            itemArray = item[1].split(',')
            count=0
            count2=0
            count3=0
            print(len(item))
            if(num==4):
                writefile.writelines("EXR4W:"+str(item[1])+".\n")

            else:
                twoStrList=[]
                while count <len(itemArray)/2:
                    #两个两个地拼凑字符
                    twoStr=str.format("{0},{1}",itemArray[2*count],itemArray[2*count+1])
                    twoStrList.append(twoStr)
                    if(len(item)>=3):#判断是否有标出基点，选出前12个点
                        if(str(item[2])==twoStr):
                            resultList.append(count)#按顺序选出基点的排在队列的哪个位置
                    count = count + 1

                if(item[2]==""):
                    if(resultListIndex<len(resultList) ):
                        while count2<=len(twoStrList)-1:
                            if(twoStrList[int(resultList[resultListIndex])]!=twoStrList[count2]):#判断两个是否重复
                                #第一种情况小于
                                if int((twoStrList[int(resultList[resultListIndex])].split(","))[0])>int((twoStrList[count2].split(","))[0]):
                                    writefile.writelines("EXR4W:"+twoStrList[count2]+","+ twoStrList[int(resultList[resultListIndex])]+".\n")
                                else:
                                    writefile.writelines("EXR4W:" + twoStrList[ int(resultList[resultListIndex])] + "," +  twoStrList[count2]+ ".\n")
                            count2 = count2 + 1
                        resultListIndex=resultListIndex+1
                    else:
                        resultListIndex = 0
                        while count2 <=len(twoStrList) - 1:
                            if (twoStrList[int(resultList[resultListIndex])] != twoStrList[count2]):
                                writefile.writelines(
                                    "EXR4W:" + twoStrList[int(resultList[resultListIndex])] + "," + twoStrList[
                                        count2] + ".\n")
                            count2 = count2 + 1
                        resultListIndex = resultListIndex + 1
                else:
                    while count3<len(twoStrList):
                        if(twoStrList[count3]==item[2]):
                            count3 = count3 + 1
                            continue
                        if(int(twoStrList[count3].split(",")[0])< int(item[2].split(",")[0])):
                            writefile.writelines("EXR4W:" + twoStrList[count3] + "," + item[2] + ".\n")
                            count3 = count3 + 1
                        else:
                            writefile.writelines("EXR4W:" + item[2] + "," + twoStrList[count3] + ".\n")
                            count3 = count3 + 1

    writefile.writelines("%END")


if singleEnable is True:
    single(result)
else:
    double(result)