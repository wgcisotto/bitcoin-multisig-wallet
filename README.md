# Bitcoin multisig wallet 

Welcome to the Bitcoin multisig wallet! This command line application offers three options for managing your Bitcoin transactions.

To begin run
````commandline
 python main.py 
````

````
Welcome to the Bitcoin multisig wallet!
(1) - Generate a M-of-N Multisig address
(2) - Spend from MULTISIG address to a P2PKH address
(3) - Send to address
````

## Option 1 - Generate a M-of-N Multisig address

To generate a multisig address, use option 1. You will be prompted to enter the following: 
````commandline
Choose one option: 1

Let's create it!

Type public keys separated by comma (,): 0363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e,020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a5,02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259
Key 0: 0363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e
Key 1: 020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a5
Key 2: 02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259

Type the number signatures required: 2
````

The application will then generate a multisig address that requires M signatures out of N possible signers to spend funds.
````commandline
Redeem script hex: 52210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae

Address: 2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw
````

## Option 2 - Spend from MULTISIG address to a P2PKH address

If you have funds in a multisig address and want to spend them, use option 2. You will be prompted to enter the following:

````commandline
Choose one option: 2

Let's do it!

Type the signing private keys separated by comma (,): cNpE7w6TtF2XRdN5Am36cMTuhyU3kyD6NGj7HVfqWkSYWEYsGTzb,cMaoSLrJdVuFcf4M3z6SApQDXi95bnDh7hpqJSLspsswa5xDNCzX
Key 0: cNpE7w6TtF2XRdN5Am36cMTuhyU3kyD6NGj7HVfqWkSYWEYsGTzb
Key 1: cMaoSLrJdVuFcf4M3z6SApQDXi95bnDh7hpqJSLspsswa5xDNCzX

Type the others public keys separated by comma (,) to recreate the redeem script: 02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259
Key 0: 02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259

Type the P2SH address do spend from: 2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw

Type the P2PKH address do send to: mhgy4V9xfeDhBujvvv55dhVPw4FRiepYQr

Now, let's setup the connection to the node

Type the rpc user: user

Type the rpc password: password

Type the rpc host: 127.0.0.1

Type the rpc port: 18332
````

The application will then create a transaction that spends funds from the multisig address and sends them to the destination address.

````commandline
Redeem script is:  52210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae

Searching UTXOs of address: 2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw

Found:
idx 0 unspent {'txid': '2821b9f1b4ef0e6e4af93435257a7091fe7776ff6427c214844dfc87389a5060', 'vout': 0, 'scriptPubKey': 'a914a5ced2922168ba3782d12fb75b7f043700ed0b4887', 'desc': 'addr(2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw)#lau7f5dq', 'amount': Decimal('0.01700468'), 'height': 2424994}

Redeem script: ['OP_2', '0363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e', '020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a5', '02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259', 'OP_3', 'OP_CHECKMULTISIG']

Redeem script hex: 52210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae

Transaction Bytes:  85

Fee rate at:  0.00001000

Amount to sent:  0.01700468

Fees:  0.00085000

Amount in satoshis to be sent (output):  1615468

Raw unsigned transaction: 020000000160509a3887fc4d8414c22764ff7677fe91707a253534f94a6e0eefb4f1b921280000000000ffffffff016ca61800000000001976a91417d50cf8c21a6f61950b0bf1fa5525df8080f48288ac00000000

Signature: 3044022076e47c1e5824e5104fd91ea10ce1206ac00a8c500e2b339de6e8faed59fec54d022014a300c8b5f511563cb200e6652b1c6e4b2542043ea71e431b80d35f50e5c97901

Raw signed transaction: 020000000160509a3887fc4d8414c22764ff7677fe91707a253534f94a6e0eefb4f1b9212800000000b400473044022076e47c1e5824e5104fd91ea10ce1206ac00a8c500e2b339de6e8faed59fec54d022014a300c8b5f511563cb200e6652b1c6e4b2542043ea71e431b80d35f50e5c979014c6952210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953aeffffffff016ca61800000000001976a91417d50cf8c21a6f61950b0bf1fa5525df8080f48288ac00000000

TxId: 09eae27caa5a20c491f9ff522e615fbf2d0a161bca96a484d986d632d310b004

Decoded signed transaction:  {'txid': '09eae27caa5a20c491f9ff522e615fbf2d0a161bca96a484d986d632d310b004', 'hash': '09eae27caa5a20c491f9ff522e615fbf2d0a161bca96a484d986d632d310b004', 'version': 2, 'size': 265, 'vsize': 265, 'weight': 1060, 'locktime': 0, 'vin': [{'txid': '2821b9f1b4ef0e6e4af93435257a7091fe7776ff6427c214844dfc87389a5060', 'vout': 0, 'scriptSig': {'asm': '0 3044022076e47c1e5824e5104fd91ea10ce1206ac00a8c500e2b339de6e8faed59fec54d022014a300c8b5f511563cb200e6652b1c6e4b2542043ea71e431b80d35f50e5c979[ALL] 52210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae', 'hex': '00473044022076e47c1e5824e5104fd91ea10ce1206ac00a8c500e2b339de6e8faed59fec54d022014a300c8b5f511563cb200e6652b1c6e4b2542043ea71e431b80d35f50e5c979014c6952210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae'}, 'sequence': 4294967295}], 'vout': [{'value': Decimal('0.01615468'), 'n': 0, 'scriptPubKey': {'asm': 'OP_DUP OP_HASH160 17d50cf8c21a6f61950b0bf1fa5525df8080f482 OP_EQUALVERIFY OP_CHECKSIG', 'hex': '76a91417d50cf8c21a6f61950b0bf1fa5525df8080f48288ac', 'address': 'mhgy4V9xfeDhBujvvv55dhVPw4FRiepYQr', 'type': 'pubkeyhash'}}]}

Confirm transaction? (y/n): y

Transaction id:  898453bc2f77957b5edab48c84ff2dffb54642d4632d0014d397d2fdd77adb0c
````

*transaction can be found at https://blockstream.info/testnet/tx/898453bc2f77957b5edab48c84ff2dffb54642d4632d0014d397d2fdd77adb0c*

## Option 3 - Send to address

If you want to send Bitcoin from a single address to another address, use option 3. 
You will be prompted to enter the following:

````commandline
Choose one option: 3

Let's do it!

Type the address to send to: 2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw

Type the UTXO to send: a3f9b89d4eb851dc3b57fe054b575aa62cdb6b5c502fa124e579b28b74b0b3a2

Type the amount: 0.01700468

Now, let's setup the connection to the node

Type the rpc user: user

Type the rpc password: password

Type the rpc host: 127.0.0.1

Type the rpc port: 18332
````

The application will then create a transaction that sends the specified amount from the source address to the destination address.

````commandline
Unsigned transaction:  0200000001a2b3b0748bb279e524a12f505c6bdb2ca65a574b05fe573bdc51b84e9db8f9a30000000000ffffffff0174f219000000000017a914a5ced2922168ba3782d12fb75b7f043700ed0b488700000000

Signed transaction:  02000000000101a2b3b0748bb279e524a12f505c6bdb2ca65a574b05fe573bdc51b84e9db8f9a30000000000ffffffff0174f219000000000017a914a5ced2922168ba3782d12fb75b7f043700ed0b4887024730440220386b67bf404c46f781f4e2a88d68e50e3ed807a3f4a5288b2c4e234076b9093202204c7d1db8191f97125351d602797b391b84f99c65eb6a4666b85f890f50b6c96a012102c1adafb8e0d7cdd4a418edc430bbc8b0e3e5fd8953e7e6b9d98e931489bb437e00000000

Decoded signed transaction: {'txid': '2821b9f1b4ef0e6e4af93435257a7091fe7776ff6427c214844dfc87389a5060', 'hash': '9a028ccc309a856a3d303ec33f91c0d68ac2b1da7a7cadc97eeeed9659bab61f', 'version': 2, 'size': 192, 'vsize': 111, 'weight': 441, 'locktime': 0, 'vin': [{'txid': 'a3f9b89d4eb851dc3b57fe054b575aa62cdb6b5c502fa124e579b28b74b0b3a2', 'vout': 0, 'scriptSig': {'asm': '', 'hex': ''}, 'txinwitness': ['30440220386b67bf404c46f781f4e2a88d68e50e3ed807a3f4a5288b2c4e234076b9093202204c7d1db8191f97125351d602797b391b84f99c65eb6a4666b85f890f50b6c96a01', '02c1adafb8e0d7cdd4a418edc430bbc8b0e3e5fd8953e7e6b9d98e931489bb437e'], 'sequence': 4294967295}], 'vout': [{'value': Decimal('0.01700468'), 'n': 0, 'scriptPubKey': {'asm': 'OP_HASH160 a5ced2922168ba3782d12fb75b7f043700ed0b48 OP_EQUAL', 'hex': 'a914a5ced2922168ba3782d12fb75b7f043700ed0b4887', 'address': '2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw', 'type': 'scripthash'}}]}

Confirm transaction? (y/n): y

Transaction id:  2821b9f1b4ef0e6e4af93435257a7091fe7776ff6427c214844dfc87389a5060
````

*transaction can be found at https://blockstream.info/testnet/tx/2821b9f1b4ef0e6e4af93435257a7091fe7776ff6427c214844dfc87389a5060*

## Utils functions 
Generation of an 2-of-3 address.

``
multisig.py main()
``

### Example output

````
Multisig 2-of-3 address:

Role:  Director
Private key WIF compressed: cNpE7w6TtF2XRdN5Am36cMTuhyU3kyD6NGj7HVfqWkSYWEYsGTzb
Private key WIF: 91s83vwhyvUXuhs62JgSjuDSY2vFfxnLLmoF7TS7TgJ7gm848LR
Public key compressed: 0363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e
Public key: 0463b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e2953764d1f6e8ce8728094b575bdf6bfcfd85626d61887924c2d4018b9e95055
Address: mid8SuNxfvEdMZv5waj7JMJcKMvzU7bTkP

Role:  CFO
Private key WIF compressed: cMaoSLrJdVuFcf4M3z6SApQDXi95bnDh7hpqJSLspsswa5xDNCzX
Private key WIF: 91awUVWkR8TLdAywqi2ggqMDMYyfCWH1w5iegJ53uY1feTj1bDc
Public key compressed: 020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a5
Public key: 040e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a5432619beecacdd1ce20b5702e9294a1b3b9b294e4166be6aa263fc344b98aab2
Address: myNkj8JiMg9cMAUUQsdgvA4hkUi5gy3thZ

Role:  COO
Private key WIF compressed: cVnttw4PT3bCMiUTM9nvNm4E5S5ihCFJqjHTrR3zrQQP18TBTpaS
Private key WIF: 93SoebT9FxsLnvoYoFgQRR2dwviQ3JxMMZEhXE9qT9UW14cR6e7
Public key compressed: 02743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259
Public key: 04743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d259f58571650efe472a3e3e5bc491688d017feffe8f0f9bbff14eeebeef8399ef90
Address: mqCSW5JoNNDoGxKxXikZKLGy7QUSXtfSjB

Redeem script hex: 52210363b44e0a2ea75a0be1dc5cf403d493f52d37cc8e00e050153e6fc82a4d11260e21020e573e9e7b79303a37e8f9b69cbb1512213b41dee331543d1d395d980237c1a52102743b49d2de0d5e31fb4ecb7d71ee5496e474e003b2853314205edc244c74d25953ae

Address: 2N8MwFDc4ktP3GXnEbfA4M23ca94krWThPw
````

### Requirements

- Python 3.x
- A running Bitcoin Core node with RPC enabled