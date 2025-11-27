#!/usr/bin/env python3

import torch
import open_clip
from PIL import Image
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Image classification with OpenCLIP')
    parser.add_argument('-i', '--image', type=str, required=True, help='Path to the image file')
    parser.add_argument('-l', '--labels', type=str, required=True, help='Comma-separated list of labels for classification')
    parser.add_argument('-m', '--model', type=str, default='ViT-B-32', help='Model name (default: ViT-B-32)')
    parser.add_argument('-p', '--pretrained', type=str, default='laion2b_s34b_b79k', help='Pretrained weights (default: laion2b_s34b_b79k)')
    return parser.parse_args()

def main():
    args = parse_args()
    device = "cpu"

    # Split the labels argument on commas to get a list of labels
    labels = [label.strip() for label in args.labels.split(',')]

    # Load model and preprocessing
    model, _, preprocess = open_clip.create_model_and_transforms(
        args.model, 
        pretrained=args.pretrained,
        device=device
    )
    
    tokenizer = open_clip.get_tokenizer(args.model)

    # Tokenize text labels
    text = tokenizer(labels).to(device)

    # Load and preprocess image
    image = preprocess(Image.open(args.image)).unsqueeze(0).to(device)
    
    with torch.no_grad():
        image_features = model.encode_image(image)
        text_features = model.encode_text(text)
        
        # Normalize features
        image_features /= image_features.norm(dim=-1, keepdim=True)
        text_features /= text_features.norm(dim=-1, keepdim=True)
        
        # Calculate similarity
        logits_per_image = (100.0 * image_features @ text_features.T)
        probs = logits_per_image.softmax(dim=-1).cpu().numpy()
        
        max_label, max_value = max(zip(labels, probs[0]), key=lambda x: x[1])

        print(max_label)

if __name__ == '__main__':
    main()
