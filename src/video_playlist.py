"""A video playlist class."""

from typing import Sequence
from .video import Video


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name: str, videos: Sequence[Video] = []):
        self.name = name
        self.videos = videos

    def contains_video(self, video_id):
        videos = [video for video in self.videos if video_id == video.video_id]
        return bool(videos)
