from pond import Pond
from .pipelines_factory import pipelines_factory

main_pond = Pond(
    borrowed_timeout=30 * 60,
    time_between_eviction_runs=-1,
    eviction_weight=0.3,
    thread_daemon=True,
)

main_pond.register(pipelines_factory)
