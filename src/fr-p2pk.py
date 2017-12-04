import sys
from btc_framework.bitcoin import OP_AND, OP_DUP, OP_CS, OP_EQUAL, OP_SIZE
from btc_framework.bitcoin import SignableTx, TxInput, TxOutput, script, \
                                    address, ScriptData, VarInt

sig_size = 71
sigmask_r = bytes().fromhex("0000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff00000000000000000000000000000000000000000000000000000000000000000000ff")

fixed_r = bytes().fromhex(
    "5071e1fff985af3cae715f9262973ed0b81c38b409900fccd3802a20e5f1d8")

"""
BTC DER signature format:
30[total-size]02[R-size][R]02[S-size][S][sighash]

30-43
02-1f-5071e1fff985af3cae715f9262973ed0b81c38b409900fccd3802a20e5f1d8
02-20-07c1edf445a58647d768db1e45d38e38f9e6e74589cf60e7d437810445b5346c
01

pubkey script to test:
OP_DUP, <pubkey>, OP_CS,
OP_SIZE, 0x47, OP_EQUAL,
<sigmask>, OP_AND, <r>, OP_EQUAL

sig script to test:
<signature fr>
"""

if __name__ == "__main__":
    # read params
    keys_base58 = sys.argv[1:]
    keys = [address.WIF.decode(key) for key in keys_base58]
    sign_key = keys[0]

    # transaction related params
    utxo_id = bytes().fromhex(
        "bb6f52769d6fd70c66735ccb69bd7f5158abc0df1410f4e81261e0f45c9a33cd")
    utxo_vout, utxo_value = 1, 5
    fees = 0.005
    to_pay = utxo_value - fees
    to_pay_addr = address.P2PKH(public_key=sign_key.public_key)

    pubkey = sign_key.public_key

    # create new transaction
    transaction = SignableTx()

    # fill transaction
    # add inputs
    in0 = TxInput(utxo_id, utxo_vout, script.sig.P2PKH())
    in0.script.input = in0
    transaction.add_input(in0)

    # add outputs
    test_script = script.Script([
                                OP_DUP, ScriptData(pubkey), OP_CS,
                                OP_SIZE, VarInt(sig_size), OP_EQUAL,
                                ScriptData(sigmask_r), OP_AND,
                                ScriptData(fixed_r), OP_EQUAL
                                ])

    transaction.add_output(TxOutput(test_script, btc=to_pay))

    # sign
    transaction.inputs[0].script.sign(key=sign_key.private_key)

    # return transaction created
    print(transaction)
    print(transaction.serialize().hex())

    # SPEND THE PREVIOUS TRANSACTION
    # transaction related params
    utxo_id, utxo_vout, to_pay = transaction.id, 0, to_pay - fees
    # create new transaction
    spendtx = SignableTx()

    # fill transaction
    # add inputs
    ls = []
    spend_script = script.Script(ls)

    in0 = TxInput(utxo_id, utxo_vout, spend_script)
    in0.script.input = in0
    spendtx.add_input(in0)

    signature = spendtx.sign(sign_key.private_key, 0, test_script)
    ls.append(ScriptData(signature))

    # add outputs
    spendtx.add_output(TxOutput(to_pay_addr.script, btc=to_pay))

    # return transaction created
    print(spendtx)
    print(spendtx.serialize().hex())
