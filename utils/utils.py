import hashlib
from binascii import hexlify

from bitcoinutils.proxy import NodeProxy
from bitcoinutils.ripemd160 import ripemd160

from utils.op_script import OP_CODES


# Bitcoin utils class
class BitcoinUtils:
    @staticmethod
    def newMOfNRedeemScript(m, n, public_keys):
        """Generates M-of-N redeem script
        Parameters
        ----------
        m : int
            the number of keys
        n : int
            the number of keys
        public_keys : PublicKey[]
            the public keys
        """
        if n < 1 or n > 7:
            raise ValueError

        if m < 1 or m > n:
            raise ValueError

        if len(public_keys) != n:
            raise ValueError

        mOPCode = OP_CODES['OP_' + str(m)]
        nOPCode = OP_CODES['OP_' + str(n)]

        script = mOPCode
        for public_key in public_keys:
            # TODO validate public keys
            pkey = bytes.fromhex(public_key)
            script += bytes([len(pkey)])
            script += pkey

        script += nOPCode
        script += OP_CODES['OP_CHECKMULTISIG']
        return script

    @staticmethod
    def hash160(data):
        """Converts a script to it's hash160 equivalent
        RIPEMD160( SHA256( script ) ) - required for P2SH addresses
        """
        if data is None:
            raise ValueError
        hashsha256 = hashlib.sha256(data).digest()
        hash160 = ripemd160(hashsha256)
        return hexlify(hash160).decode('utf-8')

    @staticmethod
    def new_p2pkh_script(b_public_key):
        """ Creates a scriptPubKey for a P2PKH transaction given the destination public key hash
        :param b_public_key: bytes
        :return script_public_key
        """
        script_public_key = OP_CODES['OP_DUP']
        script_public_key += OP_CODES['OP_HASH160']
        script_public_key += bytes([len(b_public_key)])
        script_public_key += b_public_key
        script_public_key += OP_CODES['OP_EQUALVERIFY']
        script_public_key += OP_CODES['OP_CHECKSIG']
        return bytes(script_public_key)

    @staticmethod
    def new_raw_transaction(inputs_transaction_hash, satoshis, b_script_sig, b_script_pub_key):
        """ Create a Bitcoin transaction given input_transaction_hash, output satoshi amount, b_script_sig
        and b_script_pub_key
        :param inputs_transaction_hash: list
        """
        # Version field
        version = bytes.fromhex("01000000")

        # n of inputs (always 1 in our case) // TODO: change to receive more than one
        inputs = bytes.fromhex("01")

        # Input transaction hash
        b_input_tx = bytes.fromhex(inputs_transaction_hash[0])

        # Convert input transaction hash to little-endian form
        input_tx_bytes_reversed = b_input_tx[::-1]

        # Ouput index of input transaction
        out_index = bytes.fromhex("00000000")

        # scriptSig length. To allow scriptSig > 255 bytes, we use variable length integer syntax from protocol spec
        b_script_sig_length = bytes()
        if len(b_script_sig) < 253:
            b_script_sig_length += bytes([len(b_script_sig)])
        else:
            b_script_sig_length += bytearray(3)
            b_script_sig_length += len(b_script_sig).to_bytes(2, byteorder='little')
            b_script_sig_length[1:3] = b_script_sig_length[0:2]
            b_script_sig_length[0] = 253

        # sequence_no. Normally 0xFFFFFFFF. Always in this case.
        sequence = bytes.fromhex("ffffffff")

        # Numbers of outputs for the transaction being created. Always one in this example.
        outputs_count = bytes.fromhex("01")

        b_satoshi = len(satoshis).to_bytes(8, byteorder='little')

        # Lock time field
        lock_time = bytes.fromhex("00000000")

        raw_tx = version
        raw_tx += inputs
        raw_tx += input_tx_bytes_reversed
        raw_tx += out_index
        raw_tx += b_script_sig_length
        raw_tx += b_script_sig
        raw_tx += sequence
        raw_tx += outputs_count
        raw_tx += b_satoshi
        raw_tx += bytes([len(b_script_pub_key)])
        raw_tx += b_script_pub_key
        raw_tx += lock_time

        return raw_tx

    @staticmethod
    def setup_node(user, password, host='127.0.0.1', port=18332):
        return NodeProxy(user, password, host, port).get_proxy()
