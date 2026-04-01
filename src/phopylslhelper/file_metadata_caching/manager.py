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
    def metadata_df(self) -> pd.DataFrame:
        """Concatenation of all non-empty frames in ``metadata_dict``."""
        dfs = [df for df in self.metadata_dict.values() if df is not None and not df.empty]
        if not dfs:
            return pd.DataFrame()
        return pd.concat(dfs, ignore_index=True)


__all__ = ['BaseFileMetadataManager']
