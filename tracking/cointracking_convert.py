# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import argparse
import os
import shutil
import tqdm
import cv2


def mkdirs(directory, clean=False):
    ''' make directories, optionaly cleaning them before '''
    if clean:
        try:
            shutil.rmtree(directory, ignore_errors=True)
        except Exception as e:
            pass

    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--src', help='cointracking directory', metavar='PATH', required=True)
    return parser.parse_args()

def main(args):
    dst = '../dataset/CTR'
    mkdirs(dst, clean=True)

    ## get the sequence names
    src = os.path.expanduser(args.src)
    img_dir = os.path.join(src, 'images')
    sequences = sorted([f for f in next(os.walk(img_dir))[1]
                        if os.path.isdir(os.path.join(img_dir, f))])

    ## migrate to MDNet structure
    for sequence in tqdm.tqdm(sequences):
        sequence_dst = os.path.join(dst, sequence)
        mkdirs(sequence_dst, clean=False)
        tqdm.tqdm.write(sequence)

        ## find the GT segmentation
        GT_dir = os.path.join(src, 'systematic_extra_segmentations', sequence)
        extensions = set(['.png'])
        segmentations = sorted([f for f in next(os.walk(GT_dir))[2] if os.path.splitext(f)[1] in extensions])
        GT_segmentation_name = segmentations[0]
        GT_seg = cv2.imread(os.path.join(GT_dir, GT_segmentation_name), 0)

        ## convert to bbox
        points = cv2.findNonZero(GT_seg)
        x, y, w, h = cv2.boundingRect(points)

        gt = '{},{},{},{}\n0,0,0,0'.format(x, y, w, h)
        with open(os.path.join(sequence_dst, 'groundtruth_rect.txt'), 'w') as fout:
            fout.write(gt)

        ## copy the images
        img_dst = os.path.join(sequence_dst, 'img')
        if os.path.exists(img_dst):
            shutil.rmtree(img_dst, ignore_errors=True)

        shutil.copytree(os.path.join(src, 'images', sequence), img_dst)

    return 0

if __name__ == '__main__':
    args = parse_arguments()
    sys.exit(main(args))
