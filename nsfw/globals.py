from typing import List, Optional

from nsfw.typings import LogLevel

# misc
skip_download: Optional[bool] = None
log_level: Optional[LogLevel] = None
# execution
execution_providers: List[str] = []

probability_limit: float = 0.8
