#!/usr/bin/python

from collections import defaultdict

transactionTypes = ['payment', 'support', 'endorsement', 'coupling', 'inhibition']


class User:
	name = ""
	balance = 0
	def __init__(self, name, balance, last_income, last_expenses):
		self.name = name
		self.balance = balance
		self.last_income = last_income
		self.last_expenses = last_expenses
		self.expenses = defaultdict(list)
		self.income = defaultdict(list)
		self.current_income = 0
		self.current_expenses = 0
		self.last_income = 0
		self.last_expenses = 0

