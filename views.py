from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from web3 import Web3, HTTPProvider
from web3.exceptions import TransactionNotFound
import json

balance = 2500
web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
abi = [
    {
        "inputs": [],
        "name": "payLarge",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "payMedium",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "paySmall",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdrawAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            }
        ],
        "name": "withdrawFunds",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
contract_address = "0xfeB974c4e11C57444b36d1F4bB4EDE243FF3F6Be"
if not web3.is_connected():
    raise Exception("Cannot connect to ganache.")
contract = web3.eth.contract(address=contract_address, abi=abi)


@require_POST
@csrf_exempt
def update_balance(request):
    global balance
    data = json.loads(request.body)
    balance = float(data.get('balance'))


def show_refill_page(request):
    return render(request, "refill.html")


def show_roulette_page(request):
    global balance
    return render(request, 'roulette.html', {'balance_from': balance})


def withdraw(request):
    global balance
    return render(request, 'withdraw.html', {'balance_from': balance})


def submit_withdrawal(request):
    global balance
    # Ensure this is a POST request
    print(int(web3.eth.get_balance(contract_address))/1000000000000000000)
    if request.method != 'POST':
        return HttpResponse("Invalid request", status=400)

    try:
        # Преобразование суммы из Ether в Wei
        value = int(request.POST.get('amount'))  # Сумма в Ether

        # Корректировка локального баланса
        balance -= value
        value *= 1000000000000000
        # Подготовка транзакции
        transaction = contract.functions.withdrawFunds(value).build_transaction({
            'from': web3.eth.accounts[0],
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei'),
            'nonce': web3.eth.get_transaction_count(web3.eth.accounts[0])
        })

        # Подписание транзакции секретным ключом
        private_key = '0x6b7952821c49860da55e3d85b4cb0b9576133ec3e7ab1288f9e671d11ee08925'  # Замените на свой секретный ключ
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

        # Отправка транзакции
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Ожидание квитанции о транзакции
        web3.eth.wait_for_transaction_receipt(txn_hash)

        return HttpResponse("Withdrawal successful")

    except TransactionNotFound:
        print('TransactionNotFound')
        return HttpResponse("Transaction not found", status=500)
    except Exception as e:
        print(e)
        return HttpResponse("An error occurred", status=500)


def top_up_small(request):
    global balance
    amount = request.POST.get('amount')
    if int(amount) == 500:
        transaction = contract.functions.paySmall().transact({
            'from': web3.eth.accounts[0],
            'value': 500000000000000000  # 0.5 ETH
        })
        try:
            web3.eth.wait_for_transaction_receipt(transaction)
            balance += 500
        except TransactionNotFound:
            print('TransactionNotFound')
    return HttpResponseRedirect('refill')


def top_up_medium(request):
    global balance
    amount = request.POST.get('amount')
    if int(amount) == 1000:
        transaction = contract.functions.payMedium().transact({
            'from': web3.eth.accounts[0],
            'value': 1000000000000000000  # 1 ETH
        })
        try:
            web3.eth.wait_for_transaction_receipt(transaction)
            balance += 1000
        except TransactionNotFound:
            print('TransactionNotFound')
    return HttpResponseRedirect('refill')


def top_up_large(request):
    global balance
    amount = int(request.POST.get('amount'))
    transaction = contract.functions.payLarge().transact({
        'from': web3.eth.accounts[0],
        'value': 2500000000000000000  # 2.5 ETH
    })
    try:
        web3.eth.wait_for_transaction_receipt(transaction)
        balance += 2500
    except TransactionNotFound:
        print('TransactionNotFound')
    return HttpResponseRedirect('refill')


def handle_other_post_requests(request):
    # Обработка других POST запросов
    pass


"""
class ContractNDViews(TemplateView):
    def __init__(self, **kwargs):
        self.balance = 2500
        self.web3 = Web3(HTTPProvider('http://127.0.0.1:8545'))
        self.abi = [
            {
                "inputs": [],
                "name": "payLarge",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "payMedium",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "paySmall",
                "outputs": [],
                "stateMutability": "payable",
                "type": "function"
            },
            {
                "inputs": [],
                "name": "withdrawAll",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "_amount",
                        "type": "uint256"
                    }
                ],
                "name": "withdrawFunds",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [],
                "name": "owner",
                "outputs": [
                    {
                        "internalType": "address",
                        "name": "",
                        "type": "address"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ]
        self.contract_address = "0xaE7966A02Bae26e02852B95417086f873912E183"
        if not self.web3.is_connected():
            raise Exception("Cannot connect to ganache.")
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.abi)

    def get(self, request, *args, **kwargs):
        if 'refill' in request.path:
            return render(request, "refill.html")
        else:
            return render(request, 'roulette.html', {'balance_from': self.balance})

    def post(self, request, *args, **kwargs):
        if 'top_up' in request.path:
            data = request.POST.get('amount')
            if int(data) == 500:
                transaction = self.contract.functions.paySmall().transact({
                    'from': self.web3.eth.accounts[0],
                    'value': 500000000000000000  # 1 ETH
                })
                try:
                    self.web3.eth.wait_for_transaction_receipt(transaction)
                    self.balance += float(data)
                except TransactionNotFound:
                    print('TransactionNotFound')
            elif int(data) == 1000:
                transaction = self.contract.functions.payMedium().transact({
                    'from': self.web3.eth.accounts[0],
                    'value': 1000000000000000000  # 1 ETH
                })
                try:
                    self.web3.eth.wait_for_transaction_receipt(transaction)
                    self.balance += data
                    self.balance += float(data)
                except TransactionNotFound:
                    print('TransactionNotFound')
            else:
                transaction = self.contract.functions.payLarge().transact({
                    'from': self.web3.eth.accounts[0],
                    'value': 2500000000000000000  # 1 ETH
                })
                try:
                    self.web3.eth.wait_for_transaction_receipt(transaction)
                    self.balance += float(data)
                except TransactionNotFound:
                    print('TransactionNotFound')
            return HttpResponseRedirect('refill')
        elif 'withdraw':
            pass"""
