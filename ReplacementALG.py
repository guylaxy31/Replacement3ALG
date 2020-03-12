from collections import Counter
import random


def GenString(StartCount, EndCount, FirstNum, LastNum):
    strRandlen = random.randint(StartCount, EndCount)
    tmp_refSTR = [None]*strRandlen

    for i in range(strRandlen):
        tmp_refSTR[i] = random.randint(FirstNum, LastNum)

    return tmp_refSTR


def FifoReplace(refSTR, frameSize):

    framePointer = 0

    stringLen = len(refSTR)

    pageFault = 0
    Hit = 0

    frame = [None]*frameSize
    pageFaultCountList = []

    for i in range(stringLen):

        if framePointer >= frameSize:
            framePointer = 0

        if refSTR[i] not in frame:

            frame[framePointer] = refSTR[i]
            pageFaultCountList.append(framePointer+1)
            framePointer += 1
            pageFault += 1

        else:
            Hit += 1

    FaultResult = Counter(pageFaultCountList)

    print(frame, ' Frame size is ', frameSize)
    print('Hit Count is ', Hit)
    print('PageFault count is ', pageFault)
    print(sorted(FaultResult.items()))

    print("\n")


def OptReplace(refSTR, frameSize):

    framePointer = 0

    stringLen = len(refSTR)

    pageFault = 0
    Hit = 0
    mostTime = 0
    mostTimeIDX = 0
    returnMatchIDX = 0

    frame = [None]*frameSize
    pageFaultCountList = []
    indexCheck = [0]*frameSize

    for i in range(stringLen):

        if framePointer < frameSize:
            if refSTR[i] not in frame:
                pageFault += 1
                frame[framePointer] = refSTR[i]
                pageFaultCountList.append(framePointer+1)
                indexCheck[framePointer] = 0
                framePointer += 1

                for idx, value in enumerate(indexCheck):
                    if idx != framePointer:
                        indexCheck[idx] += 1

            else:
                Hit += 1
                indexCheck[framePointer] = 0
                framePointer += 1

                for idx, value in enumerate(indexCheck):
                    if idx != framePointer:
                        indexCheck[idx] += 1
        else:
            # Find Index not use most time before append to the list
            mostTime = 0
            for l, value in enumerate(indexCheck):
                if value > mostTime:
                    mostTime = value
                    mostTimeIDX = l

            if refSTR[i] not in frame:

                frame[mostTimeIDX] = refSTR[i]
                pageFaultCountList.append(mostTimeIDX+1)
                pageFault += 1
                framePointer += 1
                indexCheck[mostTimeIDX] = 0

                for idx, value in enumerate(indexCheck):
                    if idx != mostTimeIDX:
                        indexCheck[idx] += 1
            else:
                Hit += 1

                for k, value in enumerate(frame):
                    if value == refSTR[i]:
                        returnMatchIDX = k

                frame[returnMatchIDX] = refSTR[i]
                indexCheck[returnMatchIDX] = 0
                for idx, value in enumerate(indexCheck):
                    if idx != returnMatchIDX:
                        indexCheck[idx] += 1

    FaultResult = Counter(pageFaultCountList)

    print(frame, ' Frame size is ', frameSize)
    print('Hit Count is ', Hit)
    print('PageFault count is ', pageFault)
    print(sorted(FaultResult.items()))

    print("\n")


def LRUReplace(refSTR, frameSize):

    framePointer = 0

    stringLen = len(refSTR)

    pageFault = 0
    Hit = 0
    LeastuseIDX = 0

    frame = [None]*frameSize
    pageFaultCountList = []
    tmpQueue = []

    for i in range(stringLen):
        if framePointer < frameSize:
            if refSTR[i] not in frame:
                pageFault += 1

                frame[framePointer] = refSTR[i]  # เพิ่มปกติ
                pageFaultCountList.append(framePointer+1)
                tmpQueue.append(refSTR[i])  # เพิ่มใน Queue ปกติไม่มีการลบ
                framePointer += 1

            else:
                Hit += 1
                # สำหรับเอาตัวแรกออกจาก Queue และเติม refSTR ท้าย Queue
                for o, value in enumerate(frame):
                    if value == tmpQueue[0]:
                        LeastuseIDX = o
                        tmpQueue[0] = None

                        break
                # เพิ่มเข้าไปใน Queue
                tmpQueue = list(filter(None, tmpQueue))
                tmpQueue.append(refSTR[i])

        # When framsize is full
        else:
            tmpQueue = list(filter(None, tmpQueue))
            if refSTR[i] not in frame:

                pageFault += 1
                # สำหรับเอาตัวแรกออกจาก Queue และเติม refSTR ท้าย Queue
                for o, value in enumerate(frame):
                    if value == tmpQueue[0]:
                        LeastuseIDX = o
                        tmpQueue[0] = None

                        break
                pageFaultCountList.append(LeastuseIDX+1)
                frame[LeastuseIDX] = refSTR[i]
                tmpQueue = list(filter(None, tmpQueue))
                tmpQueue.append(refSTR[i])
                framePointer += 1

            else:
                Hit += 1
            # สำหรับลบออกจาก Queue list
                for o, value in enumerate(tmpQueue):
                    if value == refSTR[i]:
                        tmpQueue[o] = None
                        break

            # เพิ่มตัวล่าสุดไปใน Queue
                tmpQueue = list(filter(None, tmpQueue))
                tmpQueue.append(refSTR[i])

    FaultResult = Counter(pageFaultCountList)

    print(frame, ' Frame size is ', frameSize)
    print('Hit Count is ', Hit)
    print('PageFault count is ', pageFault)
    print(sorted(FaultResult.items()))

    print("\n")


print("------------------FIFO Function has been called------------------", "\n")
refSTR = GenString(120, 150, 1, 10)
print('Random (', len(refSTR), ') strings')
print('Reference strings : ', refSTR, '\n')

FifoReplace(refSTR, 3)
FifoReplace(refSTR, 5)
FifoReplace(refSTR, 8)

print("------------------Optimize Function has been called------------------", "\n")

print('Random (', len(refSTR), ') strings')
print('Reference strings : ', refSTR, '\n')

OptReplace(refSTR, 3)
OptReplace(refSTR, 5)
OptReplace(refSTR, 8)

print("------------------Least Recently Use Function has been called------------------", "\n")

print('Random (', len(refSTR), ') strings')
print('Reference strings : ', refSTR, '\n')

LRUReplace(refSTR, 3)
LRUReplace(refSTR, 5)
LRUReplace(refSTR, 8)
