import os, time, datetime, pytz, sys
from pytz import timezone
from datetime import datetime, timedelta
from collections import OrderedDict
from .bg_scheduler import scheduler # 백그라운드 스케줄러 설정

connect_list=list()
exit_signal=False
model_dir=os.path.dirname(os.path.realpath(__file__)).split('/')[-1] # farm_xxxx


class CustomError(Exception):
    """
    스케줄러 재시작을 위한 CustomError 생성
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg



def init_bt_discovered_start(adapter_dev, bt_dev_tag):
    """
    init_bt_discovered_start 함수 설명
    : bluetooth (BLE) 장치를 찾는 함수, 새로운 장치를 찾았을때 status를 connect로 변경하는 역활

    상세 설명

    1. 블루투스 디바이스 명에 sc_dev가 포함될때
    2. Bt_dev DB에 저장된 장치명 또는 어드레스 조회(쿼리)
    3. 기존 Bt_dev 장치가 아무것도 없을 경우 바로 업데이트
    4. Bt_dev에 저장된 DB들 중 발견된 장치명과 어드레스가 완전 일치 할때 connect로 변경
    5. 오류시 해당 DB의 장치를 disconnect 상태로 변경
    """

    from .models import Bt_dev
    from django.db.models import Q
    import gatt

    global exit_signal

    # gatt discovered 코드
    class AnyDeviceManager(gatt.DeviceManager):
        def device_discovered(self, device):
            if bt_dev_tag in str(device.alias()): # 1. 블루투스 디바이스 명에 bt_dev_tag가 포함될때
                # 2. Bt_dev DB에 저장된 장치명 또는 어드레스 조회(쿼리)
                btdev = Bt_dev.objects.filter(Q(bt_id=str(device.alias())) | Q(bt_address=device.mac_address))
                btdev_dict = OrderedDict()

                for btv in btdev: # 2-1. DB에 저장된 장치명을 dict으로 저장
                   btdev_dict[btv.bt_id]=btv.bt_address

                if len(btdev_dict) == 0: # 3. DB에 Bt_dev 장치가 아무것도 없을 경우 바로 업데이트
                    new_btd = Bt_dev(bt_id=str(device.alias()), bt_address=device.mac_address, status='connect')
                    print("[DISCOVERED] {} : {}".format(model_dir, str(device.alias())))
                    new_btd.save()

                else: # 3-1. Bt_dev 장치가 한개라도 있을 경우 발견한 장치명과 어드레스를 dict으로 저장
                    new_btdev_dict={str(device.alias()) : device.mac_address}

                    # 2-2. DB에 저장된 장치명을 for문으로 비교
                    for n, (btk, btv) in enumerate(btdev_dict.items()):
                        if new_btdev_dict=={btk : btv}: # 4. Bt_dev에 저장된 DB들 중 발견된 장치명과 어드레스가 완전 일치 할때
                            if btdev[n].status == 'disconnect':
                                btdev[n].status = 'connect' # 4-1. 일치한 DB에 status를 disconnect 에서 connect 로 변경
                                btdev[n].save()
                                break
                            else:
                                pass
                        else:
                            if btk == next(iter(new_btdev_dict.keys())): # 4-2. 장치명이 같고 어드레스가 다를때는 삭제
                                btdev[n].delete()
                            else:
                                if btv == next(iter(new_btdev_dict.values())): # 4-3. 어드레스가 같을때는 장치명의 값을 변화
                                    btdev[n].bt_id = next(iter(new_btdev_dict.keys()))
                                    print("[DEVICE CHANGED] {} : {} -> {}".format(model_dir, btk, str(device.alias())))
                                    btdev[n].save()

    try:
       manager = AnyDeviceManager(adapter_name=adapter_dev)
       manager.is_adapter_powered = True
       manager.start_discovery()
       manager.run()

    except (KeyboardInterrupt, SystemExit):
#       print("[DISCOVER EXIT] {} - {}".format(model_dir, "discover 중지됨"))
       btdev=Bt_dev.objects.filter(status='connect')

       for btv in btdev: # 5. 오류시 disconnect 상태로 변경
           btv.status='disconnect'
           btv.save()

       manager.stop_discovery()
       manager.stop()



def bt_dev_scheduler(adapter_dev):
    """
    bt_dev_scheduler 함수 설명
    : Bt_dev에 connct 상태로 저장된 장치명의 데이터를 불러오는 코드

    상세 설명

    1. Bt_dev에 저장된 장치명의 상태가 connect 인 장치명과 어드레스를 dict으로 저장
    2. connect_list에서 현재 연결 된 리스트를 @ 으로 파싱후 장치명과 어드레스를 dict으로 저장
    3. 새로 추가된 장치가 있을때 init_bt_connect_start 스케줄러 시작
    4. init_bt_connect_start 스케줄러가 시작된 장치명과 어드레스를 connect_list에 저장
    """

    from .models import Bt_dev

    global connect_list
    global exit_signal

    if exit_signal == True:
        print('\n 서버 중지됨 \n CONTROL + Z and Process kill (./server_exit.sh)')
        scheduler.remove_job('bt_dev_scheduler')
        scheduler.shutdown(wait=False)

    sched_jobs_dict = dict()
    btdev = Bt_dev.objects.filter(status="connect") # 1. Bt_dev에 저장된 장치명의 상태가 connect 일때
    btdev_dict = dict()

    for btv in btdev: # 1-1. 위에서 쿼리한 장치명과 어드레스를 dict으로 저장
        btdev_dict[btv.bt_id]=btv.bt_address

    for sj in connect_list: # 2. connect_list에서 현재 연결 된 리스트를 @ 으로 파싱
        sj_sp=sj.split('@')
        sched_jobs_dict[sj_sp[0]]=sj_sp[1] # 2-1. connect_list의 장치명과 어드레스를 dict으로 저장

    # 3. 새로운 장치가 있는지 검사
    bt_data_add = set(btdev_dict.keys())-set(sched_jobs_dict.keys())

    # 3-1. 새로 추가된 장치가 있을때 init_bt_connect_start 스케줄러 시작
    for n, bt_add_key in enumerate(bt_data_add):
        job_date = datetime.now(timezone('Asia/Seoul')) + timedelta(seconds=(n+1))
        scheduler.add_job(init_bt_connect_start, 'date', args=[bt_add_key, btdev_dict[bt_add_key], adapter_dev], run_date=job_date, max_instances=1, id="{}@{}".format(bt_add_key, btdev_dict[bt_add_key])) # job 생성 인터벌 2초

        # 3-2. init_bt_connect_start 스케줄러가 시작된 장치명과 어드레스 connect_list에 저장
        if "{}@{}".format(bt_add_key, btdev_dict[bt_add_key]) not in connect_list:
            connect_list.append("{}@{}".format(bt_add_key, btdev_dict[bt_add_key]))


def init_bt_connect_start(dev_id, dev_address, adapter_dev):
    """
    init_bt_connect_start 함수 설명
    : Bt_dev에 connect 상태로 저장된 장치의 실제 데이터를 받아 Bt_data DB에 저장함

    상세 설명

    1. 정상적으로 연결될 경우 : CONNECTING (연결시도) -> CONNECTED (연결됨)
    2. Bt_dev status에는 connect 인데 실제로 연결이 안되는 경우 : CONNECTING (연결시도) -> CONNECT FAILED (연결실패)
    3. 블루투스 연결이 중간에 종료될 경우 : DISCONNECT (연결종료)
    4. 비정상적 종료시 : CONNECT EXIT (연결 강제 종료)
    5. services_resolved 함수에서 GATT 프로파일의 서비스를 불러오고 characteristic_value_updated 함수에서 characteristics의 값을 계속 읽는 방식
    6. 블루투스 장치에서 예를들어 38.5,46.2,96.5 의 값으로 넘어오면 ','로 파싱해서 DB에 저장
    """

    from .models import Bt_dev, Bt_data
    from django.db.models import Q
    import gatt

    global exit_signal

    manager = gatt.DeviceManager(adapter_name=adapter_dev)


    class AnyDevice(gatt.Device):

        def __init__(self, mac_address, manager, auto_reconnect=False):
            super().__init__(mac_address=mac_address, manager=manager)
            self.auto_reconnect = auto_reconnect
            self.init_connect_flag = True
            self.init_disconnect_flag = True

        def connect(self):
            print("[CONNECTING] {} : {} {} {}".format(model_dir, dev_id, dev_address, "연결중"))
            super().connect()

        def connect_succeeded(self):
            super().connect_succeeded()
            print("[CONNECTED] {} : {} {} {}".format(model_dir, dev_id, dev_address, "연결완료"))

        def connect_failed(self, error):
            super().connect_failed(error)
            print("[CONNECT FAILED] {} : {} {} {}".format(model_dir, dev_id, dev_address, "연결실패"))

            btdev = Bt_dev.objects.filter(bt_address=self.mac_address)

            for btv in btdev: # disconnect 상태로 변경
                btv.status='disconnect'
                btv.save(update_fields=['status'])

            if "{}@{}".format(dev_id, dev_address) in connect_list:
                connect_list.remove("{}@{}".format(dev_id, dev_address))

            manager.stop()
            raise CustomError("{}@{}".format(dev_id, dev_address))


        def disconnect_succeeded(self):
            super().disconnect_succeeded()

            print("[DISCONNECTED] {} : {} {} {}".format(model_dir, dev_id, dev_address, "연결종료"))

            btdev = Bt_dev.objects.filter(bt_address=self.mac_address)

            for btv in btdev: # disconnect 상태로 변경
                btv.status='disconnect'
                btv.save(update_fields=['status'])


            if "{}@{}".format(dev_id, dev_address) in connect_list:
                connect_list.remove("{}@{}".format(dev_id, dev_address))


            if self.auto_reconnect:
                self.connect()

            manager.stop()
#            raise CustomError("{}@{}".format(dev_id, dev_address))


        # 5. services_resolved 함수에서 GATT 프로파일의 서비스 정보를 볼러옴
        def services_resolved(self):
            super().services_resolved()

            device_information_service = next(
                s for s in self.services
                if s.uuid == '0000ffe0-0000-1000-8000-00805f9b34fb')

            device_bluetooth_data = next(
                c for c in device_information_service.characteristics
                if c.uuid == '0000ffe1-0000-1000-8000-00805f9b34fb')


            device_bluetooth_data.enable_notifications()
            device_bluetooth_data.read_value()

        # 5-1. 매칭된 서비스의 characteristics의 값을 계속 읽어옴
        def characteristic_value_updated(self, characteristic, value):
            try:
                if value==b'\x01' and self.init_connect_flag==True: # 초기 값 버림
                    self.init_connect_flag=False
                elif value==b'/' and self.init_connect_flag==True: # 초기 값 버림
                    self.init_connect_flag=False
                elif value==b'v' and self.init_connect_flag==True: # 초기 값 버림
                    self.init_connect_flag=False
                elif value==b'\r' and self.init_connect_flag==True: # 초기 값 버림
                    self.init_connect_flag=False
                else:
                    # 6. 블루투스에서 예를 들어 38.5,46.2,96.5 의 값으로 넘어오면 ','로 파싱해서 Bt_data DB에 저장
                    new_bt_data = value.decode('utf-8').rstrip().strip()
                    new_bt_data_sp=new_bt_data.split(',')
                    new_btd = Bt_data(bt_id=dev_id, temp=float(new_bt_data_sp[0]), bpm=float(new_bt_data_sp[1]), battery=float(new_bt_data_sp[2]))
                    new_btd.save() # DB에 저장
                    print("[UPDATE] {} : {} {}".format(model_dir, dev_id, new_bt_data))
            except:
                print("[UPDATE FAIL] {} {} {}".format(model_dir, dev_id, value )) # 디버깅용

    try:
        device = AnyDevice(mac_address=dev_address, manager=manager, auto_reconnect=False)
        device.connect()
        manager.run()

    except (CustomError, KeyboardInterrupt, SystemExit):

       if "{}@{}".format(dev_id, dev_address) in connect_list:
           connect_list.remove("{}@{}".format(dev_id, dev_address))

       manager.stop()
