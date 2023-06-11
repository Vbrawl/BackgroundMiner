from lib.Encryptor import Encryptor
import sys
import base64

if __name__ == "__main__":
    try:
        KEY = sys.argv[1].encode("UTF-8")
        IV = sys.argv[2].encode("UTF-8")
        f = sys.argv[3]
    except Exception:
        KEY = input("KEY: ").encode("UTF-8")
        IV = input("IV: ").encode('UTF-8')
        f = input("File Path to encrypt: ")
    

    copy = f + '.encrypted'
    with open(f, 'rb') as src, open(copy, 'wb') as dst:
        while (data:=src.read(Encryptor.BLOCK_SIZE)) != b'':
            dst.write(data)




    if KEY == b'' or KEY == b'_':
        KEY = Encryptor.generate_bytes(Encryptor.KEY_SIZE)

    if IV == b'' or IV == b'_':
        IV = Encryptor.generate_bytes(Encryptor.BLOCK_SIZE)

    enc = Encryptor(
        base64.b64decode(KEY),
        base64.b64decode(IV)
    )


    print("KEY:", KEY.decode("UTF-8"))
    print("IV:", IV.decode("UTF-8"))
    enc.encrypt(copy)