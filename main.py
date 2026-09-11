from tracker import add_transaction, save_transactions, load_transactions

if __name__ == '__main__':
    transactions = load_transactions()
    print(transactions)
    add_transaction(transactions, 150000, "Guns")
    save_transactions(transactions)

