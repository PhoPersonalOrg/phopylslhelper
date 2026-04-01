import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Dict, Any

import pandas as pd
from attrs import define, field, Factory

from PhoPyLSLhelper.src.phopylslhelper.file_metadata_caching.file_metadata import BaseFileMetadataParser


@define(slots=False, eq=False, repr=None)
class BaseFileMetadataManager:
    f"""
    Base manager that holds active metadata for one or more file folders using parsers to produced a combined dataframe in `self.metadata_df` using parsers. 
    Supports caching with configurable datetime columns.

	Usage:

		from phopylslhelper.file_metadata_caching.manager import BaseFileMetadataManager
		from phopylslhelper.file_metadata_caching.video_metadata import VideoMetadataParser
		from phopylslhelper.file_metadata_caching.file_metadata import BaseFileMetadataParser

		video_manager: BaseFileMetadataManager = BaseFileMetadataManager(parse_folders=[Path("M:/ScreenRecordings/EyeTrackerVR_Recordings"), Path("M:/ScreenRecordings/REC_continuous_video_recorder")],
																		parsers={'video': VideoMetadataParser},
		)
		video_manager.metadata_df

    """
    metadata_dict: Dict[str, pd.DataFrame] = field(default=Factory(dict))
    parsers: Dict[str, BaseFileMetadataParser] = field(default=Factory(dict))

    @property
    def metadata_df(self) -> pd.DataFrame:
        """The metadata_df property."""
        return pd.concat(list(self.metadata_dict.values()), ignore_index=True)

