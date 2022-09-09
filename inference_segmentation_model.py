import argparse
import os

import cv2
import numpy as np
import torch
from PIL import Image
from segmentation_models_pytorch import Unet, Linknet, PSPNet, FPN

from data_augment_segmentation import (pre_transforms,
                                       post_transforms_input,
                                       compose)


def inference(model_path, model_name, encoder_name, actvation, test_images_path, output_path):
    """
    Inference script on a saved pytorch model on a dataset in ImageFolder format

    Args:
    model_path: Path to the trained model
    model_name: Either Unet/Linknet/PSPNet/FPN depending on the model
    encoder_name: default efficientnet-b2, depends on your model encoder used
    actvation: default sigmoid, depends on your model activation used
    test_images_path: Path folder for US images to inference
    output_path: Path to save the masks

    Return: None

    """

    transform = compose([pre_transforms(), post_transforms_input()])
    # create output dir if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if model_name == 'Unet':
        model = Unet(encoder_name=encoder_name,
                     encoder_weights='imagenet',
                     in_channels=3,
                     classes=2,
                     activation='sigmoid')
    elif model_name == 'PSPNet':
        model = PSPNet(encoder_name=encoder_name,
                       encoder_weights='imagenet',
                       in_channels=3,
                       classes=1,
                       activation=actvation)
    elif model_name == 'Linknet':
        model = Linknet(encoder_name=encoder_name,
                        encoder_weights='imagenet',
                        in_channels=3,
                        classes=1,
                        activation=actvation)

    elif model_name == 'FPN':
        model = FPN(encoder_name=encoder_name,
                    encoder_weights='imagenet',
                    in_channels=3,
                    classes=1,
                    activation=actvation)
    else:
        model = Linknet(encoder_name=encoder_name,
                        encoder_weights='imagenet',
                        in_channels=3,
                        classes=1,
                        activation=actvation
                        )

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model.eval()
    model.load_state_dict(torch.load(
        model_path, map_location=device)['model_state_dict'])
    model = model.to(device)

    img_path = test_images_path
    with torch.no_grad():
        # for filename in sorted(filter(os.path.isfile, glob.glob(img_path))):
        for filename in os.listdir(img_path):
            maskpath = filename.split(".")[0]
            print(maskpath)
            image_path = os.path.join(output_path, maskpath + ".png")
            filename_p = os.path.join(img_path, filename)

            img = np.asarray(Image.open(filename_p).convert('RGB'))
            height, width, channels = img.shape
            print(img.shape)
            size = (width, height)

            transformed = transform(image=img)
            transformed_image = transformed["image"]
            input_network = transformed_image \
                # .to(device)
            # input_network = torch.from_numpy(transformed_image.reshape((3, 512, 512)))
            # input_network = input_network.float()
            # print(input_network)
            pred = model(input_network[None, ...])
            print(pred.shape)
            mask_pred = (pred[0] <= 0.5)

            device1 = torch.device("cpu")
            mask_pred = mask_pred.to(device1).detach().numpy()

            mask_pred = 255 * np.asarray(mask_pred).astype(np.uint8)
            print(np.unique(mask_pred[0]))
            print(np.unique(mask_pred[1]))

            cv2.imwrite(image_path, mask_pred[0])


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="Inference script for segmentation model")
    PARSER.add_argument('--model_path', type=str,
                        help='Path to trained model',
                        default="best.pth")
    PARSER.add_argument('--model_name', type=str,
                        help='Name of the model type',
                        default='Unet')
    PARSER.add_argument('--encoder_name', type=str,
                        help='Name of the encoder type',
                        default='efficientnet-b2')
    PARSER.add_argument('--actvation', type=str,
                        help='Name of activation type',
                        default='sigmoid')
    PARSER.add_argument('--test_images_path', type=str,
                        help='Path for the test image folder ',
                        default='')
    PARSER.add_argument('--output_masks_path', type=str,
                        help='Path for output prediction masks folder ',
                        default='./output/')
    ARGS = PARSER.parse_args()
    inference(ARGS.model_path, ARGS.model_name, ARGS.encoder_name, ARGS.actvation, ARGS.test_images_path,
              ARGS.output_masks_path)
