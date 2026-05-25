# core/batch_processor.py
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .converter import convert_image
from .resizer import resize_image
from .compressor import compress_image
from .heic_converter import convert_heic_image, has_heif

class BatchProcessor:
    def __init__(self):
        self.cancel_event = threading.Event()
        self.executor = None
        self._lock = threading.Lock()
        
    def start_batch(self, files, dst_dir, operation, params, progress_callback=None, complete_callback=None):
        """
        Runs image processing in background threads.
        
        Parameters:
        - files: List of absolute file paths to process.
        - dst_dir: Directory where files should be written.
        - operation: 'convert', 'resize', 'compress', 'heic'
        - params: Dict of configuration values specific to the operation.
        - progress_callback: fn(current, total, success, error, current_filepath)
        - complete_callback: fn(success_count, error_count)
        """
        self.cancel_event.clear()
        
        # Start a background thread to orchestrate the thread pool so the caller's thread is not blocked
        orchestrator = threading.Thread(
            target=self._run_orchestrator,
            args=(files, dst_dir, operation, params, progress_callback, complete_callback),
            daemon=True
        )
        orchestrator.start()
        
    def cancel(self):
        self.cancel_event.set()
        if self.executor:
            self.executor.shutdown(wait=False, cancel_futures=True)
            
    def _run_orchestrator(self, files, dst_dir, operation, params, progress_callback, complete_callback):
        total = len(files)
        success_count = 0
        error_count = 0
        current_idx = 0
        
        if total == 0:
            if complete_callback:
                complete_callback(0, 0)
            return
            
        max_workers = min(os.cpu_count() or 4, 8)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        
        futures = {}
        for file_path in files:
            if self.cancel_event.is_set():
                break
                
            future = self.executor.submit(
                self._process_single_file,
                file_path,
                dst_dir,
                operation,
                params
            )
            futures[future] = file_path
            
        for future in as_completed(futures):
            file_path = futures[future]
            current_idx += 1
            
            if self.cancel_event.is_set():
                error_count += (total - current_idx + 1)
                break
                
            try:
                dst_path = future.result()
                success_count += 1
                status = "success"
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")
                error_count += 1
                status = "error"
                
            if progress_callback:
                progress_callback(
                    current_idx,
                    total,
                    success_count,
                    error_count,
                    file_path
                )
                
        self.executor.shutdown(wait=True)
        self.executor = None
        
        if complete_callback:
            complete_callback(success_count, error_count)
            
    def _process_single_file(self, src_path, dst_dir, operation, params):
        if self.cancel_event.is_set():
            raise InterruptedError("Batch cancelled by user")
            
        # Extract renaming options if available
        rename_pattern = params.get('rename_pattern', '')
        preserve_metadata = params.get('preserve_metadata', True)
        
        final_dst_dir = dst_dir
        
        # If it is a batch process on an entire folder with recursive structure,
        # we might want to preserve the folder structure.
        # But to keep it simple, we save in dst_dir or handle it if relative path specified.
        # For our UI, we write all results directly into the selected output directory.
        
        # 1. Do processing to a temp or straight file path depending on operation
        if operation == 'convert':
            target_format = params.get('target_format', 'PNG')
            out_path = convert_image(src_path, final_dst_dir, target_format, preserve_metadata)
            
        elif operation == 'resize':
            mode = params.get('mode', 'percentage')
            keep_aspect = params.get('keep_aspect', True)
            resize_params = params.get('resize_params', {})
            out_path = resize_image(src_path, final_dst_dir, mode, resize_params, keep_aspect, preserve_metadata)
            
        elif operation == 'compress':
            quality = params.get('quality', 80)
            lossless = params.get('lossless', False)
            out_path = compress_image(src_path, final_dst_dir, quality, lossless)
            
        elif operation == 'heic':
            target_format = params.get('target_format', 'JPG')
            auto_rotate = params.get('auto_rotate', True)
            out_path = convert_heic_image(src_path, final_dst_dir, target_format, auto_rotate)
            
        else:
            raise ValueError(f"Unknown operation: {operation}")
            
        # 2. Apply rename pattern if set and file was successfully created
        if rename_pattern and out_path and os.path.exists(out_path):
            dir_name, full_file_name = os.path.split(out_path)
            file_name_only, ext = os.path.splitext(full_file_name)
            
            # Format pattern: substitute {name} with the original base name (without extension)
            # Safe replacement
            new_name = rename_pattern.replace("{name}", file_name_only)
            
            # Sanitise name for file system
            new_name = re.sub(r'[\\/*?:"<>|]', "", new_name)
            
            if new_name and new_name != file_name_only:
                new_out_path = os.path.join(dir_name, new_name + ext)
                
                # Check for collisions, rename safely if file already exists
                counter = 1
                while os.path.exists(new_out_path):
                    new_out_path = os.path.join(dir_name, f"{new_name}_{counter}{ext}")
                    counter += 1
                    
                os.rename(out_path, new_out_path)
                out_path = new_out_path
                
        return out_path
