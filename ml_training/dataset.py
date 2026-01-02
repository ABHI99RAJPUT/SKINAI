import os
import numpy as np
import cv2

IMG_SIZE = (180, 180)

def load_images_from_folder(folder_path, label):
    images = []
    labels = []

    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)

        if not os.path.isfile(fpath):
            continue

        img = cv2.imread(fpath)
        if img is None:
            continue

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, IMG_SIZE)

        images.append(img)
        labels.append(label)

    return images, labels


def load_dataset(root_dir):
    """
    Loads dataset for VGG19 pipeline.
    Returns: X_images, y_labels, class_names
    """

    class_names = sorted(os.listdir(root_dir))

    all_images = []
    all_labels = []

    for idx, cname in enumerate(class_names):
        path = os.path.join(root_dir, cname)

        if not os.path.isdir(path):
            continue

        imgs, lbls = load_images_from_folder(path, idx)
        all_images.extend(imgs)
        all_labels.extend(lbls)

        print(f"Loaded {len(imgs)} images from {cname}")

    X = np.array(all_images, dtype="float32") / 255.0
    y = np.array(all_labels)

    print("\nDataset Summary:")
    print("Total images:", len(X))
    print("Classes:", class_names)

    return X, y, class_names
