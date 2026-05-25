# core/compressor.py
import os
import io
from PIL import Image

def compress_image(src_path, dst_dir, quality=80, lossless=False):
    """
    Compresses an image file.
    For JPEG/WEBP, adjusts quality (1-100).
    For PNG, optimizes saving and reduces palettes if lossy, or uses standard optimization if lossless.
    """
    if not os.path.exists(src_path):
        raise FileNotFoundError(f"Source file not found: {src_path}")
        
    os.makedirs(dst_dir, exist_ok=True)
    dst_path = os.path.join(dst_dir, os.path.basename(src_path))
    
    with Image.open(src_path) as img:
        fmt = img.format
        if not fmt:
            _, ext = os.path.splitext(src_path.lower())
            fmt = 'JPEG' if ext in ('.jpg', '.jpeg') else 'PNG'
            
        save_args = {}
        
        # Keep exif metadata
        exif = img.info.get('exif')
        if exif:
            save_args['exif'] = exif
            
        img_to_save = img
        
        if fmt == 'JPEG':
            save_args['quality'] = quality
            save_args['optimize'] = True
        elif fmt == 'WEBP':
            save_args['quality'] = quality
            save_args['lossless'] = lossless
        elif fmt == 'PNG':
            if lossless:
                save_args['optimize'] = True
                save_args['compress_level'] = 9
            else:
                # If lossy PNG compression, we can reduce colors to an 8-bit palette
                # only if the quality is lower than 80.
                if quality < 80:
                    try:
                        img_to_save = img.quantize(colors=min(256, max(16, int(2.5 * quality))))
                    except Exception:
                        pass
                save_args['optimize'] = True
                
        img_to_save.save(dst_path, format=fmt, **save_args)
        
    return dst_path

def estimate_compressed_size(src_path, quality=80, lossless=False):
    """
    Estimates the output size of a compressed image in bytes without writing to disk,
    by saving it to an in-memory BytesIO buffer.
    """
    if not os.path.exists(src_path):
        return 0
        
    try:
        with Image.open(src_path) as img:
            fmt = img.format
            if not fmt:
                _, ext = os.path.splitext(src_path.lower())
                fmt = 'JPEG' if ext in ('.jpg', '.jpeg') else 'PNG'
                
            buffer = io.BytesIO()
            save_args = {}
            
            exif = img.info.get('exif')
            if exif:
                save_args['exif'] = exif
                
            img_to_save = img
            
            if fmt == 'JPEG':
                save_args['quality'] = quality
                save_args['optimize'] = True
            elif fmt == 'WEBP':
                save_args['quality'] = quality
                save_args['lossless'] = lossless
            elif fmt == 'PNG':
                if lossless:
                    save_args['optimize'] = True
                    save_args['compress_level'] = 6  # faster for estimation
                else:
                    if quality < 80:
                        try:
                            img_to_save = img.quantize(colors=min(256, max(16, int(2.5 * quality))))
                        except Exception:
                            pass
                    save_args['optimize'] = True
                    
            img_to_save.save(buffer, format=fmt, **save_args)
            return len(buffer.getvalue())
    except Exception as e:
        print(f"Error estimating size for {src_path}: {e}")
        return os.path.getsize(src_path)
