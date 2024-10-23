import torch
from trackastra.model import Trackastra, TrackingTransformer
from trackastra.tracking import graph_to_ctc, graph_to_napari_tracks
import os
import tifffile
from pathlib import Path
import numpy as np
import pandas as pd

device = "cuda" if torch.cuda.is_available() else "cpu"

# Base directories
base_img_dir = '/root/vast/mustafa/trackastra/data/lysosomes'
base_mask_dir = '/root/vast/mustafa/trackastra/data/lysosomes'
base_outdir = "/root/vast/mustafa/trackastra/data/lysosomes/tracked"

# model path
use_pretrained = False
# /root/vast/mustafa/trackastra/runs/runs/2024-10-22_06-42-45_leavout-7-1/model.pt
model_path = "/root/vast/mustafa/trackastra/runs/runs/2024-10-22_22-13-13_leavout-9-1/model.pt" if not use_pretrained else None
model_type = "trained" if not use_pretrained else "pretrained"

# dataset_names = ['7-1', '7-2', '7-3','8-1', '8-2', # don't use 8-3 as it has frames with no masks
#                  '9-1', '9-2', '9-3', '10-1', '10-2', '10-3', 
#                  '11-1', '11-2']
dataset_names = ['7-1']

# Dynamically generate input and output directories
input_dirs = [
    {
        'img_dir': f"{base_img_dir}/{name}_individual_tiffs",
        'mask_dir': f"{base_mask_dir}/{name}_individual_tiffs_GT/TRA",
        'outdir': f"{base_outdir}/{name}-tracked-{model_type}",
        'name': name
    }
    for name in dataset_names
]

# Load a pretrained model
if use_pretrained:
    model = Trackastra.from_pretrained("general_2d", device=device)
else:
    m = Path(model_path)
    if m.is_file():
        model = Trackastra.from_folder(
            m.parent,
            device=device,
        )
    else:
        model = Trackastra.from_folder(m.parent)

for dir_set in input_dirs:
    img_dir = dir_set['img_dir']
    mask_dir = dir_set['mask_dir']
    outdir = dir_set['outdir']
    name = dir_set['name']

    # Load images
    img_files = sorted([f for f in os.listdir(img_dir) if f.endswith('.tiff') or f.endswith('.tif')])
    imgs = np.array([tifffile.imread(os.path.join(img_dir, f)) for f in img_files])

    # Load masks
    mask_files = sorted([f for f in os.listdir(mask_dir) if f.endswith('.tiff') or f.endswith('.tif')])
    masks = np.array([tifffile.imread(os.path.join(mask_dir, f)) for f in mask_files])

    # Ensure imgs and masks have the same number of frames
    assert imgs.shape[0] == masks.shape[0], f"Number of image and mask frames don't match for {name}"

    print(f"Processing {name}")
    print(f"Loaded {imgs.shape[0]} frames of images and masks")
    print(f"Image shape: {imgs.shape}")
    print(f"Mask shape: {masks.shape}")

    # Track the cells
    track_graph = model.track(imgs, masks, mode="ilp")  # or mode="ilp", or "greedy_nodiv"

    # Write to cell tracking challenge format
    ctc_tracks, masks_tracked = graph_to_ctc(
        track_graph,
        masks,
        outdir={outdir},
    )

    napari_tracks, napari_tracks_graph, _ = graph_to_napari_tracks(track_graph)
    df = pd.DataFrame(napari_tracks, columns=['TRACK_ID', 'FRAME_ID', 'CENTROID_X', 'CENTROID_Y'])

    # Save CSV with the dataset name appended
    csv_filename = f"{outdir}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved tracking results to {csv_filename}")

print("Processing complete for all datasets.")
