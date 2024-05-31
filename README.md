# ComfyUI-StreamV2V
the comfyui custom node of [StreamV2V](https://github.com/Jeff-LiangF/streamv2v)
<div>
  <figure>
  <img alt='webpage' src="web.png?raw=true" width="600px"/>
  <figure>
</div>

## How to use
make sure `ffmpeg` is worked in your commandline
for Linux
```
apt update
apt install ffmpeg
```
for Windows,you can install `ffmpeg` by [WingetUI](https://github.com/marticliment/WingetUI) automatically

then!
```
git clone https://github.com/AIFSH/ComfyUI-StreamV2V.git
cd ComfyUI-StreamV2V
pip install -r requirements.txt

## insatll xformers match your torch,for torch==2.1.0+cu121
pip install xformers==0.0.22.post7
pip install accelerate 
```
weights will be downloaded from huggingface automaticly!

## Tutorial
- [Demo](https://www.bilibili.com/video/BV12m42157Us)

## WeChat Group && Donate
<div>
  <figure>
  <img alt='Wechat' src="wechat.jpg?raw=true" width="300px"/>
  <img alt='donate' src="donate.jpg?raw=true" width="300px"/>
  <figure>
</div>
    
## Thanks
- [StreamV2V](https://github.com/Jeff-LiangF/streamv2v)
