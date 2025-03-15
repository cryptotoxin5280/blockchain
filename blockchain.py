import datetime
import hashlib
import rsa
import time

# Transfer of funds between two wallets
class Transaction:
    def __init__(self, amount, payer, payee):
        self.amount = amount
        self.payer = payer
        self.payee = payee

    def __str__(self):
        return str({
            'amount': self.amount,
            'payer': self.payer,
            'payee': self.payee
        })

# Individual block on the blockchain
class Block:
    def __init__(self, prevHash, transaction):
        self.prev_hash = prevHash
        self.transaction = str(transaction)
        self.timestamp = datetime.datetime.now().timestamp()
        self.nonce = int(time.time() * 1000)

    def __str__(self):
        return str({
            'prevHash': self.prev_hash,
            'transaction': self.transaction,
            'timestamp': self.timestamp
        })

    def get_hash(self):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(str(self).encode('utf-8'))
        return sha256_hash.hexdigest()

# The Blockchain
class Chain:
    def __init__(self):
        # Genesis Block
        self.chain = [
            Block(None, Transaction(100, 'genesis', 'mikayla'))
        ]

    def __str__(self):
        return "\n".join([str(block) for block in self.chain])

    # Add a new block to the chain if valid signature & proof of work is complete
    def add_block(self, transaction, sender_public_key, signature):
        is_valid = rsa.verify(transaction.__str__().encode('utf-8'), signature, sender_public_key)
        if is_valid:
            new_block = Block(self.get_last_block().get_hash(), transaction)
            self.mine(new_block.nonce)
            self.chain.append(new_block)

    # Most recent block
    def get_last_block(self):
        return self.chain[-1]

    # Proof of work system
    def mine(self, nonce):
        solution = 1
        print('⛏️ mining...')
        while(True):
            md5_hash = hashlib.md5()
            md5_hash.update(str(nonce + solution).encode('utf-8'))
            attempt = md5_hash.hexdigest()
            if attempt[0:4] == '0000':
                print(f"Solved: {solution}")
                return solution
            solution += 1

# Wallet gives a user a public/private keypair
class Wallet:
    def __init__(self):
        (public_key, private_key) = rsa.newkeys(2048)
        self.private_key = private_key
        self.public_key = public_key
        self.private_key_pem = private_key.save_pkcs1(format='PEM').decode('utf-8')
        self.public_key_pem = public_key.save_pkcs1(format='PEM').decode('utf-8')

    def send_money(self, amount, chain, payee_public_key):
        transaction = Transaction(amount, self.public_key, payee_public_key)
        signature = rsa.sign(transaction.__str__().encode('utf-8'), self.private_key, 'SHA-256')
        chain.add_block(transaction, self.public_key, signature)

# Example Usage
blockchain = Chain()
mikayla = Wallet()
gaius = Wallet()

mikayla.send_money(5.00, blockchain, gaius.public_key)
print(blockchain)
