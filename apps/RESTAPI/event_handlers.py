from injector import Injector

from domain.misc import EventBus
from domain.posts.events import PostCreated
from domain.wall.projections import WallProjection
from infrastructure.EventBus.projection_event_handler import build_projection_event_handler


def user_event_handlers(injector: Injector, event_bus: EventBus):
    event_bus.subscribe(**build_projection_event_handler(injector, PostCreated, WallProjection))
