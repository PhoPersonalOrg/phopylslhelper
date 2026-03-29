A simple wrapper/helper for easy loging with pylsl (labstreaminglayer) 

# EasyTimeSync (for LSL Streams)

```python
import pylsl
from pylsl import StreamInfo, StreamOutlet
from attrs import define, field, Factory
from phopylslhelper.easy_time_sync import EasyTimeSyncParsingMixin, readable_dt_str, from_readable_dt_str

```