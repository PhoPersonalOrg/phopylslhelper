from pathlib import Path
from typing import Any, Dict, List, Type

import pandas as pd
from attrs import define, field

from phopylslhelper.file_metadata_caching.file_metadata import BaseFileMetadataParser


@define(slots=False, eq=False)
class BaseFileMetadataManager:
    """
    Base manager that holds metadata for one or more folders using parser classes.
    Produces a combined dataframe in ``metadata_df``. Per-parser caching is handled by each parser.

    Usage:

        from phopylslhelper.file_metadata_caching.manager import BaseFileMetadataManager
        from phopylslhelper.file_metadata_caching.video_metadata import VideoMetadataParser
        from phopylslhelper.file_metadata_caching.file_metadata import BaseFileMetadataParser

        video_manager: BaseFileMetadataManager = BaseFileMetadataManager(parse_folders=[Path("M:/ScreenRecordings/EyeTrackerVR_Recordings"), Path("M:/ScreenRecordings/REC_continuous_video_recorder")],
                                                                        parsers={'video': VideoMetadataParser},
        )
        video_manager.metadata_df

    Optional per-label kwargs (e.g. ``video_extensions``) via ``parser_kwargs={'video': {'video_extensions': ['.mp4']}}``.
    """
    parse_folders: List[Path] = field(factory=list)
    parsers: Dict[str, Type[BaseFileMetadataParser]] = field(factory=dict)
    use_cache: bool = True
    force_rebuild: bool = False
    parser_kwargs: Dict[str, Dict[str, Any]] = field(factory=dict)
    metadata_dict: Dict[str, pd.DataFrame] = field(init=False, factory=dict)


    def __attrs_post_init__(self) -> None:
        folders = [Path(f) for f in self.parse_folders]
        self.metadata_dict = {}
        for label, parser_cls in self.parsers.items():
            extra = dict(self.parser_kwargs.get(label, {}))
            for folder in folders:
                key = f"{label}::{folder.resolve()}"
                self.metadata_dict[key] = parser_cls.parse_folder(folder_path=folder, use_cache=self.use_cache, force_rebuild=self.force_rebuild, **extra)


    @property
    def unfiltered_metadata_df(self) -> pd.DataFrame:
        """Concatenation of all non-empty frames in ``metadata_dict``."""
        dfs = [df for df in self.metadata_dict.values() if df is not None and not df.empty]
        if not dfs:
            return pd.DataFrame()
        # Sort by columns: 'video_start_datetime' (descending), 'video_end_datetime' (descending)
        df = pd.concat(dfs, ignore_index=True).sort_values(['video_start_datetime', 'video_end_datetime'], ascending=[False, False])
        # Filter rows based on column: 'video_duration'
        df = df[df['video_duration'] > 5]
        return df


    @property
    def metadata_df(self) -> pd.DataFrame:
        """Only videos that aren't still recording or invalid."""
        df = self.unfiltered_metadata_df
        # Filter rows based on column: 'video_duration'
        df = df[df['video_duration'] > 5]
        return df


    @property
    def currently_recording_videos_metadata_df(self) -> pd.DataFrame:
        """All videos that are still recording."""
        df = self.unfiltered_metadata_df
        df = df[np.logical_and((df['video_duration'] == 0), (df['video_start_datetime'] == df['video_end_datetime']))]
        return df


    def get_most_recent_videos_df(self, max_num_videos: int = 10) -> pd.DataFrame:
        return self.metadata_df.head(max_num_videos)


    def get_most_recent_video_paths(self, max_num_videos: int = 10) -> List[Path]:
        return self.get_most_recent_videos_df(max_num_videos=max_num_videos)['video_file_path'].tolist()







__all__ = ['BaseFileMetadataManager']
