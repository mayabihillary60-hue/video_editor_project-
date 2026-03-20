"""
Timeline Editor - Handles multi-track timeline editing and keyframe animations
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

@dataclass
class Keyframe:
    """Represents a keyframe for animations"""
    time: float  # Time in seconds
    position: tuple  # (x, y) position
    scale: float  # Scale factor
    rotation: float  # Rotation in degrees
    opacity: float  # Opacity (0-1)
    easing: str = "linear"  # Easing function

@dataclass
class TrackItem:
    """Represents an item on a track (video, audio, text, effect)"""
    id: str
    type: str  # 'video', 'audio', 'text', 'effect'
    source_path: str
    start_time: float  # Start time on timeline
    end_time: float  # End time on timeline
    layer: int  # Layer for compositing (higher = on top)
    keyframes: List[Keyframe] = None
    properties: Dict = None
    
    def __post_init__(self):
        if self.keyframes is None:
            self.keyframes = []
        if self.properties is None:
            self.properties = {}

@dataclass
class Timeline:
    """Represents a complete timeline with multiple tracks"""
    video_tracks: List[List[TrackItem]]  # List of video tracks (each track is a list of items)
    audio_tracks: List[List[TrackItem]]  # List of audio tracks
    duration: float = 0.0
    fps: float = 30.0
    width: int = 1920
    height: int = 1080
    
    def add_video_item(self, item: TrackItem, track_index: int = 0):
        """Add a video item to specified track"""
        while len(self.video_tracks) <= track_index:
            self.video_tracks.append([])
        self.video_tracks[track_index].append(item)
        self._update_duration()
    
    def add_audio_item(self, item: TrackItem, track_index: int = 0):
        """Add an audio item to specified track"""
        while len(self.audio_tracks) <= track_index:
            self.audio_tracks.append([])
        self.audio_tracks[track_index].append(item)
        self._update_duration()
    
    def _update_duration(self):
        """Update timeline duration based on longest item"""
        max_duration = 0
        for track in self.video_tracks:
            for item in track:
                max_duration = max(max_duration, item.end_time)
        for track in self.audio_tracks:
            for item in track:
                max_duration = max(max_duration, item.end_time)
        self.duration = max_duration

class TimelineEditor:
    def __init__(self):
        self.current_timeline = None
        self.preview_clip = None
        
    def create_empty_timeline(self, width=1920, height=1080, fps=30):
        """Create an empty timeline"""
        self.current_timeline = Timeline(
            video_tracks=[[]],
            audio_tracks=[[]],
            width=width,
            height=height,
            fps=fps
        )
        return self.current_timeline
    
    def load_timeline(self, filepath):
        """Load timeline from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Convert dict to dataclass instances
        video_tracks = []
        for track_data in data['video_tracks']:
            track = []
            for item_data in track_data:
                keyframes = [Keyframe(**kf) for kf in item_data.get('keyframes', [])]
                item = TrackItem(
                    id=item_data['id'],
                    type=item_data['type'],
                    source_path=item_data['source_path'],
                    start_time=item_data['start_time'],
                    end_time=item_data['end_time'],
                    layer=item_data['layer'],
                    keyframes=keyframes,
                    properties=item_data.get('properties', {})
                )
                track.append(item)
            video_tracks.append(track)
        
        audio_tracks = []
        for track_data in data.get('audio_tracks', []):
            track = []
            for item_data in track_data:
                item = TrackItem(**item_data)
                track.append(item)
            audio_tracks.append(track)
        
        self.current_timeline = Timeline(
            video_tracks=video_tracks,
            audio_tracks=audio_tracks,
            duration=data.get('duration', 0),
            fps=data.get('fps', 30),
            width=data.get('width', 1920),
            height=data.get('height', 1080)
        )
        return self.current_timeline
    
    def save_timeline(self, filepath):
        """Save timeline to JSON file"""
        if not self.current_timeline:
            return False
        
        # Convert dataclasses to dict
        data = {
            'video_tracks': [],
            'audio_tracks': [],
            'duration': self.current_timeline.duration,
            'fps': self.current_timeline.fps,
            'width': self.current_timeline.width,
            'height': self.current_timeline.height
        }
        
        for track in self.current_timeline.video_tracks:
            track_data = []
            for item in track:
                item_dict = asdict(item)
                track_data.append(item_dict)
            data['video_tracks'].append(track_data)
        
        for track in self.current_timeline.audio_tracks:
            track_data = []
            for item in track:
                item_dict = asdict(item)
                track_data.append(item_dict)
            data['audio_tracks'].append(track_data)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    
    def add_keyframe(self, item_id: str, keyframe: Keyframe):
        """Add a keyframe to an item"""
        if not self.current_timeline:
            return False
        
        # Find item by ID
        for track in self.current_timeline.video_tracks:
            for item in track:
                if item.id == item_id:
                    item.keyframes.append(keyframe)
                    # Sort keyframes by time
                    item.keyframes.sort(key=lambda kf: kf.time)
                    return True
        return False
    
    def get_item_at_time(self, time: float) -> List[TrackItem]:
        """Get all items active at given time"""
        items = []
        if not self.current_timeline:
            return items
        
        for track in self.current_timeline.video_tracks:
            for item in track:
                if item.start_time <= time <= item.end_time:
                    items.append(item)
        
        return items
    
    def render_preview(self, time: float) -> Optional[CompositeVideoClip]:
        """Render preview at specific time"""
        # This is a simplified preview - in production you'd render the actual frame
        active_items = self.get_item_at_time(time)
        if not active_items:
            return None
        
        clips = []
        for item in active_items:
            if item.type == 'video':
                clip = VideoFileClip(item.source_path).subclip(
                    max(0, time - item.start_time),
                    min(item.end_time - item.start_time, item.end_time - item.start_time)
                )
                
                # Apply keyframe animations
                clip = self._apply_keyframes(clip, item, time - item.start_time)
                clips.append(clip)
        
        if clips:
            return CompositeVideoClip(clips)
        return None
    
    def _apply_keyframes(self, clip, item: TrackItem, local_time: float):
        """Apply keyframe animations to clip"""
        if not item.keyframes:
            return clip
        
        # Find surrounding keyframes
        prev_kf = None
        next_kf = None
        for kf in item.keyframes:
            if kf.time <= local_time:
                prev_kf = kf
            if kf.time > local_time and next_kf is None:
                next_kf = kf
        
        if prev_kf and next_kf:
            # Interpolate between keyframes
            t = (local_time - prev_kf.time) / (next_kf.time - prev_kf.time)
            
            # Apply easing
            t = self._apply_easing(t, prev_kf.easing)
            
            # Interpolate values
            x = prev_kf.position[0] + t * (next_kf.position[0] - prev_kf.position[0])
            y = prev_kf.position[1] + t * (next_kf.position[1] - prev_kf.position[1])
            scale = prev_kf.scale + t * (next_kf.scale - prev_kf.scale)
            rotation = prev_kf.rotation + t * (next_kf.rotation - prev_kf.rotation)
            opacity = prev_kf.opacity + t * (next_kf.opacity - prev_kf.opacity)
            
            # Apply transformations
            clip = clip.resize(scale).rotate(rotation)
            clip = clip.set_position((x, y)).set_opacity(opacity)
        
        return clip
    
    def _apply_easing(self, t: float, easing: str) -> float:
        """Apply easing function to time value"""
        if easing == "linear":
            return t
        elif easing == "ease_in":
            return t * t
        elif easing == "ease_out":
            return t * (2 - t)
        elif easing == "ease_in_out":
            return t * t * (3 - 2 * t) if t < 0.5 else (t - 1) * (t - 1) * (3 - 2 * (t - 1)) + 1
        elif easing == "bounce":
            # Simple bounce easing
            if t < 0.5:
                return 4 * t * t
            else:
                return 1 - 4 * (t - 1) * (t - 1)
        else:
            return t
    
    def export_timeline(self, output_path, callback=None):
        """Render entire timeline to video file"""
        if not self.current_timeline:
            return False, "No timeline loaded"
        
        try:
            if callback:
                callback(10, "Preparing timeline...")
            
            # Collect all video clips
            all_clips = []
            total_items = sum(len(track) for track in self.current_timeline.video_tracks)
            processed = 0
            
            for track_idx, track in enumerate(self.current_timeline.video_tracks):
                for item in track:
                    if callback:
                        progress = 10 + int((processed / total_items) * 60)
                        callback(progress, f"Processing clip {processed+1}/{total_items}...")
                    
                    # Load clip
                    clip = VideoFileClip(item.source_path)
                    
                    # Trim to duration
                    clip_duration = item.end_time - item.start_time
                    if clip.duration > clip_duration:
                        clip = clip.subclip(0, clip_duration)
                    
                    # Apply keyframe animations
                    if item.keyframes:
                        clip = self._apply_keyframes_sequence(clip, item)
                    
                    # Set position in timeline
                    clip = clip.set_start(item.start_time)
                    
                    # Set layer
                    if item.layer > 0:
                        clip = clip.set_layer(item.layer)
                    
                    all_clips.append(clip)
                    processed += 1
            
            if callback:
                callback(80, "Compositing video...")
            
            # Composite all clips
            if all_clips:
                final = CompositeVideoClip(all_clips, size=(self.current_timeline.width, self.current_timeline.height))
                final.duration = self.current_timeline.duration
                
                if callback:
                    callback(90, "Writing output file...")
                
                # Write output
                final.write_videofile(
                    output_path,
                    codec='libx264',
                    audio_codec='aac',
                    fps=self.current_timeline.fps,
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    logger=None
                )
                
                if callback:
                    callback(100, "Export complete!")
                
                return True, output_path
            else:
                return False, "No video clips to render"
                
        except Exception as e:
            return False, str(e)
    
    def _apply_keyframes_sequence(self, clip, item: TrackItem):
        """Apply keyframes over entire clip duration"""
        if not item.keyframes:
            return clip
        
        # This would apply keyframe animations over time
        # For now, return clip as-is
        return clip
