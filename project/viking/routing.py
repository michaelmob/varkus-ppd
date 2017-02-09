from channels.routing import include


channel_routing = [
	include("controlpanel.routing.routes", path=r"^/ws/cp"),
	include("lockers.routing.routes", path=r"^/ws/lockers"),
]