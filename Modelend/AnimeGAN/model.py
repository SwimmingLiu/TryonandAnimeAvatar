from io import BytesIO
import torch
from PIL import Image
import os
def anime_model(image_path,save_path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = torch.hub.load("bryandlee/animegan2-pytorch:main", "generator", device=device).eval()
    face2paint = torch.hub.load("bryandlee/animegan2-pytorch:main", "face2paint", device=device)

    im_in = Image.open(image_path).convert("RGB")
    im_out = face2paint(model, im_in, side_by_side=False)
    im_out.save(save_path)