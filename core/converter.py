# core/converter.py
import os
from PIL import Image

def convert_image(src_path, dst_dir, target_format, preserve_metadata=True):
    """
    Converts an image file to another format (PNG, JPG, WEBP).
    Handles alpha transparency for JPG conversion by overlaying onto a white background.
    """
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    os.makedirs(dst_dir, exist_ok=True)
    
    # Standardize formats
    fmt = target_format.upper()
    if fmt == "JPG":
        fmt = "JPEG"
        
    base_name = os.path.splitext(os.path.basename(src_path))[0]
    ext = ".jpg" if fmt == "JPEG" else f".{fmt.lower()}"
    dst_path = os.path.join(dst_dir, base_name + ext)
    
    with Image.open(src_path) as img:
        # Prepare saving arguments
        save_args = {}
        
        # Handle EXIF metadata
        if preserve_metadata:
            exif = img.info.get('exif')
            if exif:
                save_args['exif'] = exif
        
        # Handle conversion settings depending on format
        if fmt == "JPEG":
            # JPEG doesn't support alpha transparency (RGBA). Convert to RGB with white background
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                alpha = img.convert("RGBA")
                background = Image.new("RGBA", alpha.size, (255, 255, 255, 255))
                merged = Image.alpha_composite(background, alpha)
                img_to_save = merged.convert("RGB")
            else:
                img_to_save = img.convert("RGB")
                
            save_args['quality'] = 90
        elif fmt == "PNG":
            # PNG is fine with alpha, no special conversion needed
            img_to_save = img
            save_args['optimize'] = True
        elif fmt == "WEBP":
            img_to_save = img
            save_args['quality'] = 85
        else:
            img_to_save = img
            
        img_to_save.save(dst_path, fmt, **save_args)
        
    return dst_path
