#!/usr/bin/env python3

from functools import partial

import json

from wl_framework.network.connection import WaylandConnection
from wl_framework.protocols.base import UnsupportedProtocolError
from wl_framework.protocols.foreign_toplevel import ForeignTopLevel

class ToplevelManager(ForeignTopLevel):
	def __init__(self, wl_connection):
		super().__init__(wl_connection)

	def on_toplevel_created(self, toplevel):
		pass

	def on_toplevel_synced(self, toplevel):
		windows = []
		for window in self.windows:
			states = []
			for state in self.windows[window].states:
				states.append(state)
			# print(str(window) + ": " + self.windows[window].title + ' ' + str(states))

			windows.append(
				{
					"id": window,
					"app_idd": self.windows[window].app_id,
					"title": self.windows[window].title,
					"states": states
					# "outputs": list(self.windows[window].outputs)
				}
				)

		# print( json.dumps( {"clients": windows} ) )

		with open("../seww/lab/clients.txt", "a") as fin:
			fin.write( json.dumps( {"clients": windows} ) + "\n" )
		fin.close()

	def on_toplevel_closed(self, toplevel):
		pass


class TestClass(WaylandConnection):

	def on_initial_sync(self, data):
		super().on_initial_sync(data)
		try:
			self.workspaces = ToplevelManager(self)
		except UnsupportedProtocolError as e:
			self.log(e)
			self.shutdown()

if __name__ == '__main__':

	import sys
	from wl_framework.loop_integrations import PollIntegration
	loop = PollIntegration()

	try:
		app = TestClass(eventloop_integration=loop)
	except RuntimeError as e:
		print(e)
		sys.exit(1)
	try:
		loop.run()
	except KeyboardInterrupt:
		print()
