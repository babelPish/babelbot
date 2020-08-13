# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os
from typing import  Dict, Text, Any, List, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction, REQUESTED_SLOT
from rasa_sdk.executor import CollectingDispatcher
from .utils import *
from datetime import timedelta, datetime
import pandas as pd
import logging
logger = logging.getLogger(__name__)
from rasa_sdk.events import (
    AllSlotsReset,
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)



class BookingForm(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "booking_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        '''
        날짜, 기간, 시간표현(오늘,내일), 요일, 시작날짜, 끝날짜, 인원, 객실종류, 뷰종류

        1. 아무것도 없음
        2. 날짜 있음(나머지 정보도 종종 있지만 날짜는 꼭 있는 경우)
        3. 시작끝날짜 있음
        4. 인원만 있음
        5. 시간표현(오늘, 내일) (나머지 정보도 종종 있음)
        6. 기간만 있음
        7. 요일(이번 주 혹은 다음주 특정 요일)
        8. 객실종류
        9. 뷰종류

        1, 2, 4, 6, 8, 5, 9

        3 - 별도로

        7 - 나중에
        '''

        if tracker.get_slot('날짜'):  # 2
            # logger.info('2 진입')
            return ['날짜', '기간', '인원', '객실종류']
        elif tracker.get_slot('객실종류') and donthave(tracker, ['시간표현']):  # 8
            # logger.info('8 진입')
            return ['날짜', '기간', '인원', '객실종류']
        # 1
        elif donthave(tracker, ['날짜', '기간', '인원', '객실종류', '시간표현', '시작날짜', '끝날짜', '요일', '뷰종류']):
            # logger.info('1 진입')
            return ['날짜', '기간', '인원', '객실종류']
        # 4
        elif tracker.get_slot('인원') and \
                donthave(tracker, ['날짜', '기간', '객실종류', '시간표현', '시작날짜', '끝날짜', '요일', '뷰종류']):
            # logger.info('4 진입')
            return ['날짜', '기간', '인원', '객실종류']
        # 6
        elif tracker.get_slot('기간') and \
                donthave(tracker, ['날짜', '인원', '객실종류', '시간표현', '시작날짜', '끝날짜', '요일', '뷰종류']):
            # logger.info('6 진입')
            return ['날짜', '기간', '인원', '객실종류']
        # 9
        elif tracker.get_slot('뷰종류') and donthave(tracker, ['시간표현']):
            return ['날짜', '기간', '인원', '객실종류', '뷰종류']
        # 5
        elif (tracker.get_slot('시간표현') in ['오늘', '내일', '모레', '당일'] or set(tracker.get_slot('시간표현')) & set(['오늘', '내일', '모레', '당일'])) and \
                donthave(tracker, ['날짜', '시작날짜', '끝날짜', '요일']):
            # logger.info('시간표현(오늘/내일) 진입')
            return ['시간표현', '기간', '인원', '객실종류']

        else:
            raise ValueError('확인할 수 없는 유형')

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"날짜": self.from_entity(entity='날짜'),
                "시간표현": self.from_entity(entity='시간표현'),  # 5
                "기간": self.from_entity(entity='기간'),
                "인원": self.from_entity(entity='인원'),
                "객실종류": self.from_entity(entity='객실종류'),
                "뷰종류": self.from_entity(entity='뷰종류')  #
                }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        date = tracker.get_slot('날짜')
        timex = tracker.get_slot('시간표현')
        if not checkDateFormat(date) and timex is not None:
            date = None
        date_from_ep = tracker.get_slot('date')
        if date is not None:
            if date_from_ep is not None:
                logger.debug('날짜 : {}, date : {}'.format(date, date_from_ep))
                date = date_from_ep
            startdate = convertRawToDate(date)

        elif timex is not None:
            if (set(timex) & set(['오늘', '당일'])) or (timex in ['오늘', '당일']):
                startdate = datetime.now()
            elif '내일' in timex:
                startdate = datetime.now() + timedelta(days=1)
            elif '모레' in timex:
                startdate = datetime.now() + timedelta(days=2)
        else:
            raise ValueError('날짜, 시간표현 둘 다 없음.')

        period = tracker.get_slot('기간')
        logger.info('기간[0]: {}'.format(period))
        period = extractSingleInteger(period)
        logger.info('기간[1]: {}'.format(period))
        enddate = startdate + timedelta(days=period)

        # convert date obj to str format to serialize
        startdate = startdate.strftime('%Y-%m-%d')
        enddate = enddate.strftime('%Y-%m-%d')

        num = tracker.get_slot('인원')
        num = extractSingleInteger(num)
        room_type = tracker.get_slot('객실종류')
        view = tracker.get_slot('뷰종류')

        price = '이십만원'

        logger.info('start date : {}'.format(startdate))
        logger.info('end date : {}'.format(enddate))
        logger.info('period : {}'.format(period))
        logger.info('numPeople : {}'.format(num))
        logger.info('room_type : {}'.format(room_type))
        logger.info('view : {}'.format(view))
        logger.info('price : {}'.format(price))

        # 위 조건에 맞는 빈 방이 있는지 확인
        # 일단 있다고 가정하고

        # 고객 의사 확인
        if view is None:
            dispatcher.utter_message('숙박기간 : {startdate} ~ {enddate}\n'
                                     '객실유형 : {room}\n'
                                     '가격 : {price}\n'
                                     '인원 : {num}\n'
                                     '위 내용으로 예약진행 도와드릴까요?'
                                     .format(startdate=startdate,
                                             enddate=enddate,
                                             room=room_type,
                                             price=price,
                                             num=num))
        else:
            dispatcher.utter_message('숙박기간 : {startdate} ~ {enddate}\n'
                                     '객실유형 : {room}\n'
                                     '가격 : {price}\n'
                                     '인원 : {num}\n'
                                     '객실뷰 : {view}\n'
                                     '위 내용으로 예약진행 도와드릴까요?'
                                     .format(startdate=startdate,
                                             enddate=enddate,
                                             room=room_type,
                                             price=price,
                                             num=num,
                                             view=view))
        # 빈방이 없으면???

        return [SlotSet('시작날짜', startdate),
                SlotSet('끝날짜', enddate),
                SlotSet('인원', num),
                SlotSet('기간', period),
                SlotSet('가격', price)]


class BookingForm2(FormAction):

    def name(self) -> Text:
        """Unique identifier of the form"""
        return "booking_form2"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        '''
        3. 시작끝날짜 있음
        '''

        return ['시작날짜', '끝날짜', '인원', '객실종류']

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"시작날짜": self.from_entity(entity='시작날짜'),
                "끝날짜": self.from_entity(entity='끝날짜'),
                "인원": self.from_entity(entity='인원'),
                "객실종류": self.from_entity(entity='객실종류')
                }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Once required slots are filled, print buttons for found facilities"""

        startdate = tracker.get_slot('시작날짜')
        # logger.info('date : {}, format : {}'.format(date, type(date)))
        startdate = convertRawToDate(startdate)
        enddate = tracker.get_slot('끝날짜')
        enddate = convertRawToDate(enddate)

        # convert date obj to str format to serialize
        startdate = startdate.strftime('%Y-%m-%d')
        enddate = enddate.strftime('%Y-%m-%d')

        num = tracker.get_slot('인원')
        num = extractSingleInteger(num)
        room_type = tracker.get_slot('객실종류')
        view = tracker.get_slot('뷰종류')

        # 위 조건에 맞는 빈 방이 있는지 확인
        # 일단 있다고 가정하고

        price = '십오만원'
        # 고객 의사 확인
        if view is None:
            dispatcher.utter_message('숙박기간 : {startdate} ~ {enddate}\n'
                                     '객실유형 : {room}\n'
                                     '가격 : {price}\n'
                                     '인원 : {num}\n'
                                     '위 내용으로 예약진행 도와드릴까요?'
                                     .format(startdate=startdate,
                                             enddate=enddate,
                                             room=room_type,
                                             price=price,
                                             num=num))
        else:
            dispatcher.utter_message('숙박기간 : {startdate} ~ {enddate}\n'
                                     '객실유형 : {room}\n'
                                     '가격 : {price}\n'
                                     '인원 : {num}\n'
                                     '객실뷰 : {view}\n'
                                     '위 내용으로 예약진행 도와드릴까요?'
                                     .format(startdate=startdate,
                                             enddate=enddate,
                                             room=room_type,
                                             price=price,
                                             num=num,
                                             view=view))
        # 빈방이 없으면???

        return [SlotSet('시작날짜', startdate),
                SlotSet('끝날짜', enddate),
                SlotSet('인원', num),
                SlotSet('가격', price)]


class CustomerInfoForm(FormAction):
    '''
    고객정보(이름, 휴대폰번호) 입력 받은 후 예약 진행(db에 입력)
    '''
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "customer_info_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ['이름', '휴대폰번호']

    def slot_mappings(self) -> Dict[Text, Any]:
        return {"이름": self.from_entity(entity='이름'),
                "휴대폰번호": self.from_entity(entity='휴대폰번호')
                }

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:

        name = tracker.get_slot('이름')
        phonenum = tracker.get_slot('휴대폰번호')

        startdate = tracker.get_slot('시작날짜')
        enddate = tracker.get_slot('끝날짜')
        num = tracker.get_slot('인원')
        room_type = tracker.get_slot('객실종류')
        price = tracker.get_slot('가격')

        view = tracker.get_slot('뷰종류')
        if view is None:
            view = '랜덤'

        # 아직 하드코딩
        breakfast = 2
        add_bed = 0

        newRecords = {
            'name': name,
            'start_date': startdate,
            'end_date': enddate,
            'room_type': room_type,
            'num_people': num,
            'cellphone': phonenum,
            'view': view,
            'price': price,
            'breakfast': breakfast,
            'add_bed': add_bed,
            'status': 1
        }

        logger.info(newRecords)

        # db 에 저장

        dispatcher.utter_message('{name} 고객님 예약 완료되었습니다. 감사합니다.'.format(name=name))

        return []


class ResetAllSlot(Action):

    def name(self):
        return "action_reset_all_slot"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
        ) -> List[Dict]:

        return [AllSlotsReset()]
