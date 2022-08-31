#!/usr/bin/python3
import json
from datetime import datetime
import pandas as pd


class value:
	def __init__(self, number, unit):
		self.number = number
		self.unit = unit


class value_time(value):
	def __init__(self, patient, number, unit, time):
		super().__init__(number, unit)
		self.patient = patient
		self.time = time


class value_period(value):
	def __init__(self, patient, number, unit, time, end):
		super().__init__(number, unit)
		self.patient = patient
		self.time = time
		self.end = end


class item:
	def __init__(self, name):
		self.name = name
		self.subentries = []
		self.values = []

	def add_subentry(self, name):
		self.subentries.add(item(name))

	def add_value_time(self, patient, number, unit, time):
		self.values.append(value_time(patient, number, unit, time))

	def add_value_period(self, patient, number, unit, time, end):
		self.values.append(value_period(patient, number, unit, time, end))

	def print_content(self):
		for val in self.values:
			try:
				data = {'@type': self.name, '@sourceName': val.patient, '@unit': val.unit, '@startDate':  val.time, '@value': val.number}
				return data
			except:
				data = {'@type': self.name, '@sourceName': val.patient, '@unit': val.unit, '@startDate':  val.time, '@value': val.number}
				return data


def get_entry_index(entity, input_name):
	for i in range(len(entity)):
		if entity[i].name == input_name:
			return i
	else:
		entity.append(item(input_name))
		return -1


def export_json_data(path):
	data = []
	with open(path) as fp:
		print(open)
		for line in fp:
			data.append(json.loads(line))


	items = []
	for line in data:
		test_string = line["code"]["coding"][0]["display"]

		selected_item = items[get_entry_index(items, test_string)]
		if test_string != selected_item.name:
			print("!!!!!!!!!!!!!!!!")

		if "component" in line:
			for component in line["component"]:
				subentry = selected_item.subentries[get_entry_index(selected_item.subentries, component["code"]["text"])]
				subentry.add_value_time(
					line["subject"]["reference"],
					component["valueQuantity"]["value"],
					component["valueQuantity"]["unit"],
					datetime.fromisoformat(line["effectiveDateTime"])
				)
		else:
			try:
				selected_item.add_value_time(
					line["subject"]["reference"],
					line["valueQuantity"]["value"],
					line["valueQuantity"]["unit"],
					datetime.fromisoformat(line["effectiveDateTime"])
				)
			except:
				selected_item.add_value_period(
					line["subject"]["reference"],
					line["valueQuantity"]["value"],
					line["valueQuantity"]["unit"],
					datetime.fromisoformat(line["effectivePeriod"]["start"]),
					datetime.fromisoformat(line["effectivePeriod"]["end"])
				)

	df = pd.DataFrame(columns=['@type', '@sourceName', '@unit', '@startDate', '@value'], dtype=object)
	for i, entry in enumerate(items):
		if entry.subentries:
			for subentry in entry.subentries:
				data = pd.DataFrame(subentry.print_content(), index=[i])
				df = pd.concat([df, data])
		else:
			data = pd.DataFrame(entry.print_content(), index=[i])
			df = pd.concat([df, data])
	return df




