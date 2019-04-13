import re


with open('T1448R1A.net', 'r') as f:
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

result = re.findall(r"N\d+={(?P<num>\d+):(?P<pins>.*?),}(\((?P<base>.*?)\))?", subject, re.DOTALL)
if nets != len(result):
    print('文件中没有找到 PCS 数！')
    exit()

result = [[item[0], item[1].replace("\n", ""), item[3]] for item in result]

#写入到文件
writefile=open('OutPut.NET','w')
index=1

#写PIECE:1,48,2049,2087这种
maxMinList=[]
maxMinList2000=[]
twelveCount=0
for item in result:
    if twelveCount < 12:

        allList = item[1].split(",")
        for item1 in allList:
            if(int(item1)<2000):
                maxMinList.append(int(item1))
            else:
                maxMinList2000.append(int(item1))

        if twelveCount==11:
            writefile.writelines(
                str.format("PIEXE:{0},{1},{2},{3}\n", min(maxMinList), max(maxMinList), min(maxMinList2000),
                           max(maxMinList2000)))
            maxMinList = []
            maxMinList2000 = []
            twelveCount = 0
        twelveCount = twelveCount + 1


#写NET1=7这种
for item in result:
    num = int(item[0])
    if (num == 1) or (num % 2 == 0):
        writefile.writelines("NET"+str(index)+"="+str(item[1]+"\n"))
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
        print(len(item))
        if(num==4):
            writefile.writelines("EXR4W:"+str(item[1])+"\n")

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
                    while count2<len(twoStrList)-1:
                        if(twoStrList[int(resultList[resultListIndex])]!=twoStrList[count2]):#判断两个是否重复
                            #第一种情况小于
                            if int((twoStrList[int(resultList[resultListIndex])].split(","))[0])>int((twoStrList[count2].split(","))[0]):
                                writefile.writelines("EXR4W:"+twoStrList[count2]+","+ twoStrList[int(resultList[resultListIndex])]+"\n")
                            else:
                                writefile.writelines("EXR4W:" + twoStrList[ int(resultList[resultListIndex])] + "," +  twoStrList[count2]+ "\n")
                        count2 = count2 + 1
                    resultListIndex=resultListIndex+1
                else:
                    resultListIndex = 0
                    while count2 < len(twoStrList) - 1:
                        if (twoStrList[int(resultList[resultListIndex])] != twoStrList[count2]):
                            writefile.writelines(
                                "EXR4W:" + twoStrList[int(resultList[resultListIndex])] + "," + twoStrList[
                                    count2] + "\n")
                        count2 = count2 + 1
                    resultListIndex = resultListIndex + 1






