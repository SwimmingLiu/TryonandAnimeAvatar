import torch
import subprocess
import re


def get_gpu_memory():
    """
    Returns a list of namedtuples of type 'GPUMemory', with the GPU id and its available memory.
    """
    result = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.free', '--format=csv,nounits,noheader'],
                            encoding='utf-8',
                            stdout=subprocess.PIPE)
    gpu_info = result.stdout.strip().split('\n')
    gpu_info = [re.split(r',\s*', x) for x in gpu_info]
    gpu_info = [{"id": int(g[0]), "free_memory": int(g[1])} for g in gpu_info]
    print(gpu_info)
    return gpu_info


def select_gpu(required_memory=5000):
    """
    Selects the GPU with the most available memory above a certain threshold.
    """
    gpu_memory = get_gpu_memory()
    gpu_memory = [g for g in gpu_memory if g["free_memory"] >= required_memory]  # filter out GPUs with insufficient memory
    if not gpu_memory:
        raise RuntimeError("No GPU with sufficient memory found.")
    best_gpu = max(gpu_memory, key=lambda x: x["free_memory"])
    return best_gpu['id']


def main():
    # anime ===> 11000 MB
    # tryon ===> 4000 MB
    selected_gpu = select_gpu(required_memory=5000)  # call with required_memory parameter as needed
    print(f"Selected GPU: {selected_gpu}")

    # Set PyTorch to use the selected GPU
    # torch.cuda.set_device(selected_gpu)

if __name__ == '__main__':
    main()