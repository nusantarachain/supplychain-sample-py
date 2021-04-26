#!/usr/bin/env python

from substrateinterface import Keypair
import nuchain
import time
from datetime import datetime

# Test accounts
ALICE = Keypair.create_from_uri('//Alice')
BOB = Keypair.create_from_uri('//Bob')
CHARLIE = Keypair.create_from_uri('//Charlie')

YEAR = "2021"


def main():

    nuchain.connect("wss://testnet.nuchain.riset.tech")
    # nuchain.connect("ws://127.0.0.1:9944")

    tracking_id = "kopi-bowongso-paket-02"

    # # account_info = conn.query('System', 'Account', params=[keypair.ss58_address])
    # # print("account info:", account_info)

    # 1. Buat organisasi
    print("\033[93m1. BUAT ORGANISASI...\033[0m")
    props = [{
        "name": "SK-KUMHAM",
        "value": "SKH-RI/2021/I33T"
    }]
    org_id = nuchain.create_organization(
        "MyOrganization", "Lorem Ipsum", BOB.ss58_address, props=props, account=ALICE)

    # # dapatkan informasi organisasi dari modul `Organization` storage `Organizations`.
    # org = nuchain.conn.query('Organization', 'Organizations', params=[org_id])
    # print(org)

    # 2. Daftarkan produk
    print("\033[93m2. DAFTARKAN PRODUK...\033[0m")
    nuchain.register_product("kopi-bowongso-01", org_id, YEAR, props=[
        {"name": "name", "value": "Kopi Bowongso"},
        {"name": "source", "value": "Bowongso, Indonesia"},
        {"name": "weight", "value": "100g"},
    ], account=BOB)

    # 3. Buat tracking
    print("\033[93m3. BUAT TRACKING...\033[0m")
    # kode tracking ini harus unik karena sifatnya global
    # apabila kode ini dijalankan lebih dari sekali maka yang kedua dan seterusnya akan gagal.

    nuchain.create_tracking(tracking_id, org_id, YEAR, account=BOB)

    # 4. Update status tracking
    print("\033[93m4. BOB UPDATE STATUS...\033[0m")
    nuchain.update_status(tracking_id, "dipanen", int(
        time.time() * 1000), account=BOB)

    # Update status tracking (lagi)
    location = {"latitude": "-7.7195894", "longitude": "110.3519251"}
    nuchain.update_status(tracking_id, "dimasak", int(
        time.time() * 1000), location=location, account=BOB)

    # Update status tracking (lagi) dengan akun orang lain (Charlie)
    # harusnya gagal, karena Charlie tidak memiliki akses dari organisasi
    print("\033[93m4. CHARLIE UPDATE STATUS...\033[0m")
    nuchain.update_status(tracking_id, "dikemas", int(
        time.time() * 1000), account=CHARLIE)

    # 5. Berikan akses ke Charlie
    print("\033[93m5. GRANT ACCESS KE CHARLIE...\033[0m")
    nuchain.grant_access(org_id, CHARLIE.ss58_address, account=BOB)

    # 6. Sekarang Charlie harusnya bisa update status tracking
    print("\033[93m6. CHARLIE UPDATE STATUS...\033[0m")
    nuchain.update_status(tracking_id, "dikemas", int(
        time.time() * 1000), account=CHARLIE)

    # 7. Tampilkan semua events pada suatu tracking
    print("\033[93m7. TRACING...\033[0m")
    resp = nuchain.conn.query(
        'ProductTracking', 'EventsOfTracking', params=[tracking_id])
    events = [nuchain.conn.query('ProductTracking', 'AllEvents', params=[
                                 str(idx)]) for idx in resp.elements]
    print("Track ID:", tracking_id)
    for event in events:
        event = event.value
        # print(event)
        event_type = list(event['event_type'])[0][8:]
        print("     ├─■ %s [%s] - %s @ location: %s" % (format_time(
            event['timestamp']), event_type, event['status'], event['location']))
        print("     │")

    print("END OF DEMO.")


def format_time(ms):
    return datetime.fromtimestamp(ms / 1000.0).strftime("%d-%m-%Y %H:%M:%S")


def print_receipt(receipt):
    print("Success:", receipt.is_success)
    print("Weight:", receipt.weight)
    print("Gas Fee:", receipt.total_fee_amount)
    if receipt.error_message:
        print(receipt.error_message)


if __name__ == "__main__":
    main()
