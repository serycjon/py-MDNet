# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
import argparse
import os
import json
import csv


def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--cointracking_dir', help='cointracking base directory', required=True)
    parser.add_argument('--dst', help='output directory', required=True)
    return parser.parse_args()

def main(args):
    ## get the sequence names
    cointracking_base = os.path.expanduser(args.cointracking_dir)
    dst = os.path.expanduser(args.dst)
    img_dir = os.path.join(cointracking_base, 'images')
    sequences = sorted([f for f in next(os.walk(img_dir))[1]
                        if os.path.isdir(os.path.join(img_dir, f))])

    mdnet_results = '../result'
    for sequence in sequences:
        mdnet_res_file = os.path.join(mdnet_results, sequence, 'result.json')
        if not os.path.exists(mdnet_res_file):
            print('{} results not available'.format(sequence))
            continue

        with open(mdnet_res_file, 'r') as fin:
            mdnet_res = json.loads(fin.read())
        bboxes = mdnet_res['res']

        extensions = set(['.jpg'])
        img_dir = os.path.join(cointracking_base, 'images', sequence)
        images = sorted([f for f in next(os.walk(img_dir))[2] if os.path.splitext(f)[1] in extensions])

        assert len(bboxes) == len(images)

        out_file = os.path.join(dst, '{}.csv'.format(sequence))
        with open(out_file, 'wb') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

            for i, image in enumerate(images):
                image_number = int(os.path.splitext(image)[0])
                bbox = bboxes[i]
                csv_writer.writerow([i, bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3], -1, -1, 0])

    return 0

if __name__ == '__main__':
    args = parse_arguments()
    sys.exit(main(args))
