## 호텔 예약 문의1 - 일반 - 예
* 호텔-예약문의-일반
  - booking_form <!-- required slots : 날짜, 인원, 기간, 객실종류 -->
  - form{"name": "booking_form"}
  - form{"name": null}
  - booking_form
* 긍정
  - utter_ask_고객정보
* inform-고객정보 <!-- 이름, 휴대폰번호 -->
  - customer_info_form
  - form{"name": "customer_info_form"}
  - form{"name": null}
  - utter_anythingelse

## 호텔 예약 문의1 - 일반 - 중간 취소
* 호텔-예약문의-일반
  - booking_form <!-- required slots : 날짜, 인원, 기간, 객실종류 -->
  - form{"name": "booking_form"}
* 부정
  - utter_process_stopped <!-- 예약 절차가 종료되었습니다. 저장된 정보는 소멸됩니다.  -->
  - form{"name": null}
  - action_reset_all_slot
  - utter_anythingelse
  
## 호텔 예약 문의1 - 인사로 시작
* 인사
  - utter_greet
* 호텔-예약문의-일반
  - booking_form <!-- required slots : 날짜, 인원, 기간, 객실종류 -->
  - form{"name": "booking_form"}
  - form{"name": null}
* 긍정
  - utter_ask_고객정보
* inform-고객정보 <!-- 이름, 휴대폰번호 -->
  - customer_info_form
  - form{"name": "customer_info_form"}
  - form{"name": null}
  - utter_anythingelse

## 호텔 예약 문의2 - 시작끝날짜
* 호텔-예약문의-시작끝
  - booking_form2 <!-- required slots : 시작날짜, 끝날짜, 인원, 객실종류 -->
  - form{"name": "booking_form2"}
  - form{"name": null}
* 긍정
  - utter_ask_고객정보
* inform-고객정보 <!-- 이름, 휴대폰번호 -->
  - customer_info_form
  - form{"name": "customer_info_form"}
  - form{"name": null}
  - utter_anythingelse
