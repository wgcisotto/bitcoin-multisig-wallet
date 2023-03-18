import hashlib
from binascii import unhexlify

from base58check import b58encode
from bitcoinutils.constants import NETWORK_P2SH_PREFIXES
from bitcoinutils.setup import setup, get_network
from bitcoinutils.keys import PrivateKey, PublicKey

from utils.utils import BitcoinUtils

setup('testnet')


class MultiSig:
    """Represents M-of-N Multisig address.

    Attributes
    ----------
    key : bytes
        M-of-N MultiSig scheme

    Methods
    -------
    get_address()
        returns the corresponding P2PH object
    get_redeem_script()
        return the byte redeem script
    get_redeem_script()
        return the hex redeem script
    """

    def __init__(self, m, public_keys):
        """
        Parameters
        ----------
        m : int
            M in the M-of-N MultiSig scheme
            minimum signatures required to spend UTXO for this address

        public_keys: list
            Public keys, length represents the N in the M-of-N MultiSig scheme
        """
        p_keys = []
        for pk in public_keys:
            p_keys.append(PublicKey.from_hex(pk.strip()))
        redeem_script = BitcoinUtils.newMOfNRedeemScript(int(m), len(public_keys), public_keys)
        self.redeem_script = redeem_script

    def get_hex_redeem_script(self):
        return self.redeem_script.hex()

    def get_redeem_script(self):
        return self.redeem_script

    def get_address(self):
        # Using this hash we create a Bitcoin address
        # OP_HASH160 = The input is hashed twice: first with SHA-256 and then with RIPEMD-160.
        hash160 = BitcoinUtils.hash160(self.redeem_script)
        # Address to String
        hash160_encoded = hash160.encode('utf-8')
        hash160_bytes = unhexlify(hash160_encoded)
        data = NETWORK_P2SH_PREFIXES[get_network()] + hash160_bytes
        data_hash = hashlib.sha256(hashlib.sha256(data).digest()).digest()
        checksum = data_hash[0:4]
        address_bytes = b58encode(data + checksum)
        return address_bytes.decode('utf-8')


def addr_redeem(script):
    # Using this hash we create a Bitcoin address
    # OP_HASH160 = The input is hashed twice: first with SHA-256 and then with RIPEMD-160.
    hash160 = BitcoinUtils.hash160(script)
    # Address to String
    hash160_encoded = hash160.encode('utf-8')
    hash160_bytes = unhexlify(hash160_encoded)
    data = NETWORK_P2SH_PREFIXES[get_network()] + hash160_bytes
    data_hash = hashlib.sha256(hashlib.sha256(data).digest()).digest()
    checksum = data_hash[0:4]
    address_bytes = b58encode(data + checksum)
    address = address_bytes.decode('utf-8')
    return address


def generate_address():
    setup('testnet')
    # create a private key
    # TODO: create own PrivateKey class
    privDirector = PrivateKey()
    privCFO = PrivateKey()
    privCOO = PrivateKey()
    # display keys
    pubDirector = display_keys(privDirector, "Director")
    pubCFO = display_keys(privCFO, "CFO")
    pubCOO = display_keys(privCOO, "COO")
    # create redeem Script from public keys
    script = BitcoinUtils.newMOfNRedeemScript(2, 3,
                                              [pubDirector.to_hex(compressed=True), pubCFO.to_hex(compressed=True),
                                               pubCOO.to_hex(compressed=True)])
    print("\nRedeem script hex:", script.hex())
    address = addr_redeem(script)
    print("\nAddress:", address)


def display_keys(priv, role):
    # display the role
    print("\nRole: ", role)
    # compressed private key
    print("Private key WIF compressed:", priv.to_wif(compressed=True))
    print("Private key WIF:", priv.to_wif(compressed=False))
    # get the public key
    pub = priv.get_public_key()
    # compressed is the default
    print("Public key compressed:", pub.to_hex(compressed=True))
    print("Public key:", pub.to_hex(compressed=False))
    # get address from public key
    address = pub.get_address()
    # print the address default is compressed address
    print("Address:", address.to_string())
    return pub


if __name__ == '__main__':
    generate_address()
