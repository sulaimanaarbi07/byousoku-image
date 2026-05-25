# core/resizer.py
import os
from PIL import Image

def resize_image(src_path, dst_dir, mode, params, keep_aspect=True, preserve_metadata=True):
    """
    Resizes an image using LANCZOS interpolation.
    
    Parameters:
    - src_path: Path to source image
    - dst_dir: Target output directory
    - mode: 'percentage' or 'dimensions' or 'presets'
    - params: Dictionary containing:
        - if percentage: {'percent': int (e.g. 50)}
        - if dimensions/presets: {'width': int, 'height': int}
    - keep_aspect: Keep original aspect ratio (only applies to dimensions/presets)
    """
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))
    
    with Image.open(src_path) as img:
        original_width, original_height = img.size
        
        if mode == 'percentage':
            percent = float(params.get('percent', 100)) / 100.0
            new_width = int(original_width * percent)
            new_height = int(original_height * percent)
            
            # Prevent zero size
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
        elif mode in ('dimensions', 'presets'):
            target_w = int(params.get('width', original_width))
            target_h = int(params.get('height', original_height))
            
            if keep_aspect:
                # Calculate based on maintaining original aspect ratio
                ratio_w = target_w / original_width
                ratio_h = target_h / original_height
                ratio = min(ratio_w, ratio_h)
                
                new_width = int(original_width * ratio)
                new_height = int(original_height * ratio)
            else:
                new_width = target_w
                new_height = target_h
                
            # Prevent zero size
            new_width = max(1, new_width)
            new_height = max(1, new_height)
            
        else:
            new_width, new_height = original_width, original_height
            
        # Resize image using high quality LANCZOS
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Keep format and preserve metadata
        save_args = {}
        if preserve_metadata:
            exif = img.info.get('exif')
            if exif:
                save_args['exif'] = exif
                
        # Preserve original format
        fmt = img.format
        if not fmt:
            # Fallback based on extension
            _, ext = os.path.splitext(src_path.lower())
            if ext in ('.jpg', '.jpeg'):
                fmt = 'JPEG'
            elif ext == '.png':
                fmt = 'PNG'
            elif ext == '.webp':
                fmt = 'WEBP'
            else:
                fmt = 'PNG'
                
        resized_img.save(dst_path, format=fmt, **save_args)
        
    return dst_path
