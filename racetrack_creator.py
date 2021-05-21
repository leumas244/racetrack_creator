#!/usr/bin/env python3

import sys
import csv
import numpy
import copy
from xml.dom import minidom

TRACK_MODEL = "./models/track.x3d"
TRACK_SEGMENT_MODEL = "./models/track_segment.xml"


def parse_segment_def(segment_def):
    tmp = segment_def.split(',')
    assert len(tmp) == 6

    return {
        'x_coord': float(tmp[0]),
        'y_coord': float(tmp[1]),
        'length': float(tmp[2]),
        'x_rot': float(tmp[3]),
        'y_rot': float(tmp[4]),
        'width': float(tmp[5]),
    }


def create_racetrack():
    # Track Segment Model Schema
    track_segment_model = minidom.parse(TRACK_SEGMENT_MODEL).childNodes[0]
    # General Track Model Schema
    output_track_base = minidom.parse(TRACK_MODEL)

    # Parse street segments
    track_segments = []
    with open(input_file, newline='') as track_def:
        reader = csv.reader(track_def, delimiter=' ', quotechar='|')
        # Parse track segments
        [track_segments.append(parse_segment_def(','.join(line))) for line in reader]

    print("DEBUG: " + str(track_segments))

    for idx, segment in enumerate(track_segments):
        # Construct segment model
        segment_model = copy.deepcopy(track_segment_model)
        segment_model.attributes['DEF'] = 'Strecke%d' % idx
        segment_model.attributes['scale'] = '%f 1 %f' % (segment['width'] / 10, segment['length'] / 20)
        segment_model.attributes['rotation'] = '0 1 0 - %f' % numpy.arctan2(segment['x_rot'], segment['y_rot'])
        segment_model.attributes['translation'] = '%f 1 %f' % (segment['x_coord'], segment['y_coord'])
        # Append to track
        output_track_base.childNodes[1].childNodes[3].appendChild(segment_model)

    # Save track to output file
    with open(output_file, 'w') as output:
        output_track_base.writexml(output)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./racetrack_creator.py <CSV_INPUT_FILE> <XML_OUTPUT_FILE>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    create_racetrack()
