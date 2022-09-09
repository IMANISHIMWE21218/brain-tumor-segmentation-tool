from albumentations import LongestMaxSize, PadIfNeeded, Normalize, Compose, ShiftScaleRotate, IAAPerspective, \
    RandomBrightnessContrast, RandomGamma, HueSaturationValue, JpegCompression
from albumentations.pytorch.transforms import ToTensorV2

BORDER_CONSTANT = 0
BORDER_REFLECT = 2


def pre_transforms(image_size=512):
    # Convert the image to a square of size image_size x image_size
    # (keeping aspect ratio)
    result = [
        LongestMaxSize(max_size=image_size),
        PadIfNeeded(image_size, image_size, border_mode=BORDER_CONSTANT)
    ]

    return result


def post_transforms():
    # we use ImageNet image normalization
    # and convert it to torch.Tensor
    return [Normalize(), ToTensor()]


def compose(_transforms):
    # combine all augmentations into one single pipeline
    result = Compose([item for sublist in _transforms for item in sublist])
    return result


def post_transforms_input():
    result = [
        # Random shifts, stretches and turns with a 50% probability
        # ShiftScaleRotate(
        #     shift_limit=0.1,
        #     scale_limit=0.1,
        #     rotate_limit=15,
        #     border_mode=BORDER_REFLECT,
        #     p=0.5
        # ),
        # IAAPerspective(scale=(0.02, 0.05), p=0.3),
        # Random brightness / contrast with a 30% probability
        RandomBrightnessContrast(
            brightness_limit=0.1, contrast_limit=0.1, p=0.3
        ),
        # Random gamma changes with a 30% probability
        RandomGamma(gamma_limit=(85, 115), p=0.3),
        # Randomly changes the hue, saturation, and color value of the input image
        # HueSaturationValue(p=0.3),
        # JpegCompression(quality_lower=80),
        Normalize(), ToTensorV2(),
    ]

    return result
