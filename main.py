from bitcoinutils.keys import PrivateKey, PublicKey, P2pkhAddress
from bitcoinutils.script import Script
from bitcoinutils.transactions import TxInput, TxOutput, Transaction
from bitcoinutils.utils import to_satoshis

from multisig.multisig import MultiSig
from utils.utils import BitcoinUtils


def main():
    try:
        print('Welcome to the Bitcoin multisig wallet!')
        option = option_sel()
        match option:
            case "1":
                print('\nLet\'s create it!')
                multisig()
            case "2":
                print('\nLet\'s do it!')
                spend_from()
            case "3":
                print('\nLet\'s do it!')
                send_to()
            case _:
                print('Ops! invalid option selected!')
    except KeyboardInterrupt:
        print('\nShutdown')


def multisig():
    public_keys = input('\nType public keys separated by comma (,): ')
    arr_pub_keys = public_keys.split(',')
    print_keys(arr_pub_keys)
    min_sig = multisig_sig_required(arr_pub_keys)
    multisig = MultiSig(min_sig, arr_pub_keys)
    print("\nRedeem script hex:", multisig.get_hex_redeem_script())
    print("\nAddress:", multisig.get_address())


def spend_from():
    """ Be aware that you need use the same order used to generate the multisig script
    Note that some public keys will be derided from order of the private keys provided and appended the others public keys
    eg. priv, priv -> pub, pub + others pub keys
    """
    private_keys = input('\nType the signing private keys separated by comma (,): ')
    arr_prv_keys = private_keys.split(',')
    print_keys(arr_prv_keys)
    public_keys = input('\nType the others public keys separated by comma (,) to recreate the redeem script: ')
    arr_pub_keys = public_keys.split(',')
    print_keys(arr_pub_keys)
    p2sh_addr = input('\nType the P2SH address do spend from: ')
    p2pkh_addr = input('\nType the P2PKH address do send to: ')
    print('\nNow, let\'s setup the connection to the node')
    user = input('\nType the rpc user: ')
    password = input('\nType the rpc password: ')
    host = input('\nType the rpc host: ')
    port = input('\nType the rpc port: ')
    node = BitcoinUtils.setup_node(user, password, host, int(port))

    private_keys = []
    p_keys = []
    for prv_key in arr_prv_keys:
        private_key_from_wif = PrivateKey.from_wif(prv_key.strip())
        private_keys.append(private_key_from_wif)
        p_keys.append(private_key_from_wif.get_public_key().to_hex())

    for pub_key in arr_pub_keys:
        p_keys.append(PublicKey.from_hex(pub_key.strip()).to_hex())

    p2sh_multisig = MultiSig(len(arr_prv_keys), p_keys)

    redeem = p2sh_multisig.get_hex_redeem_script()
    print('\nRedeem script is: ', redeem)

    print('\nSearching UTXOs of address:', p2sh_addr)
    unspents = node.scantxoutset('start', ['addr(' + p2sh_addr + ')'])
    UTXOs = unspents['unspents']

    if len(UTXOs) == 0:
        print('\nNo UTXO found for address:', p2sh_addr)
    else:
        print('\nFound:')
        amount = 0
        txin = []
        for idx, unspent in enumerate(UTXOs):
            print('idx', idx, 'unspent', unspent)
            txin.append(TxInput(unspent['txid'], 0))
            amount += unspent['amount']

        # To allow user select the unspent to use.
        # unspent_tx_id = input('\nChoose the unspent to send: ')
        # print('\nYou have selected:', unspent_tx_id)

        script = ['OP_' + str(len(arr_prv_keys))]
        for private_key in p_keys:
            script.append(private_key)
        script.append('OP_' + str(len(p_keys)))
        script.append('OP_CHECKMULTISIG')
        redeem_script = Script(script)
        print('\nRedeem script:', redeem_script)
        print('\nRedeem script hex:', redeem_script.to_hex())
        to_addr = P2pkhAddress(p2pkh_addr)

        txout = TxOutput(to_satoshis(float("0.01852235")), to_addr.to_script_pub_key())
        tx = Transaction(txin, [txout])
        txInBytes = len(bytes.fromhex(tx.serialize()))
        print("\nTransaction Bytes: ", txInBytes)
        feerate = node.estimatesmartfee(6)
        print('\nFee rate at: ', feerate['feerate'])
        fee_rate_tx_in_bytes = feerate['feerate'] * txInBytes
        print("\nAmount to sent: ", amount)
        print("\nFees: ", fee_rate_tx_in_bytes)
        txout_amount = to_satoshis(float(amount) - float(fee_rate_tx_in_bytes))
        print("\nAmount in satoshis to be sent (output): ", txout_amount)
        if txout_amount < 0:
            print("\nInvalid amount -> Amount to sent - fees too small")
            raise ValueError('Invalid amount -> Amount to sent - fees too small')

        txout = TxOutput(txout_amount, to_addr.to_script_pub_key())
        tx = Transaction(txin, [txout])

        # print raw transaction
        print("\nRaw unsigned transaction: " + tx.serialize())

        sigs = []
        for p2pk_sk in private_keys:
            sig = p2pk_sk.sign_input(tx, 0, redeem_script)
            sigs.append(sig)
            print('\nSignature:', sig)

        # OP_0 for Multisig off-by-one error
        # set the scriptSig (unlocking script)
        unlocking_script = ['OP_0']
        for sig in sigs:
            unlocking_script.append(sig)
        unlocking_script.append(redeem_script.to_hex())

        for tx_input in txin:
            tx_input.script_sig = Script(unlocking_script)

        signed_tx = tx.serialize()
        # print raw signed transaction ready to be broadcasted
        print("\nRaw signed transaction:",  signed_tx)
        print("\nTxId:", tx.get_txid())

        decoded_tx = node.decoderawtransaction(signed_tx)
        print('\nDecoded signed transaction: ', decoded_tx)
        confirmation = input('\nConfirm transaction? (y/n): ')
        if confirmation == 'y':
            tx_id = node.sendrawtransaction(signed_tx)
            print('\nTransaction id: ', tx_id)
        else:
            print('\nDone.')

def send_to():
    address = input('\nType the address to send to: ')
    utxo = input('\nType the UTXO to send: ')
    amount = input('\nType the amount: ')
    print('\nNow, let\'s setup the connection to the node')
    user = input('\nType the rpc user: ')
    password = input('\nType the rpc password: ')
    host = input('\nType the rpc host: ')
    port = input('\nType the rpc port: ')
    node = BitcoinUtils.setup_node(user, password, host, int(port))
    # node = BitcoinUtils.setup_node('wgcisotto', 'will00gc', '192.168.1.189', 18332)
    unsigned_tx = node.createrawtransaction(
        [{"vout": 0, "txid": utxo}],
        {address: float(amount)})
    print('\nUnsigned transaction: ', unsigned_tx)
    signed_tx = node.signrawtransactionwithwallet(unsigned_tx)
    if signed_tx['complete']:
        raw_tx = signed_tx['hex']
        print('\nSigned transaction: ', raw_tx)
        decoded_tx = node.decoderawtransaction(raw_tx)
        print('\nDecoded signed transaction: ', decoded_tx)
        confirmation = input('\nConfirm transaction? (y/n): ')
        if confirmation == 'y':
            tx_id = node.sendrawtransaction(raw_tx)
            print('\nTransaction id: ', tx_id)
        else:
            print('\nDone.')
    else:
        print('\nFailed to sign transaction: ', signed_tx['errors'])


def print_keys(arr):
    for i, k in enumerate(arr):
        print('Key ' + str(i) + ': ' + arr[i].strip())


def multisig_sig_required(arr_pub_keys):
    min_sig = input('\nType the number signatures required: ')
    if int(min_sig) > len(arr_pub_keys):
        print('\nOps! invalid option selected!')
        multisig_sig_required(arr_pub_keys)
    return min_sig


def option_sel():
    # So far we only support testnet.
    # TODO: add network selection for futures releases.
    print('(1) - Generate a M-of-N Multisig address')
    print('(2) - Spend from MULTISIG address to a P2PKH address')
    print('(3) - Send to address')
    option = input('\nChoose one option: ')
    try:
        if int(option) < 1 or int(option) > 3:
            return invalid_sel()
    except ValueError:
        return invalid_sel()
    return option


def invalid_sel():
    print('\nInvalid option selected, try again!')
    return option_sel()


if __name__ == '__main__':
    main()
