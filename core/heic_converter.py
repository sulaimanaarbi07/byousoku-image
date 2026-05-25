# core/heic_converter.py
import os
from PIL import Image, ImageOps

# Dynamic import to avoid crash if pillow-heif is not installed
has_heif = False
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    has_heif = True
except ImportError:
    pass

def convert_heic_image(src_path, dst_dir, target_format="JPG", auto_rotate=True):
    """
    Converts a HEIC/HEIF image to JPG or PNG using pillow-heif.
    """
    if not has_heif:
        raise ImportError(
            "HEIC support is not available. Please install pillow-heif (pip install pillow-heif)."
        )
        
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    os.makedirs(dst_dir, exist_ok=True)
    
    fmt = target_format.upper()
    if fmt == "JPG":
        fmt = "JPEG"
        
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    ext = ".jpg" if fmt == "JPEG" else ".png"
    dst_path = os.path.join(dst_dir, base_name + ext)
    
    with Image.open(src_path) as img:
        save_args = {}
        
        # Preserve EXIF metadata if possible
        exif = img.info.get('exif')
        if exif:
            save_args['exif'] = exif
            
        img_to_save = img
        
        if auto_rotate:
            # Auto rotate based on EXIF tag 274
            try:
                img_to_save = ImageOps.exif_transpose(img)
            except Exception as e:
                print(f"Error auto-rotating HEIC image: {e}")
                
        # Perform format specific operations
        if fmt == "JPEG":
            if img_to_save.mode in ("RGBA", "LA") or (img_to_save.mode == "P" and "transparency" in img_to_save.info):
                alpha = img_to_save.convert("RGBA")
                background = Image.new("RGBA", alpha.size, (255, 255, 255, 255))
                merged = Image.alpha_composite(background, alpha)
                img_to_save = merged.convert("RGB")
            else:
                img_to_save = img_to_save.convert("RGB")
            save_args['quality'] = 90
        elif fmt == "PNG":
            save_args['optimize'] = True
            
        img_to_save.save(dst_path, fmt, **save_args)
        
    return dst_path
