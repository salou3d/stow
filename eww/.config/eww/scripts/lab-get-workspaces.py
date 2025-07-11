#!/usr/bin/env python3

from functools import partial

import json
from os.path import expanduser, join

from wl_framework.network.connection import WaylandConnection
from wl_framework.protocols.base import UnsupportedProtocolError

from wl_framework.protocols.cosmic_workspaces import CosmicWorkspaceManager


class WorkspaceManager(CosmicWorkspaceManager):

	def on_group(self, group):
		#self.log(f"Got new workspace group: {group}")
		#group.create_workspace("foobar")
		pass

	def on_workspace(self, workspace):
		#self.log(f"Got new workspace: {workspace.name}")
		#workspace.activate()
		#self.commit()
		pass

	def on_sync(self):
		grps_ws = []
		for group in self.groups:
			grp = {"id": str(group)}
			ws = []
			for workspace in group.workspaces:
				# self.log(f"\t[Workspace] {workspace.name} " +
					# f"({', '.join(workspace.states)})")
				ws.append(
                    {
                        "name": workspace.name,
                        "states": ', '.join(workspace.states)
                    }
                    )
			grp["workspaces"] = ws
			grps_ws.append(grp)

		with open(join(expanduser("~"), ".config/eww/seww/lab/workspaces.txt"), "a") as fin:
			fin.write( json.dumps(grps_ws) + "\n" )
		fin.close()

		# print(json.dumps(grps_ws))

	def on_workspace_removed(self, workspace):
		#self.log(f"Workspace got removed: {workspace.name}")
		workspace.activate()
		self.commit()

class TestClass(WaylandConnection):

	def on_initial_sync(self, data):
		super().on_initial_sync(data)
		try:
			self.workspaces = WorkspaceManager(self)
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
