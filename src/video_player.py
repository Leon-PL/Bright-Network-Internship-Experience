"""A video player class."""
import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.playing_video = None
        self.paused = False
        self.playlists = []

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        print("Here's a list of all available videos:")
        sorted_videos = sorted(self._video_library.get_all_videos(), key=lambda v: v.title)
        if sorted_videos:
            for video in sorted_videos:
                if video.flag_state.flagged:
                    print(f"{video.title} ({video.video_id}) [{video.tags_to_string()}] - FLAGGED (reason: {video.flag_state.reason})")
                else:
                    print(f"{video.title} ({video.video_id}) [{video.tags_to_string()}]")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Cannot play video: Video does not exist")
        else:
            if video.flag_state.flagged:
                print(f"Cannot play video: Video is currently flagged (reason: {video.flag_state.reason})")
                return
            if self.playing_video is None:
                print(f"Playing video: {video.title}")
            else:
                print(f"Stopping video: {self.playing_video.title}")
                print(f"Playing video: {video.title}")

        self.playing_video = video
        self.paused = False

    def stop_video(self):
        """Stops the current video."""
        if self.playing_video is None:
            print("Cannot stop video: No video is currently playing")
        else:
            print(f"Stopping video: {self.playing_video.title}")
            self.playing_video = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()
        non_flagged_videos = [video for video in videos if not video.flag_state.flagged]

        if non_flagged_videos:
            random_video = random.choice(non_flagged_videos)
            self.play_video(random_video.video_id)
        else:
            print("No videos available")

    def pause_video(self):
        """Pauses the current video."""
        if self.playing_video is None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self.paused:
                print(f"Video already paused: {self.playing_video.title}")
            else:
                print(f"Pausing video: {self.playing_video.title}")
            self.paused = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self.playing_video is None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.paused:
                print(f"Continuing video: {self.playing_video.title}")
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""
        if self.playing_video is None:
            print("No video is currently playing")
        else:
            output_string = f"Currently playing: {self.playing_video.title} ({self.playing_video.video_id})" \
                            f" [{self.playing_video.tags_to_string()}]"
            if self.paused:
                print(output_string + " - PAUSED")
            else:
                print(output_string)

    def contains_playlist(self, playlist_name):
        playlists = [playlist for playlist in self.playlists
                     if playlist_name.lower() == playlist.name.lower()]
        return bool(playlists)

    def get_playlist(self, playlist_name):
        playlists = [playlist for playlist in self.playlists
                     if playlist_name.lower() == playlist.name.lower()]
        return playlists[0]

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.contains_playlist(playlist_name):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self.playlists.append(Playlist(playlist_name, videos=[]))
            print(f"Successfully created new playlist: {playlist_name}")


    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        video = self._video_library.get_video(video_id)
        if self.contains_playlist(playlist_name):
            playlist = self.get_playlist(playlist_name)
            if video is None:
                print(f"Cannot add video to {playlist_name}: Video does not exist")
            else:
                if video.flag_state.flagged:
                    print(
                        f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {video.flag_state.reason})")
                    return
                if video in playlist.videos:
                    print(f"Cannot add video to {playlist_name}: Video already added")
                else:
                    print(f"Added video to {playlist_name}: {video.title}")
                    playlist.videos.append(video)
        else:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")


    def show_all_playlists(self):
        """Display all playlists."""
        if self.playlists:
            print("Showing all playlists:")
            for playlist in sorted(self.playlists, key=lambda p: p.name):
                print(playlist.name)
        else:
            print("No playlists exist yet")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.playlists:
            if self.contains_playlist(playlist_name):
                playlist = self.get_playlist(playlist_name)
                print(f"Showing playlist: {playlist_name}")
                if playlist.videos:
                    for video in playlist.videos:
                        if video.flag_state.flagged:
                            print(f"{video.title} ({video.video_id}) [{video.tags_to_string()}] - FLAGGED (reason: {video.flag_state.reason})")
                        else:
                            print(f"{video.title} ({video.video_id}) [{video.tags_to_string()}]")
                else:
                    print("No videos here yet")
        else:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        video = self._video_library.get_video(video_id)
        if self.contains_playlist(playlist_name):
            playlist = self.get_playlist(playlist_name)
            if video is None:
                print(f"Cannot remove video from {playlist_name}: Video does not exist")
            else:
                if video in playlist.videos:
                    print(f"Removed video from {playlist_name}: {video.title}")
                    playlist.videos = [video for video in playlist.videos if video.video_id != video_id]
                else:
                    print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
        else:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.contains_playlist(playlist_name):
            playlist = self.get_playlist(playlist_name)
            playlist.videos.clear()
            print(f"Successfully removed all videos from {playlist_name}")
        else:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if self.contains_playlist(playlist_name):
            self.playlists = [playlist for playlist in self.playlists if playlist_name.lower() != playlist.name.lower()]
            print(f"Deleted playlist: {playlist_name}")
        else:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos = sorted(self._video_library.get_all_videos(), key=lambda v: v.title)
        videos = [video for video in videos if search_term.lower() in video.title.lower()
                  and not video.flag_state.flagged]

        if videos:
            print(f"Here are the results for {search_term}:")
            for i in range(0, len(videos)):
                print(f"{i + 1}) {videos[i].title} ({videos[i].video_id}) [{videos[i].tags_to_string()}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            response = input()
            if response.isnumeric():
                index = int(response)
                if 0 <= index <= len(videos):
                    self.play_video(videos[index-1].video_id)
        else:
            print(f"No search results for {search_term}")


    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        videos = sorted(self._video_library.get_all_videos(), key=lambda v: v.title)
        videos = [video for video in videos if video_tag.lower() in video.tags_to_string().lower()
                  and not video.flag_state.flagged]

        if videos:
            print(f"Here are the results for {video_tag}:")
            for i in range(0, len(videos)):
                print(f"{i + 1}) {videos[i].title} ({videos[i].video_id}) [{videos[i].tags_to_string()}]")
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            response = input()
            if response.isnumeric():
                index = int(response)
                if 0 <= index <= len(videos):
                    self.play_video(videos[index - 1].video_id)
        else:
            print(f"No search results for {video_tag}")

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if video.flag_state.flagged:
                print("Cannot flag video: Video is already flagged")
            else:
                if video is self.playing_video:
                    self.stop_video()
                video.flag_state.update_state(flagged=True, reason=flag_reason)
                print(f"Successfully flagged video: {video.title} (reason: {video.flag_state.reason})")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video = self._video_library.get_video(video_id)
        if video:
            if video.flag_state.flagged:
                video.flag_state.update_state(flagged=False)
                print(f"Successfully removed flag from video: {video.title}")
            else:
                print(f"Cannot remove flag from video: Video is not flagged")
        else:
            print("Cannot remove flag from video: Video does not exist")
