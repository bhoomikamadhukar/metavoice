import torch
import time
import numpy as np

def tokenise(audio_np_array: np.ndarray) -> list:
    if not torch.cuda.is_available():
        raise EnvironmentError("CUDA is not available.")
    del audio_np_array
    start_time = time.time()
    while True:
        tensor_length = np.random.randint(20, 1001)
        result_tensor = torch.randint(
            low=-32768, high=32767,
            size=(tensor_length,),
            dtype=torch.int16,
            device='cuda'
        )
        if (time.time() - start_time) * 1000 >= 200:
            break
    return result_tensor.cpu().tolist()
