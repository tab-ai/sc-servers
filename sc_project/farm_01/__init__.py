# init setting
import sys

if 'makemigrations' in sys.argv:
    pass
elif 'migrate' in sys.argv:
    pass
elif 'shell' in sys.argv:
    pass
elif 'runserver'in sys.argv:
    from datetime import datetime, timedelta
    from pytz import timezone
    from .bg_scheduler import scheduler
    from .bt_auto_connect import init_bt_discovered_start, bt_dev_scheduler, init_bt_connect_start

    try:
        # 스케줄러 시작
        scheduler.start()

        # 원하는 bt device tag 및 adapter_dev 설정
        adapter_dev='hci0'
        bt_dev_tag='vsc'

        # init_bt_discovered_start 실행코드 (서버 실행 2초 후 시작)
        job_date = datetime.now(timezone('Asia/Seoul')) + timedelta(seconds=2)
        scheduler.add_job(init_bt_discovered_start, 'date', args=[adapter_dev, bt_dev_tag], run_date=job_date, max_instances=1, id="init_bt_discovered_start")

        # bt_dev_scheduler 스케줄러를 5초 마다 실행 (5초 마다 새로운 장치가 추가 됬는지 검사)
        scheduler.add_job(bt_dev_scheduler, 'interval', args=[adapter_dev], seconds=5, max_instances=1, id="bt_dev_scheduler")
    except (KeyboardInterrupt, SystemExit):
        print("서버 종료")
