from typing import Dict, List, Tuple, Optional, Callable, Union, Any
from enum import Enum, auto


class DataModalityType(Enum):
    """The various types of datastreams produced by my recorder and analyzed.
    from phopylslhelper.core.data_modalities import DataModalityType

    """
    EEG = auto()
    MOTION = auto()
    PHO_LOG_TO_LSL = auto()
    WHISPER = auto()
    # PHO_LOG_TO_LSL = auto()

    def __str__(self):
        return self.name
    
    @classmethod
    def list_values(cls):
        """Returns a list of all enum values"""
        return list(cls)

    @classmethod
    def list_names(cls):
        """Returns a list of all enum names"""
        return [e.name for e in cls]


    @classmethod
    def get_stream_name_to_modality_dict(cls) -> Dict:
        stream_name_to_modality_dict = {'Epoc X': cls.EEG, 'Epoc X Motion':cls.MOTION, 'Epoc X eQuality':None, 'TextLogger': cls.PHO_LOG_TO_LSL, 'EventBoard': cls.PHO_LOG_TO_LSL}
        return stream_name_to_modality_dict


lab_recorder_to_mne_to_type_dict = {'EEG':'eeg', 'ACC':'eeg', 'GYRO':'eeg', 'RAW': 'eeg'} # 'RAW' for eeg quality
stream_name_to_modality_dict = {'Epoc X': DataModalityType.EEG, 'Epoc X Motion':DataModalityType.MOTION, 'Epoc X eQuality':None, 'TextLogger': DataModalityType.PHO_LOG_TO_LSL, 'EventBoard': DataModalityType.PHO_LOG_TO_LSL}

