#!/usr/bin/python

import random
from User import *
from Transaction import *

ledger = []

ordering = ['payment', 'support', 'endorsement', 'coupling', 'inhibition']

def print_users(users):
	line = ""
	for user in users:
		line += user.name + " - " + str(user.balance) 
		for tx in ordering:
			if(len(user.income[tx]) != 0 or len(user.expenses[tx]) != 0 ):
				line += "  : " + tx + " i: " +str(len(user.income[tx])) + " e: " + str(len(user.expenses[tx]))
		line += " :: "
	print(line)

def update_expense(transactionType, user, transaction):
	if transactionType == 'payment':
		return transaction.amount;
	elif transactionType == 'support':
		value = transaction.proportion * transaction.recipient.last_income
		return value
	elif transactionType == 'endorsement':
		value = 0
		# Expense of endorsement is recipient's last_income?
		# Expense of endorsement this step is recipient's payments summed
		for tx in transaction.recipient.expenses['payment']:
			value += tx.amount * transaction.proportion
		return value
	elif transactionType == 'coupling':
		value = 0
		return value

def update_income(transactionType, user, transaction):
	if transactionType == 'payment':
		#Income from a payment includes endorsers
		# explicit check/early bail unnecessary,
		# will remove once confidence in endorsement handling
		if(len(transaction.initiator.income['endorsement']) == 0):
			return transaction.amount;
		e_value = 0
		for tx in transaction.initiator.income['endorsement']:
			e_value += transaction.amount * tx.proportion
		return e_value + transaction.amount
	elif transactionType == 'support':
		value = transaction.proportion * transaction.recipient.last_income
		return value
	elif transactionType == 'endorsement':
		# No direct income from endorsements
		value = 0
		return value
	elif transactionType == 'coupling':
		value = 0
		return value

def process_users(users):
	for user in users:
		user.current_expense = 0
		user.current_income = 0
		for transactionType in ordering:
			#print(user.name + " ttype: " + transactionType + " un " + str(len(user.expenses[transactionType]))+ " " + str(len(user.income[transactionType]))) 
			current_tx_expense = 0
			current_tx_income = 0
			for entry in user.expenses[transactionType]:
				current_tx_expense += update_expense(transactionType, user, entry)
				#entry.duration -= 1
				#if entry.duration <= 1:
				#	user.expenses[transactionType].remove(entry)
			for entry in user.income[transactionType]:
				current_tx_income += update_income(transactionType, user, entry)
				#entry.duration -= 1
				#if entry.duration <= 1:
				#	user.income[transactionType].remove(entry)
			user.current_expense += current_tx_expense
			user.current_income += current_tx_income
#			if(current_tx_income != 0 or current_tx_expense != 0):
#				print(transactionType + " " + user.name + " CE: " + str(current_tx_expense) + " CI: " + str(current_tx_income) )
		new_balance = user.balance + user.current_income - user.current_expense
#		print(user.name + " BAL: " + str(user.balance) +" NEW BAL: " + str(new_balance) )
		user.balance = new_balance
	for user in users:
		for transactionType in ordering:
			# Making the assumption that every tx is in some user's expenses exactly once
			for entry in user.expenses[transactionType]:
				entry.duration -= 1
				if entry.duration <= 0:
					user.expenses[transactionType].remove(entry)
	for user in users:
		for transactionType in ordering:
			for entry in user.income[transactionType]:
				if entry.duration <= 0:
					user.income[transactionType].remove(entry)

	for user in users:
		user.last_expense = user.current_expense
		user.last_income = user.current_income

# 

def check_users(users):
	total = 0
	for user in users:
		if(user.balance <= 0):
			return False
		else:
			total += user.balance
	print("Total at end of step:" + str(total))
	return True

def run_step(transactions, users):
	if(len(transactions) == 0):
		return False
	for transaction in transactions:
		if transaction.tType == 'payment':
			transaction.initiator.expenses['payment'].append(transaction)
			transaction.recipient.income['payment'].append(transaction)
		elif transaction.tType == 'support':
			transaction.initiator.expenses['support'].append(transaction)
			transaction.recipient.income['support'].append(transaction)
		elif transaction.tType == 'endorsement':
			transaction.initiator.expenses['endorsement'].append(transaction)
			transaction.recipient.income['endorsement'].append(transaction)
		elif transaction.tType == 'coupling':
			transaction.initiator.expenses['coupling'].append(transaction)
			transaction.recipient.income['coupling'].append(transaction)
		else:
			return False
		ledger.append(transaction)
	#Uncomment here to see payments and balances
	#print_users(users)
	process_users(users)
	checkPassed = check_users(users)
	return checkPassed

def run_simulation():
	#users = [User("X",100,0,0), User("Y",200,0,0), User("Z", 100, 0,0)]
	users = generate_users(5, 10)
	transactions = [Payment(users[0], users[1], 25)] 
	run_step(transactions, users)
	print_users(users)
	transactions = [Endorsement(users[2], users[1], .5, 5)]
	run_step(transactions, users)
	print_users(users)
	running = True
	count = 0
	while(running):
		if(random.choice([True, False]) ):
			transactions = [Payment(users[0], users[1], count)]
		else:
			transactions = [Payment(users[1], users[0], count)]
		running = run_step(transactions, users)
		# Uncomment here to see balances & long-duration transactions
		#print_users(users)
		count += 1
			

run_simulation()


def generate_users(num, gini):
	users = []
	for x in range(0,num):
		balance = 100 * random.uniform(0,gini)
		users.append(User("User #" + str(x), balance, 0,0))
	return users
