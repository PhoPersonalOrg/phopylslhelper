A simple wrapper/helper for easy loging with pylsl (labstreaminglayer) 

# EasyTimeSync (for LSL Streams)

```python
import pylsl
from pylsl import StreamInfo, StreamOutlet
from attrs import define, field, Factory
from phopylslhelper.easy_time_sync import EasyTimeSyncParsingMixin, readable_dt_str, from_readable_dt_str

@define(slots=False)
class EmotivBase(EasyTimeSyncParsingMixin):
    READ_SIZE: int = field(default=32)
    serial_number: str = field(default=None)
	...

    def __attrs_post_init__(self):
        self.init_EasyTimeSyncParsingMixin()


    def add_lsl_outlet_info_common(self, info: StreamInfo) -> StreamInfo:
        """ adds common LSL metadata
        """
        # Add some metadata
        info.desc().append_child_value("manufacturer", "emotiv_lsl")
        info.desc().append_child_value("version", "0.1.4")
        info.desc().append_child_value("description", "Logged by the open-source tool 'emotiv_lsl' to record raw data from Emotiv headsets.")
        ## add a custom timestamp field to the stream info:
        info = self.EasyTimeSyncParsingMixin_add_lsl_outlet_info(info=info)
        return info
    


    def get_lsl_outlet_eeg_stream_info(self) -> StreamInfo:
        """Create LSL stream for EEG sensor data"""
        info = self.add_lsl_outlet_info_common(info=info)
        return info

    def get_lsl_outlet_motion_stream_info(self) -> StreamInfo:
        """Create LSL stream info for motion sensor data (accelerometer + gyroscope)"""
        info = self.add_lsl_outlet_info_common(info=info)
        return info
    


    def main_loop(self):
        import hid

        # Create EEG outlet
        eeg_outlet = None 

        # Create motion outlet if the device supports it
        motion_outlet = None
        if self.has_motion_data and self.enable_motion_data:
            motion_outlet = StreamOutlet(self.get_lsl_outlet_motion_stream_info())
            print(f'Setup motion outlet')
            
        # Create motion outlet if the device supports it
        raw_packet_outlet = None
        if self.is_reverse_engineer_mode:
            raw_packet_outlet = StreamOutlet(self.get_lsl_outlet_raw_debugging_stream_info())
            print(f'Setup raw_packet_outlet (for reverse-engineering)')
            
        eeg_quality_outlet = None



```