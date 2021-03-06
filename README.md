Contoh kode demo implementasi rantai pasok (supply chain) di Nuchain.

## Dokumentasi

Untuk dokumentasi silahkan baca [Nuchain Docs](https://nuchain.network/docs/build/supply-chain)

Gambaran alur kerja:

![nuchain supply chain](https://nuchain.network/assets/images/nuchain-supply-chain-c95c544c0357d8018cf71db9da92c868.png)

Cara menjalankan demonya:

```
python test_supply_chain.py
```

Secara default perintah tersebut akan menjalankan script untuk jaringan Testnet.
Apabila ingin mencobanya di node local bisa menjalankan perintah seperti berikut:

```
NUCHAIN_HOST=ws://127.0.0.1:9944 python test_supply_chain.py
```

Pastikan node lokal sudah jalan dengan perintah:

```
nuchain --dev --tmp
```

### Penjelasan

Kode ini akan mendemonstrasikan alur kerja rantai pasok sebagai berikut:

1. Membuat organisasi
2. Organisasi mendaftarkan produk
3. Organisasi mendaftarkan tracking berisi produk yg dibuat di poin 2.
4. Bob sebagai admin organisasi melakukan update status pada tracking yang dibuat di poin 3.
5. Charlie coba melakukan update status, tetapi gagal karena tidak memiliki akses.
6. Bob sebagai admin organisasi memberikan akses kepada Charlie.
7. Charlie coba melakukan update status dan berhasil.
8. Melakukan tracing.

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
5. CHARLIE UPDATE STATUS...
   🔖 '2a28f...6ab53' included in block #7
     GAGAL
6. GRANT ACCESS KE CHARLIE...
   🔖 '5faf3...3d189' included in block #8
     SUKSES
7. CHARLIE UPDATE STATUS...
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
