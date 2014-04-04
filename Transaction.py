#!/usr/bin/python

from User import *

TransactionTypes = ['payment', 'support', 'endorsement', 'coupling', 'inhibition']

class Transaction:
	tType = ''
	duration = 1

class Payment(Transaction):
	def __init__(self, initiator, recipient, amount):
		self.tType = 'payment'
		self.initiator = initiator
		self.recipient = recipient
		self.amount = amount
		self.duration = 1

class Support(Transaction):
	def __init__(self, initiator, recipient, proportion, duration):
		self.tType = 'support'
		self.initiator = initiator
		self.recipient = recipient
		self.proportion = proportion
		self.duration = 2 * duration
