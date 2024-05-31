import os
import site
now_dir = os.path.dirname(os.path.abspath(__file__))

site_packages_roots = []
for path in site.getsitepackages():
    if "packages" in path:
        site_packages_roots.append(path)
if(site_packages_roots==[]):site_packages_roots=["%s/runtime/Lib/site-packages" % now_dir]
#os.environ["OPENBLAS_NUM_THREADS"] = "4"
for site_packages_root in site_packages_roots:
    if os.path.exists(site_packages_root):
        try:
            with open("%s/streamv2v.pth" % (site_packages_root), "w") as f:
                f.write(
                    "%s\n%s/StreamV2V\n"
                    % (now_dir,now_dir)
                )
            break
        except PermissionError:
            raise PermissionError

if os.path.isfile("%s/streamv2v.pth" % (site_packages_root)):
    print("!!!streamv2v path was added to " + "%s/streamv2v.pth" % (site_packages_root) 
    + "\n if meet `No module` error,try `python main.py` again, don't be foolish to pip install modules")


from .nodes import LoadVideo,PreViewVideo,CombineAudioVideo,StreamV2V,LoadImagePath, LoadAudio
WEB_DIRECTORY = "./web"
# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "LoadAudio": LoadAudio,
    "LoadVideo": LoadVideo,
    "PreViewVideo": PreViewVideo,
    "CombineAudioVideo": CombineAudioVideo,
    "StreamV2V": StreamV2V,
    "LoadImagePath": LoadImagePath
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "streamv2v": "StreamV2V Node",
    "LoadVideo": "Video Loader",
    "PreViewVideo": "PreView Video",
    "CombineAudioVideo": "Combine Audio Video",
    "LoadImagePath": "LoadImagePath",
    "LoadAudio": "AudioLoader"
}
