from base58check import b58decode
from bitcoinutils.keys import PrivateKey
from bitcoinutils.setup import setup

from multisig.multisig import MultiSig
from utils.op_script import OP_CODES
from utils.utils import BitcoinUtils

# **NOT USED**
# high-level logic for spending from a P2SH multisig address
def generate_spend_multisig_tx(prv_keys, public_key_hash, multisig, utxos, amount):
    """
    Parameters
    ----------
    prv_keys : list
        list of private keys to sign the transaction

    public_key_hash: str
        address to send the utxo

    multisig: MultiSig
        Object representing a multisig address

    utxos: list
        UTXO id to spent

    amount: string
        amount to send
    """
    # get redeem script in bytes
    setup('testnet')
    b_redeem_script = multisig.get_redeem_script()
    b_public_key = b58decode(public_key_hash)
    b_script_public_key = BitcoinUtils.new_p2pkh_script(b_public_key)
    inputs_transaction_hash = []
    for utxo in utxos:
        inputs_transaction_hash.append(utxo['txid'])
    # TODO: need to calculete the fees
    raw_transaction = BitcoinUtils.new_raw_transaction(inputs_transaction_hash, amount, b_redeem_script, b_script_public_key)
    print(raw_transaction.hex())
    # SIGHASH_ALL in little-endian format to the end of the raw transaction.
    hash_code_type = bytes.fromhex("01000000")
    raw_transaction += hash_code_type

    #b_raw_transaction = new_raw_transaction(utxos, public_key_hash, amount)
    raw_multisig_tx = sign_multisig_tx(raw_transaction, prv_keys, b_script_public_key, b_redeem_script, inputs_transaction_hash, amount)
    print(raw_multisig_tx.hex())


# TODO: move this to the util class
def sign_multisig_tx(raw_transaction, prv_keys, b_script_public_key, b_redeem_script, inputs_transaction_hash, amount):
    # Hash type SIGHASH_ALL
    hash_code_type = bytes.fromhex("01")
    signatures = []
    for prv_key in prv_keys:
        private = PrivateKey.from_wif(prv_key.strip())
        signature = private.sign_message(raw_transaction.hex())
        print('signature: ', signature)
        signatures.append(signature)

    # redeemScript length. To allow redeemScript > 255 bytes, we use OP_PUSHDATA2 and use two bytes to specify length
    if len(b_redeem_script) < 255:
        # OP_PUSHDATA1 specifies next *one byte* will be length to be pushed to stack
        OP_PUSHDATA = OP_CODES['OP_PUSHDATA1']
        b_redeem_script_length_bytes = bytes([len(b_redeem_script)])
    else:
        # OP_PUSHDATA2 specifies next *two bytes* will be length to be pushed to stack
        OP_PUSHDATA = OP_CODES['OP_PUSHDATA2']
        bytes(2)
        b_redeem_script_length_bytes = len(b_redeem_script).to_bytes(2, byteorder='little')

    # OP_0 for Multisig off-by-one error
    script_sig = OP_CODES['OP_0']
    for sig in signatures:
        script_sig += bytes([len(sig.encode()) + 1]) #//PUSH each signature. Add one for hash type byte
        script_sig += sig.encode() # // Signature bytes
        script_sig += hash_code_type # hash type

    script_sig += OP_PUSHDATA #  //OP_PUSHDATA1 or OP_PUSHDATA2 depending on size of redeemScript
    script_sig += b_redeem_script_length_bytes
    script_sig += b_redeem_script

    print('\nScriptSig:', script_sig)
    print('\nScriptSig Hex:', script_sig.hex())

    return BitcoinUtils.new_raw_transaction(inputs_transaction_hash, amount, script_sig, b_script_public_key)


def myTest():
    print(bytes([76]))
    print(OP_CODES['OP_PUSHDATA1'])
    print(bytes([77]))
    print(OP_CODES['OP_PUSHDATA2'])
    print(bytes.fromhex("01"))
    #multi = MultiSig(1, ["02b3de9932e9143f445be472c233b9d90fc5bcb497e67132194d542c345fc1b625", "03f5414970343a6852077465de27828a7c7c2a62519872ce51f61ef4e930138102"])
    #utxos = ["{'txid': 'f11c9887de0fa6955e7c99e2d4de3bfed8a75004424912a544e813a30dfaaf9f', 'vout': 0, 'scriptPubKey': 'a914f1bd0ab73bb81a2c13b8679ba374776cfd9c4c0087', 'desc': 'addr(2NFHRJNdJJYv37FzQQ8kPLAAhnPrA7yALxx)#e3e3huwy', 'amount': Decimal('0.01937235'), 'height': 2424101}"]
    #generate_spend_multisig_tx(["cNurAYess8WSm5da5FnymSeMdecF9QYXQrLuYKr6kC5sdSbnCtSd"], "mhgy4V9xfeDhBujvvv55dhVPw4FRiepYQr", multi, utxos, "0.01937235")

if __name__ == '__main__':
    myTest()

