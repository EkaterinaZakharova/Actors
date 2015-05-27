import sys
import pykka
import os

class Distributor(pykka.ThreadingActor):

	def on_receive(self, message):
		listf = os.listdir(".")
		for namef in listf:
			print(namef)
		while True:
			namef = input('Enter filename')
			if os.path.isfile(namef):
				break
			print('input error')
		client = Client.start()
		result = client.ask({'filename' : namef})
		client.stop()
		return result


class Client(pykka.ThreadingActor):

	def on_receive(self, message):
		filename = message.get('filename')
		print(filename)
		f = open(filename)
		content = f.read()
		return content

class MainActor(pykka.ThreadingActor):

	def on_receive(self, message):
		Distrib = Distributor.start()
		result = Distrib.ask({})
		Distrib.stop()
		return result

main = MainActor.start()
result=main.ask({})
print(result)
main.stop()
