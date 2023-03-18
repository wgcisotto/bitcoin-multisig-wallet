# Bitcoin's op codes.
# Added only OP_CODE needed. Complete list at: https://en.bitcoin.it/wiki/Script
OP_CODES = {
    # constants
    'OP_0': b'\x00',
    'OP_1': b'\x51',
    'OP_2': b'\x52',
    'OP_3': b'\x53',
    'OP_4': b'\x54',
    'OP_5': b'\x55',
    'OP_6': b'\x56',
    'OP_7': b'\x57',
    'OP_PUSHDATA1': b'\x4c',
    'OP_PUSHDATA2': b'\x4d',
    # bitwise logic
    'OP_EQUALVERIFY': b'\x88',
    # crypto
    'OP_CHECKMULTISIG': b'\xae',
    'OP_HASH160': b'\xa9',
    'OP_CHECKSIG': b'\xac',
    # stack
    'OP_DUP': b'\x76'
}
