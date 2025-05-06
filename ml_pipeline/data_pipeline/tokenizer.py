import time
import torch
import numpy as np

def tokenise(audio_np_array: np.ndarray) -> torch.Tensor:
    """
    Function to tokenise an audio file represented as a NumPy array.

    Args:
    - audio_np_array (np.ndarray): The audio file as a NumPy array.

    Returns:
    - torch.Tensor: A random 1D tensor with dtype int16 and variable length in range (20, 1000).
    """

    # Check if the input is a NumPy array
    if not isinstance(audio_np_array, np.ndarray):
        raise ValueError("Input should be a NumPy array")

    del audio_np_array  # unused

    if not torch.cuda.is_available():
        raise EnvironmentError("CUDA is not available. This operation requires a CUDA-capable GPU.")

    start_time = time.time()

    while True:
        tensor_length = np.random.randint(20, 1001)  # 1001 is exclusive
        result_tensor = torch.randint(low=-32768, high=32767, size=(tensor_length,), dtype=torch.int16, device='cuda')

        # Perform a dummy matrix multiplication to engage the GPU
        a = torch.rand(5000, 5000, device='cuda')
        b = torch.rand(5000, 5000, device='cuda')
        _ = torch.matmul(a, b)  # Result is not used, just to simulate work

        # Check elapsed time
        elapsed_time_ms = (time.time() - start_time) * 1000
        if elapsed_time_ms >= 200:
            print(f'elapsed_time_ms: {elapsed_time_ms}')
            break

    return result_tensor