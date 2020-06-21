import nfc
import binascii
import time
from threading import Thread, Timer

TIME_cycle = 10.0
TIME_interval = 0.2
TIME_wait = 3

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
target_req_felica = nfc.clf.RemoteTarget("212F")

# 106A(NFC type A)で設定
target_req_nfc = nfc.clf.RemoteTarget("106A")


def check_FeliCa():
    print('FeliCa waiting..')
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(target_req_felica, iterations=int(
        TIME_cycle//TIME_interval)+1, interval=TIME_interval)
    if not target_res is None:
        tag = nfc.tag.activate(clf, target_res)

        # IDmを取り出す
        idm = binascii.hexlify(tag.idm)
        print('FeliCa detected. idm = ', idm)

        # sleepなしでは次の読み込みが始まって終了する
        print('sleep ', str(TIME_wait), ' seconds')
        time.sleep(TIME_wait)

    clf.close()


def check_NFC():
    print('NFC and FeliCa waiting...')
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')

    mydict = {}
    while True:
        target_res = clf.sense(target_req_nfc, target_req_felica, iterations=int(
            TIME_cycle//TIME_interval)+1, interval=TIME_interval)
        if not target_res is None:
            tag = nfc.tag.activate(clf, target_res)
            print('TAG type: ' + tag.type)

            # FeliCaカードをタッチしたら読み込みをやめる
            if tag.type == "Type3Tag":
                break
            # Type1,Type2:NFCタグ、Type4:Android端末でのNFCなど
            else:
                # NFCタグに埋めたtextを読む
                records = tag.ndef.records
                for record in records:
                    print('NFC detected. record.text = ' + record.text)
                    # str()で変換するとユニコードオブジェクトにならない
                    key = str(record.text)
                    mydict[key] = key

                print('sleep ', str(TIME_wait), ' seconds')
                time.sleep(TIME_wait)
    for dic in mydict:
        print(dic)

    clf.close()


check_FeliCa()
check_NFC()
