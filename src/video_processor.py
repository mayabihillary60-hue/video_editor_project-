"""
Video Processor - Handles all video editing operations using MoviePy
"""

import os
from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from moviepy.video.fx import speedx
import numpy as np

class VideoProcessor:
    def __init__(self):
        self.current_clip = None
        self.temp_files = []
        
    def load_video(self, video_path):
        """Load a video file"""
        try:
            self.current_clip = VideoFileClip(video_path)
            return True, f"Video loaded: {os.path.basename(video_path)}"
        except Exception as e:
            return False, f"Error loading video: {str(e)}"
    
    def get_video_info(self, video_path=None):
        """Get video information"""
        clip = self.current_clip
        if video_path:
            clip = VideoFileClip(video_path)
        
        if clip:
            info = {
                "duration": clip.duration,
                "fps": clip.fps,
                "size": clip.size,
                "width": clip.w,
                "height": clip.h,
                "audio": clip.audio is not None
            }
            if video_path:
                clip.close()
            return info
        return None
    
    def trim_video(self, input_path, output_path, start_time, end_time, callback=None):
        """Trim video from start_time to end_time"""
        try:
            if callback:
                callback(10, "Loading video...")
            
            # Load video
            video = VideoFileClip(input_path)
            
            if callback:
                callback(30, f"Trimming from {start_time}s to {end_time}s...")
            
            # Trim video
            trimmed = video.subclip(start_time, end_time)
            
            if callback:
                callback(70, "Writing output file...")
            
            # Write output
            trimmed.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None
            )
            
            # Clean up
            video.close()
            trimmed.close()
            
            if callback:
                callback(100, "Trim complete!")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def merge_videos(self, video_paths, output_path, callback=None):
        """Merge multiple videos"""
        try:
            clips = []
            total = len(video_paths)
            
            for i, path in enumerate(video_paths):
                if callback:
                    progress = int((i / total) * 50)
                    callback(progress, f"Loading video {i+1}/{total}...")
                
                clip = VideoFileClip(path)
                clips.append(clip)
            
            if callback:
                callback(60, "Concatenating videos...")
            
            # Merge videos
            final = concatenate_videoclips(clips)
            
            if callback:
                callback(80, "Writing output file...")
            
            # Write output
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None
            )
            
            # Clean up
            for clip in clips:
                clip.close()
            final.close()
            
            if callback:
                callback(100, "Merge complete!")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def add_text_overlay(self, input_path, output_path, text, position='center', 
                        fontsize=70, color='white', duration=None, callback=None):
        """Add text overlay to video"""
        try:
            if callback:
                callback(20, "Loading video...")
            
            # Load video
            video = VideoFileClip(input_path)
            
            if callback:
                callback(40, "Creating text overlay...")
            
            # Set duration
            txt_duration = duration if duration else video.duration
            
            # Create text clip
            txt_clip = TextClip(
                text,
                fontsize=fontsize,
                color=color,
                font='Arial'
            )
            
            # Set position and duration
            txt_clip = txt_clip.set_pos(position).set_duration(txt_duration)
            
            if callback:
                callback(60, "Compositing video with text...")
            
            # Composite video and text
            result = CompositeVideoClip([video, txt_clip])
            
            if callback:
                callback(80, "Writing output file...")
            
            # Write output
            result.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None
            )
            
            # Clean up
            video.close()
            txt_clip.close()
            result.close()
            
            if callback:
                callback(100, "Text added successfully!")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def add_audio(self, input_path, audio_path, output_path, volume=1.0, callback=None):
        """Add or replace audio in video"""
        try:
            if callback:
                callback(20, "Loading video...")
            
            # Load video
            video = VideoFileClip(input_path)
            
            if callback:
                callback(40, "Loading audio...")
            
            # Load audio
            audio = AudioFileClip(audio_path)
            
            # Adjust audio volume
            audio = audio.volumex(volume)
            
            if callback:
                callback(60, "Setting audio to video...")
            
            # Set audio to video
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            elif audio.duration < video.duration:
                # Loop audio if shorter
                audio = audio.loop(duration=video.duration)
            
            final = video.set_audio(audio)
            
            if callback:
                callback(80, "Writing output file...")
            
            # Write output
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None
            )
            
            # Clean up
            video.close()
            audio.close()
            final.close()
            
            if callback:
                callback(100, "Audio added successfully!")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def change_speed(self, input_path, output_path, speed_factor, callback=None):
        """Change video speed"""
        try:
            if callback:
                callback(20, "Loading video...")
            
            # Load video
            video = VideoFileClip(input_path)
            
            if callback:
                callback(50, f"Changing speed to {speed_factor}x...")
            
            # Change speed
            final = video.fx(speedx, speed_factor)
            
            if callback:
                callback(80, "Writing output file...")
            
            # Write output
            final.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                temp_audiofile='temp-audio.m4a',
                remove_temp=True,
                logger=None
            )
            
            # Clean up
            video.close()
            final.close()
            
            if callback:
                callback(100, f"Speed changed to {speed_factor}x!")
            
            return True, output_path
        except Exception as e:
            return False, str(e)
    
    def extract_audio(self, input_path, output_path, callback=None):
        """Extract audio from video"""
        try:
            if callback:
                callback(30, "Loading video...")
            
            # Load video
            video = VideoFileClip(input_path)
            
            if callback:
                callback(60, "Extracting audio...")
            
            # Extract audio
            if video.audio:
                video.audio.write_audiofile(
                    output_path,
                    logger=None
                )
                
                if callback:
                    callback(100, "Audio extracted successfully!")
                
                return True, output_path
            else:
                return False, "No audio track found"
        except Exception as e:
            return False, str(e)
        finally:
            if 'video' in locals():
                video.close()
    
    def cleanup(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
        self.temp_files.clear()