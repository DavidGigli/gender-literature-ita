
def lista_nomi(path):

	import csv

	my_list = []

	with open(path, encoding="utf-8", errors='ignore') as csv_to_read:
		# print(csv_to_read)# instantiate a csv reader object, specifying the delimiter and quote characters
		my_reader = csv.reader(csv_to_read)
		for row in my_reader:
			my_list.append(row[0].lower())
		my_list.sort()
		# print(my_list)

		my_new_list = []
		for item in my_list:
			if item not in my_new_list:
				my_new_list.append(item)
		return(my_new_list)
