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
        "826d472b04e5bca232510370fce3325d6251a950815d5c2c30ec0401866fc0b0")
    utxo_vout, utxo_value = 0, 39.99996160
    fees = 0.005
    to_pay = utxo_value - fees
    to_pay_addr = address.P2PKH(public_key=sign_key.public_key)

    # create new transaction
    transaction = SignableTx()

    # fill transaction
    # add inputs
    in0 = TxInput(utxo_id, utxo_vout, script.sig.P2PKH())
    in0.script.input = in0
    transaction.add_input(in0)

    # add outputs
    test_script = script.Script([OP_0, OP_OR])
    transaction.add_output(TxOutput(to_pay_addr.script, btc=to_pay))

    # sign
    transaction.inputs[0].script.sign(key=sign_key.private_key)

    # return transaction created
    print(transaction)
    print(transaction.serialize().hex())

    """
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
    """
