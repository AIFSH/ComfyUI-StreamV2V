import os
import sys
import time
import folder_paths
import streamv2v
from pydub import AudioSegment
from moviepy.editor import VideoFileClip,AudioFileClip

input_path = folder_paths.get_input_directory()
out_path = folder_paths.get_output_directory()
now_dir = os.path.dirname(os.path.abspath(__file__))

lora_path = os.path.join(now_dir, "lora_weights")
class StreamV2V:
    @classmethod
    def INPUT_TYPES(s):
        face_lora_list = os.listdir(os.path.join(lora_path,"face"))
        style_lora_list = os.listdir(os.path.join(lora_path,"style"))
        return {
            "required": {
                "input_video": ("VIDEO",),
                "prompt":("STRING",{
                    "default": "Elon Musk is giving a talk.",
                    "multiline": True,
                }),
                "face_lora": (face_lora_list+["none"],{
                    "default": "none"
                }),
                "face_lora_weights": ("FLOAT",{
                    "default": 1.,
                    "min": 0.,
                    "max": 1.,
                    "step":0.1,
                    "display": "slider"
                }),
                "style_lora":(style_lora_list+["none"],{
                    "default": "none"
                }),
                "style_lora_weights": ("FLOAT",{
                    "default": 1.,
                    "min": 0.,
                    "max": 1.,
                    "step":0.1,
                    "display": "slider"
                }),
                "model_id":("STRING",{
                    "default": "runwayml/stable-diffusion-v1-5"
                }),
                "scale":("FLOAT",{
                    "default": 1.
                }),
                "guidance_scale":("FLOAT",{
                    "default": 1.
                }),
                "diffusion_steps":("INT",{
                    "default": 4
                }),
                "noise_strength":("FLOAT",{
                    "default": 0.4
                }),
                "acceleration":(["none", "xformers", "tensorrt"],{
                    "default": "xformers"
                }),
                "seed":("INT",{
                    "default": 42
                }),
            }
        }
    
    CATEGORY = "AIFSH_StreamV2V"

    RETURN_TYPES = ("VIDEO",)
    FUNCTION = "generate"

    def generate(self,input_video,prompt,face_lora,face_lora_weights,
                 style_lora,style_lora_weights,
                 model_id,scale,guidance_scale,
                 diffusion_steps,noise_strength,acceleration,seed):
        python_exec = sys.executable or "python"
        parent_directory = os.path.join(now_dir,"StreamV2V","vid2vid")
        video_file = os.path.join(out_path, f"streamv2v_{time.time()}.mp4")
        streamv2v_cmd = f"{python_exec} {parent_directory}/main.py --input {input_video} \
            --prompt '{prompt}' --output_file {video_file} --model_id {model_id} --scale {scale} \
                --guidance_scale {guidance_scale} --diffusion_steps {diffusion_steps} --noise_strength {noise_strength} \
                    --acceleration {acceleration} --feature_similarity_threshold 0.98 --use_denoising_batch --use_cached_attn \
                       --use_feature_injection --feature_injection_strength 0.8 --cache_interval 4 --cache_maxframes 1 \
                        --use_tome_cache --do_add_noise --seed {seed} --face_lora '{face_lora}' --style_lora '{style_lora}'\
                            --style_lora_weights {style_lora_weights} --face_lora_weights {face_lora_weights}"
        
        print(streamv2v_cmd)
        os.system(streamv2v_cmd)
        return(video_file,)


class LoadAudio:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1] in ["wav", "mp3","WAV","flac","m4a"]]
        return {"required":
                    {"audio": (sorted(files),)},
                }

    CATEGORY = "AIFSH_StreamV2V"

    RETURN_TYPES = ("AUDIO",)
    FUNCTION = "load_audio"

    def load_audio(self, audio):
        audio_path = folder_paths.get_annotated_filepath(audio)
        return (audio_path,)

class LoadImagePath:
    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {"required":
                    {"image": (sorted(files), {"image_upload": True})},
                }

    CATEGORY = "AIFSH_StreamV2V"

    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "load_image"
    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)
        return (image_path,)
    
class CombineAudioVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"vocal_AUDIO": ("AUDIO",),
                     "bgm_AUDIO": ("AUDIO",),
                     "video": ("VIDEO",)
                    }
                }

    CATEGORY = "AIFSH_StreamV2V"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO",)

    OUTPUT_NODE = False

    FUNCTION = "combine"

    def combine(self, vocal_AUDIO,bgm_AUDIO,video):
        vocal = AudioSegment.from_file(vocal_AUDIO)
        bgm = AudioSegment.from_file(bgm_AUDIO)
        audio = vocal.overlay(bgm)
        audio_file = os.path.join(out_path,"ip_lap_voice.wav")
        audio.export(audio_file, format="wav")
        cm_video_file = os.path.join(out_path,"voice_"+os.path.basename(video))
        video_clip = VideoFileClip(video)
        audio_clip = AudioFileClip(audio_file)
        new_video_clip = video_clip.set_audio(audio_clip)
        new_video_clip.write_videofile(cm_video_file)
        return (cm_video_file,)


class PreViewVideo:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":{
            "video":("VIDEO",),
        }}
    
    CATEGORY = "AIFSH_StreamV2V"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ()

    OUTPUT_NODE = True

    FUNCTION = "load_video"

    def load_video(self, video):
        video_name = os.path.basename(video)
        video_path_name = os.path.basename(os.path.dirname(video))
        return {"ui":{"video":[video_name,video_path_name]}}

class LoadVideo:
    @classmethod
    def INPUT_TYPES(s):
        files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f)) and f.split('.')[-1] in ["mp4", "webm","mkv","avi"]]
        return {"required":{
            "video":(files,),
        }}
    
    CATEGORY = "AIFSH_StreamV2V"
    DESCRIPTION = "hello world!"

    RETURN_TYPES = ("VIDEO","AUDIO")

    OUTPUT_NODE = False

    FUNCTION = "load_video"

    def load_video(self, video):
        video_path = os.path.join(input_path,video)
        video_clip = VideoFileClip(video_path)
        audio_path = os.path.join(input_path,video+".wav")
        try:
            video_clip.audio.write_audiofile(audio_path)
        except:
            print("none audio")
        return (video_path,audio_path,)