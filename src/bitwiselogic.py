import sys
from btc_framework.bitcoin import OP_AND, OP_OR, OP_XOR, OP_1, OP_0
from btc_framework.bitcoin import SignableTx, TxInput, TxOutput, script, \
                                    address, P2PKHScriptSig


if __name__ == "__main__":
    # read params
    keys_base58 = sys.argv[1:]
    keys = [address.WIF.decode(key) for key in keys_base58]
    sign_key = keys[0]

    # transaction related params
    utxo_id = bytes().fromhex(
        "89851c0a7aa11ff9e75757131870b215937b963c6fb3742ec794eaeefa359aff")
    utxo_num, utxo_value = 0, 50
    fees = 0.005
    to_pay = utxo_value - fees

    # create new transaction
    transaction = SignableTx()

    # fill transaction
    # add inputs
    in_script = P2PKHScriptSig()
    in0 = TxInput(utxo_id, utxo_num, in_script)
    transaction.add_input(in0)
    in0.script.input = in0
    # add outputs
    test_script = script.Script([OP_0, OP_OR])
    to_pay_addr = address.P2PKH(public_key=sign_key.public_key)

    transaction.add_output(TxOutput(to_pay_addr.script, btc=to_pay))

    # sign
    transaction.inputs[0].script.sign(key=sign_key.private_key)

    # return transaction created
    print(transaction)
    print(transaction.serialize().hex())

    # SPEND THE PREVIOUS TRANSACTION
    # transaction related params
    to_pay_addr = address.P2PKH(public_key=sign_key.public_key)
    utxo_id, utxo_num, to_pay = transaction.id, 0, to_pay - fees

    # create new transaction
    spendtx = SignableTx()

    # fill transaction
    # add inputs
    spend_script = script.Script([OP_1])
    spendtx.add_input(TxInput(utxo_id, utxo_num, spend_script))
    # add outputs
    spendtx.add_output(TxOutput(to_pay_addr.script, btc=to_pay))

    # return transaction created
    print(spendtx)
    print(spendtx.serialize().hex())
