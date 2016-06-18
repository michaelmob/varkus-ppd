from channels.routing import include

channel_routing = [
	include("apps.cp.routing.routes", path=r"^/ws/cp"),
	include("apps.lockers.routing.routes", path=r"^/ws/lockers"),
]