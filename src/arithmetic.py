import sys
# OPCODES to use
from btc_framework.bitcoin import OP_2MUL, OP_2DIV, OP_MUL, OP_DIV, OP_MOD, \
                                  OP_NUMEQUAL, OP_NEV, VarInt, OP_EQUAL
# BTC related
from btc_framework.bitcoin import SignableTx, TxInput, TxOutput, script, \
                                    address

if __name__ == "__main__":
    # read params
    keys_base58 = sys.argv[1:]
    keys = [address.WIF.decode(key) for key in keys_base58]
    sign_key = keys[0]

    # transaction related params
    utxo_id = bytes().fromhex(
        "00f2d2be85025d83ef20d8b9eb49b7f82e7d23b1f8c9112a08963cd0479e6650")
    utxo_vout, utxo_value = 0, 50
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
    test_script = script.Script([OP_2MUL, VarInt(26), OP_EQUAL])
    transaction.add_output(TxOutput(test_script, btc=to_pay))

    # sign
    transaction.inputs[0].script.sign(key=sign_key.private_key)

    # return transaction created
    print(transaction)
    print(transaction.serialize().hex())

    print("\n")
    print("SPEND")
    print("\n")
    # SPEND THE PREVIOUS TRANSACTION
    # transaction related params
    utxo_id, utxo_vout, to_pay = transaction.id, 0, to_pay - fees

    # create new transaction
    spendtx = SignableTx()

    # fill transaction
    # add inputs
    spend_script = script.Script([VarInt(13)])
    spendtx.add_input(TxInput(utxo_id, utxo_vout, spend_script))
    # add outputs
    spendtx.add_output(TxOutput(to_pay_addr.script, btc=to_pay))

    # return transaction created
    print(spendtx)
    print(spendtx.serialize().hex())
