Contoh implementasi rantai pasok (supply chain) di Nuchain.

## Demo

```console
$ python test_supply_chain.py
1. BUAT ORGANISASI...
   🔖 '533b5...5e096' included in block #2
     SUKSES
module: Treasury, event: Deposit
module: Did, event: OwnerChanged
module: Organization, event: OrganizationAdded
+ Org created ID: 0x10ee41f34f4dd68c9ef0f5e07e1f6dce65633f325123e743a5a7bd9a946a9de5
    ss58 Address: 5CSuQBuv5WKs9xfvvxX3fZe6MsBZvUYYjJFg3Qi8J8uzosZu
2. DAFTARKAN PRODUK...
   🔖 '0b934...fd643' included in block #3
     SUKSES
+ Product registered: kopi-bowongso-01
3. BUAT TRACKING...
   🔖 'f917e...76b16' included in block #4
     SUKSES
+ Tracking registered: kopi-bowongso-paket-01
4. BOB UPDATE STATUS...
   🔖 '6891a...0c873' included in block #5
     SUKSES
 [i] got tracking event: `kopi-bowongso-paket-01` dipanen
   🔖 'f403e...8cc67' included in block #6
     SUKSES
 [i] got tracking event: `kopi-bowongso-paket-01` dimasak
4. CHARLIE UPDATE STATUS...
   🔖 '2a28f...6ab53' included in block #7
     GAGAL
5. GRANT ACCESS KE CHARLIE...
   🔖 '5faf3...3d189' included in block #8
     SUKSES
6. CHARLIE UPDATE STATUS...
   🔖 '6c532...2cc2d' included in block #9
     SUKSES
 [i] got tracking event: `kopi-bowongso-paket-01` dipacking
7. TRACING...
Track ID: kopi-bowongso-paket-01
     ├─■ 23-04-2021 13:39:12 [Registration] - registered @ location: None
     │
     ├─■ 23-04-2021 13:39:12 [UpdateStatus] - dipanen @ location: None
     │
     ├─■ 23-04-2021 13:39:18 [UpdateStatus] - dimasak @ location: {'latitude': -7.7195894, 'longitude': 110.3519251}
     │
     ├─■ 23-04-2021 13:39:36 [UpdateStatus] - dipacking @ location: None
     │
END OF DEMO.
```
