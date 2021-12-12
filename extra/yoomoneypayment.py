from yoomoney import Client
from yoomoney import Authorize
from yoomoney import Quickpay
import uuid
import extra.main_data as md

class YooMoney(object):
	def __init__(self, label):
		self.token = md.YOOMONEY_TOKEN
		self.card_number = md.YOOMONEY_CARD
		self.label = label


	def check_balance(self):
		client = Client(self.token)
		user = client.account_info()
		print("Account number:", user.account)
		print("Account balance:", user.balance)
		print("Account currency code in ISO 4217 format:", user.currency)
		print("Account status:", user.account_status)
		print("Account type:", user.account_type)
		print("Extended balance information:")
		for pair in vars(user.balance_details):
		    print("\t-->", pair, ":", vars(user.balance_details).get(pair))
		print("Information about linked bank cards:")
		cards = user.cards_linked
		if len(cards) != 0:
		    for card in cards:
		        print(card.pan_fragment, " - ", card.type)
		else:
		    print("No card is linked to the account")


	def make_payment(self, summ):
		self.summ = summ
		quickpay = Quickpay(
            receiver=self.card_number,
            quickpay_form="shop",
            targets="Pay",
            paymentType="SB",
            sum=self.summ,
            label=self.label,
            )
		return quickpay.base_url
		# return quickpay.redirected_url


	def check_payment(self):
		client = Client(self.token)
		history = client.operation_history(label=self.label)
		# print("List of operations:")
		# print("Next page starts with: ", history.next_record)
		for operation in history.operations:
			return operation.status
		#     print()
		#     print("Operation:",operation.operation_id)
		#     print("\tStatus     -->", operation.status)
		#     print("\tDatetime   -->", operation.datetime)
		#     print("\tTitle      -->", operation.title)
		#     print("\tPattern id -->", operation.pattern_id)
		#     print("\tDirection  -->", operation.direction)
		#     print("\tAmount     -->", operation.amount)
		#     print("\tLabel      -->", operation.label)
		#     print("\tType       -->", operation.type)





	# "a1b2c3d4e5"