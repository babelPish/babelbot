import re
from datetime import datetime
from actions import korean2num
from rasa_sdk import Tracker
import logging
logger = logging.getLogger(__name__)

numbers = {"하루": 1,
           "이틀": 2,
           "사흘": 3,
           "나흘": 4,
           "닷새": 5,
           "엿새": 6,
           "이레": 7,
           "여드레": 8,
           "아흐레": 9,
           "열흘": 10,
           "열하루": 11,
           "보름": 15,
           "스무날": 20
           }


def extractIntegerFromHanguelDate(raw, today):
    '''
    한글로 되어 있는 날짜에서 숫자로 월, 일 정보 반환
    '''
    if '년' in raw:
        year = korean2num.decode(raw.split('년')[0])
        raw = raw.split('년')[1].strip()
    else:
        year = today.year
    if '월' in raw:
        tmp = raw.split('월')[0]
        if tmp == '시':
            month = 10
        else:
            month = korean2num.decode(tmp)
        raw = raw.split('월')[1].strip()
    else:
        month = today.month
    if '일' in raw:
        day = korean2num.decode(raw.split('일')[0])
    else:
        raise ValueError('Wrong Date Format')

    # print('reformated date : {}-{}-{}'.format(year, month, day))
    return datetime(year=year, month=month, day=day)


def extractIntegersFromRawMixDate(rawDate, today, book=True):
    nums = re.findall('[1-9][0-9][0-9][0-9]|[0-9]?[0-9]', rawDate)
    if len(nums) == 3: # year, month, day
        if len(nums[0]) == 4:
            year = int(nums[0])
        elif len(nums[0]) == 2:
            if book:
                year = int(nums[0])+2000
                if year >= today.year+2:
                    raise ValueError('extractIntegersFromRawMixDate : 예약불가 연도')
            else: # 몇 년생 물어보는 것에 대한 대답 처리
                if int(nums) <= today.year - 2000 + 1:
                    year = int(nums) + 2000
                else:
                    year = int(nums) + 1900
        else:
            raise ValueError('extractIntegersFromRawMixDate : wrong format {}'.format(rawDate))
        month = int(nums[1])
        day = int(nums[2])

    elif len(nums) == 2:
        year = today.year
        month = int(nums[0])
        day = int(nums[1])

    elif len(nums) == 1:
        year = today.year
        month = today.month
        day = int(nums[0])
    else:
        raise ValueError('extractIntegersFromRawMixDate : wrong format {}'.format(rawDate))

    return datetime(year, month, day)


def convertRawToDate(rawData):
    '''
    전체가 한글로 표현되거나 일부만 한글로 되어 있는 날짜를
    YYYY-MM-dd 형식으로 변환하여 반환
    '''
    condition_h = '((십|이십)년 ?)?((일|이|삼|사|오|유|육|칠|팔|구|십|시|십일|십이)월 ?)?((이|삼)?십)?(일|이|삼|사|오|육|칠|팔|구)일|' \
                  '((십|이십)년 ?)?((일|이|삼|사|오|유|육|칠|팔|구|십|시|십일|십이)월 ?)?((이|삼)?십)(일|이|삼|사|오|육|칠|팔|구)?일'
    condition_i = '((20)?[0-2][0-9]년 ?)?(1?[0-9]월 ?)?[1-3]?[0-9]일'
    today = datetime.now()

    if type(rawData) is not list:
        rawData = [rawData]

    wrong = True
    for rawDate in rawData:
        if re.search(condition_h, rawDate):
            date = extractIntegerFromHanguelDate(rawDate, today)
            wrong = False
            break
        elif re.search(condition_i, rawDate):
            date = extractIntegersFromRawMixDate(rawDate, today)
            wrong = False
            break
    if wrong:
        raise ValueError('Wrong Date Format : 확인불가 유형')
    return date

def getLongestStr(candidates):
    idx = 0
    maxlen = len(candidates[0])
    for i in range(1,len(candidates)):
        if maxlen < len(candidates[i]):
            idx = i
            maxlen = len(candidates[i])
    return candidates[idx]

def extractSingleInteger(rawText):
    if type(rawText) is int:
        return rawText
    elif type(rawText) is list:
        # list 중 제일 긴 텍스트로 지정한다.
        rawText = getLongestStr(rawText)
        print('raw : ', rawText)

    if rawText in numbers.keys():
        return numbers[rawText]

    nums = re.findall('[1-9][0-9]?', rawText)
    # 일반적으로 1박2일 이런 형태로 말하기 때문에 몇 박인지 추출한다.
    return int(nums[0])


def donthave(tracker: Tracker, slots):
    '''
    slot list에 있는 slot들이 모두 없어야 True, 하나라도 있으면 False
    :param tracker:
    :param slots:
    :return: bool
    '''
    for slot in slots:
        if tracker.get_slot(slot):
            return False
    return True


def checkDateFormat(slot):
    if slot is None:
        return 1
    if type(slot) == list:
        return 1
    if re.search('박.{0,3}일|일 ?동안|일 ?기간', slot):
        return 0
    else: return 1

# if __name__ == '__main__':
    # res = convertRawToDate('시월 십일이요')
    # print(res)
    # res = extractSingleInteger(['1박', '3박 4일'])
    # res = extractSingleInteger('3박 4일이요')
    # print(res)