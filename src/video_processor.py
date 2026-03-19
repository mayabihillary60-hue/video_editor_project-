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

# Add these imports at the top of video_processor.py if not already there
from moviepy.video.fx import fadein, fadeout, gamma_correction, mirror_x, mirror_y
from moviepy.video.fx.resize import resize
from moviepy.video.fx.rotate import rotate
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

# Add these methods inside the VideoProcessor class
def apply_filter(self, input_path, output_path, filter_type, intensity=1.0, callback=None):
    """Apply visual filters to video"""
    try:
        if callback:
            callback(10, "Loading video...")
        
        # Load video
        video = VideoFileClip(input_path)
        
        if callback:
            callback(30, f"Applying {filter_type} filter...")
        
        # Apply selected filter
        if filter_type == "grayscale":
            processed = video.fx(lambda gf, t: np.dot(gf(t)[..., :3], [0.299, 0.587, 0.114])[..., np.newaxis].repeat(3, axis=2) / 255.0)
        
        elif filter_type == "sepia":
            def sepia_filter(get_frame, t):
                frame = get_frame(t)
                sepia_frame = np.dot(frame[..., :3], [[0.393, 0.349, 0.272],
                                                       [0.769, 0.686, 0.534],
                                                       [0.189, 0.168, 0.131]])
                return np.clip(sepia_frame, 0, 255).astype('uint8')
            processed = video.fl(sepia_filter)
        
        elif filter_type == "negative":
            processed = video.fx(lambda gf, t: 255 - gf(t))
        
        elif filter_type == "brightness":
            factor = 1.0 + (intensity * 0.5)
            processed = video.fx(lambda gf, t: np.clip(gf(t) * factor, 0, 255).astype('uint8'))
        
        elif filter_type == "contrast":
            factor = 1.0 + (intensity * 1.5)
            def contrast_filter(get_frame, t):
                frame = get_frame(t).astype(float)
                mean = np.mean(frame[..., :3], axis=(0, 1), keepdims=True)
                adjusted = mean + (frame[..., :3] - mean) * factor
                new_frame = frame.copy()
                new_frame[..., :3] = np.clip(adjusted, 0, 255)
                return new_frame.astype('uint8')
            processed = video.fl(contrast_filter)
        
        elif filter_type == "blur":
            def blur_filter(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame)
                for _ in range(int(intensity * 3)):
                    img = img.filter(ImageFilter.BLUR)
                return np.array(img)
            processed = video.fl(blur_filter)
        
        elif filter_type == "sharpen":
            def sharpen_filter(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame)
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(1.0 + intensity * 2)
                return np.array(img)
            processed = video.fl(sharpen_filter)
        
        elif filter_type == "edge_detect":
            def edge_filter(get_frame, t):
                frame = get_frame(t)
                img = Image.fromarray(frame).convert('L')
                edges = img.filter(ImageFilter.FIND_EDGES)
                return np.array(edges.convert('RGB'))
            processed = video.fl(edge_filter)
        
        elif filter_type == "pixelate":
            def pixelate_filter(get_frame, t):
                frame = get_frame(t)
                h, w = frame.shape[:2]
                pixel_size = max(5, int(20 * intensity))
                small = Image.fromarray(frame).resize((w//pixel_size, h//pixel_size), Image.NEAREST)
                return np.array(small.resize((w, h), Image.NEAREST))
            processed = video.fl(pixelate_filter)
        
        elif filter_type == "vintage":
            def vintage_filter(get_frame, t):
                frame = get_frame(t).astype(float)
                # Apply sepia tone
                sepia = np.dot(frame[..., :3], [[0.393, 0.349, 0.272],
                                               [0.769, 0.686, 0.534],
                                               [0.189, 0.168, 0.131]])
                # Add vignette effect
                h, w = sepia.shape[:2]
                Y, X = np.ogrid[:h, :w]
                center_y, center_x = h/2, w/2
                mask = np.sqrt((Y - center_y)**2 + (X - center_x)**2)
                mask = 1 - (mask / mask.max()) * 0.3
                sepia = sepia * mask[..., np.newaxis]
                return np.clip(sepia, 0, 255).astype('uint8')
            processed = video.fl(vintage_filter)
        
        else:
            processed = video
        
        if callback:
            callback(70, "Writing output file...")
        
        # Write output
        processed.write_videofile(
            output_path,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            logger=None
        )
        
        # Clean up
        video.close()
        processed.close()
        
        if callback:
            callback(100, f"{filter_type} filter applied!")
        
        return True, output_path
    except Exception as e:
        return False, str(e)

def add_transition(self, video1_path, video2_path, output_path, transition_type="fade", duration=1.0, callback=None):
    """Add transition between two videos"""
    try:
        if callback:
            callback(10, "Loading videos...")
        
        # Load videos
        clip1 = VideoFileClip(video1_path)
        clip2 = VideoFileClip(video2_path)
        
        if callback:
            callback(30, f"Applying {transition_type} transition...")
        
        # Apply transition based on type
        if transition_type == "fade":
            # Fade out first clip, fade in second
            clip1_fade = fadeout(clip1, duration)
            clip2_fade = fadein(clip2, duration)
            
            # Crossfade
            transition = CompositeVideoClip([
                clip1_fade,
                clip2_fade.set_start(clip1.duration - duration)
            ])
            final = concatenate_videoclips([clip1_fade, clip2_fade])
        
        elif transition_type == "slide":
            # Slide transition (simplified)
            # For complex transitions, we'd need more sophisticated compositing
            final = concatenate_videoclips([clip1, clip2])
        
        elif transition_type == "wipe":
            # Wipe transition (simplified)
            final = concatenate_videoclips([clip1, clip2])
        
        elif transition_type == "zoom":
            # Zoom transition
            clip1_zoom = clip1.resize(lambda t: 1 + 0.5 * (t / clip1.duration))
            clip2_zoom = clip2.resize(lambda t: 1 - 0.5 * (t / clip2.duration))
            final = concatenate_videoclips([clip1_zoom, clip2_zoom])
        
        else:
            final = concatenate_videoclips([clip1, clip2])
        
        if callback:
            callback(70, "Writing output file...")
        
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
        clip1.close()
        clip2.close()
        final.close()
        
        if callback:
            callback(100, "Transition applied!")
        
        return True, output_path
    except Exception as e:
        return False, str(e)

def add_effects_chain(self, input_path, output_path, effects_list, callback=None):
    """Apply multiple effects in sequence"""
    try:
        current_input = input_path
        temp_files = []
        
        for i, (effect_type, params) in enumerate(effects_list):
            if callback:
                progress = int((i / len(effects_list)) * 80)
                callback(progress, f"Applying effect {i+1}/{len(effects_list)}...")
            
            # Create temp file for this effect
            temp_output = f"temp_effect_{i}.mp4"
            temp_files.append(temp_output)
            
            # Apply effect based on type
            if effect_type == "filter":
                success, _ = self.apply_filter(
                    current_input, temp_output, params['filter_type'], 
                    params.get('intensity', 1.0), None
                )
            elif effect_type == "speed":
                success, _ = self.change_speed(
                    current_input, temp_output, params['speed'], None
                )
            elif effect_type == "text":
                success, _ = self.add_text_overlay(
                    current_input, temp_output, params['text'],
                    params.get('position', 'center'),
                    params.get('fontsize', 70),
                    params.get('color', 'white'),
                    None
                )
            else:
                success = False
            
            if not success:
                return False, f"Failed at effect {i+1}"
            
            current_input = temp_output
        
        if callback:
            callback(90, "Finalizing...")
        
        # Copy final result to output
        import shutil
        shutil.copy2(current_input, output_path)
        
        # Clean up temp files
        for temp in temp_files:
            if os.path.exists(temp):
                os.remove(temp)
        
        if callback:
            callback(100, "Effects chain completed!")
        
        return True, output_path
    except Exception as e:
        return False, str(e)