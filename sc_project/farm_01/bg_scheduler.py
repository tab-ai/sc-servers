import sys
from apscheduler.schedulers.background import BackgroundScheduler # 백그라운드 스케줄러 생성
#from django.conf import settings

scheduler = BackgroundScheduler() # 스케줄러 객체 생성
