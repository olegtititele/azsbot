from pyqiwip2p import QiwiP2P
from pyqiwip2p.p2p_types import QiwiCustomer, QiwiDatetime
import extra.main_data as md

class Qiwi(object):
	def __init__(self, label, amount):
		self.QIWI_PRIV_KEY = md.QIWI_PRIV_KEY
		self.p2p = QiwiP2P(auth_key=self.QIWI_PRIV_KEY)
		self.lifetime = 45
		self.label = label
		self.amount = amount
		self.new_bill = self.p2p.bill(bill_id=self.label, amount=self.amount, lifetime=self.lifetime)


	def make_payment(self):
		return self.new_bill.pay_url

	def check_payment(self):
		return self.p2p.check(bill_id=self.new_bill.bill_id).status

