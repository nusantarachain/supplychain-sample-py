##
# Contoh kode fungsi-fungsi supply chain di Nuchain.
#
# kode ini menggunakan library https://github.com/polkascan/py-substrate-interface
# untuk berkomunikasi dengan Nuchain node.
#

from substrateinterface import SubstrateInterface, Keypair
from substrateinterface.exceptions import SubstrateRequestException
from substrateinterface.utils import ss58


import json

with open("nuchain-types.json") as f:
    nuchain_types = json.load(f)

conn = None

def connect(url):
    global conn
    try:
        conn = SubstrateInterface(
            url=url,
            ss58_format=42,
            type_registry_preset='polkadot',
            type_registry=nuchain_types
        )
        return conn
    except ConnectionRefusedError:
        print("⚠️ Cannot connect to Nuchain node")
        exit()

def short_hash(a_hash):
    return a_hash[2:7] + "..." + a_hash[-5:]

def submit_extrinsic(extrinsic):
    try:
        receipt = conn.submit_extrinsic(extrinsic, wait_for_inclusion=True)
        block = conn.get_block(block_hash=receipt.block_hash)
        print("   🔖 '{}' included in block #{}".format(short_hash(receipt.extrinsic_hash), block['header']['number']))
        if receipt.is_success:
            print("     SUKSES")
        else:
            print("     GAGAL")
        return receipt
    except SubstrateRequestException as e:
        print("Failed to send: {}".format(e))


def create_organization(name, description, admin, website="", email="", props=[], account=None):

    call = conn.compose_call(
        call_module="Organization",
        call_function="create",
        call_params={
            "name": name,
            "description": description,
            "admin": admin,
            "website": website,
            "email": email,
            "props": props
        }
    )
    extrinsic = conn.create_signed_extrinsic(call=call, keypair=account)

    receipt = submit_extrinsic(extrinsic)

    # dapatkan ID organisasi yang baru saja tercipta
    # dengan cara menangkapnya di atribut event `OrganizationAdded`
    for event in receipt.triggered_events:
        org_id = get_created_org_id(event)
        if org_id:
            print("+ Org created ID: {}".format(org_id))
            print("    ss58 Address: {}".format(ss58.ss58_encode(org_id)))
            return org_id


def get_created_org_id(event):
    """Mendapatkan ID organisasi dari event
    yang ke-trigger dari ekstrinsik `organization.create`.
    """
    print("module: {}, event: {}".format(event.event_module.name, event.event.name))
    if event.event_module.name == "Organization" and event.event.name == "OrganizationAdded":
        return event.params[0]['value']
        

def register_product(product_id, org_id, year, props=[], account=None):
    """Daftarkan produk ke registry"""
    call = conn.compose_call(
        call_module="ProductRegistry",
        call_function="register",
        call_params={
            "id": product_id,
            "org_id": org_id,
            "year": year,
            "props": props
        }
    )
    extrinsic = conn.create_signed_extrinsic(call=call, keypair=account)
    receipt = submit_extrinsic(extrinsic)

    for event in receipt.triggered_events:
        if event.event_module.name == "ProductRegistry" and event.event.name == "ProductRegistered":
            print("+ Product registered:", event.params[1]['value'])


def create_tracking(tracking_id, org_id, year, products=[], parent_id=None, props=None, account=None):
    """Buatkan tracking untuk produk"""
    call = conn.compose_call(
        call_module="ProductTracking",
        call_function="register",
        call_params={
            "id": tracking_id,
            "org_id": org_id,
            "year": year,
            "products": products,
            "parent_id": parent_id,
            "props": props
        }
    )
    extrinsic = conn.create_signed_extrinsic(call=call, keypair=account)
    receipt = submit_extrinsic(extrinsic)

    for event in receipt.triggered_events:
        if event.event_module.name == "ProductTracking" and event.event.name == "TrackingRegistered":
            print("+ Tracking registered:", event.params[1]['value'])
        # else:
        #     print(event)

def update_status(tracking_id, status, timestamp, location=None, readings=None, props=None, account=None):
    """Update status tracking"""
    call = conn.compose_call(
        call_module="ProductTracking",
        call_function="update_status",
        call_params={
            "id": tracking_id,
            "status": status,
            "timestamp": timestamp,
            "location": location,
            "readings": readings,
            "props": props
        }
    )
    extrinsic = conn.create_signed_extrinsic(call=call, keypair=account)
    receipt = submit_extrinsic(extrinsic)

    if receipt is not None:
        for event in receipt.triggered_events:
            if event.event_module.name == "ProductTracking" and event.event.name == "TrackingStatusUpdated":
                if event.event.name == "TrackingStatusUpdated":
                    params = event.params
                    print(" [i] got tracking event: `{}` {}".format(params[1]['value'], params[3]['value']))
            # else:
            #     print(event)

def grant_access(org_id, to_account, valid_for=None, account=None):
    """Grant access ke akun melalui Decentralized Identifiers (DIDs) module
    https://wiki.nuchain.network/docs/build/build-did
    """
    call = conn.compose_call(
        call_module="Did",
        call_function="add_delegate",
        call_params={
            "identity": org_id,
            "delegate": to_account,
            "delegate_type": "ProductTracker", # kode akses untuk tracker adalah "ProductTracker"
            "valid_for": valid_for
        }
    )
    extrinsic = conn.create_signed_extrinsic(call=call, keypair=account)
    receipt = submit_extrinsic(extrinsic)
    return receipt

