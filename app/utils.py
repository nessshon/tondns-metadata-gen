from typing import Dict

from pytoniq_core import Cell, Address, begin_cell, StateInit

ITEM_CODE = "b5ee9c72410216010003af000114ff00f4a413f4bcf2c80b01020162020f0202ce030c020120040b02f30c8871c02497c0f83434c0c05c6c2497c0f83e90087c007e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7f4cffc0081acf8c08a3000638f440e17c20ccc4871c17cb8645c20843a282aff885b60101c20043232c15401f3c594017e808572da84b2c7f2cfc89bace51633c5c0644cb88072407ec0380a20050701f65f03323435355233c705f2e1916d70c8cb07f400c904fa40d4d420c701c0008e42fa00218e3a821005138d9170c82acf165003cf162604503373708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00915be29130e2820afaf08070fb027082107b4b42e62703076d8306060054708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb004503f00302e082105fcc3d14ba8e8a3810394816407315db3ce03a3a2682102fcb26a2ba8e3e3035365b347082108b77173504c8cbff58cf164430128040708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb00e0350582104eb1f0f9bae3025f08840ff2f0080a01f65137c705f2e191fa4021f001fa40d20031fa000c820afaf080a121945315a0a1de22d70b01c300209206a19136e220c2fff2e192218e3dc8500acf16500ccf16821005138d9171245146104f50f2708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0094102c395be20209007e8e3428f00148508210d53276db016d71708010c8cb055007cf165005fa0215cb6a12cb1fcb3f226eb39458cf17019132e201c901fb0093303436e25504f003007a5153c705f2e19101d3ff20d74ac20008d0d30701c000f2e19cf404300898d43040178307f417983050068307f45b30e270c8cb07f400c910355512f00300113e910c30003cb853600201200d0e00433b513434fffe900835d27080271fc07e903535350c04118411780c1c165b5b5b5b600023017232ffd40133c59633c5b33333327b55200201201011004bbc265f801282b2f82b8298064459ba37b74678b658382680a678b09e58380e8678b6583e4e840201201213000db8fcff0023031802012014150011b64a5e0042cbe0da1000c7b461843ae9240f152118001e5c08de004204cbe0da1a60e038001e5c339e8086007ae140f8001e5c33b84111c466105e033e04883dcb11fb64ddc4964ad1ba06b879240dc23572f37cc5caaab143a2fffbc4180012660f003c003060fe81edf4260f00304c1dd84e"  # noqa


def slice_hash(s: str) -> str:
    cell = begin_cell().store_snake_string(s).end_cell()
    return cell.hash.hex()


def calculate_nft_address_hash(subdomain: str, collection_addr_hash: str) -> str:
    collection_address = Address((0, int(collection_addr_hash).to_bytes(32, byteorder="big")))
    index = int.from_bytes(bytes.fromhex(slice_hash(subdomain)), "big", signed=False)

    data = begin_cell().store_uint(index, 256).store_address(collection_address).end_cell()
    code = Cell.one_from_boc(ITEM_CODE)

    state_init = StateInit(code=code, data=data)
    return state_init.serialize().hash.hex()


def create_item_metadata(collection_addr_hash: str, subdomain: str, domain: str) -> Dict[str, str]:
    return {
        "attributes": [
            {
                "trait_type": "length",
                "value": str(len(subdomain)),
            }
        ],
        "buttons": [
            {
                "label": "⚙️ Manage",
                "uri": f"https://t.me/tondnsx_bot?startapp=manage__address__0--3A{calculate_nft_address_hash(subdomain, collection_addr_hash)}",
            }
        ],
        "description": f'A .{domain}.ton blockchain domain. TON DNS allows assigning human-readable names to wallets, smart contracts, and websites.'
    }
