#!/usr/bin/env python3

import sys
import csv
import numpy
import copy
from xml.dom import minidom

CAR_MODEL = './models/car.xml'
TRACK_MODEL = './models/track.x3d'
TRACK_SEGMENT_MODEL = './models/track_segment.xml'
TRACK_SEGMENT_LENGTH = 20
TRACK_SEGMENT_WIDTH = 10

# Coordinate System
#   Y
#   |
#   |______ X
#  /
# /
# Z
#
# CSV Input Format
# x,z,length,angle,width


def parse_track_segment(segment_obj):
    tmp = segment_obj.split(',')
    # Ensure valid row format
    assert len(tmp) == 5

    # Convert fields to named map
    return {
        'x_coord': float(tmp[0]),
        'z_coord': float(tmp[1]),
        'length': float(tmp[2]) / TRACK_SEGMENT_LENGTH,
        'angle': float(tmp[3]),
        'width': float(tmp[4]) / TRACK_SEGMENT_WIDTH,
    }


def create_racetrack():
    # Car Model Schema
    car_model = minidom.parse(CAR_MODEL).childNodes[0]
    # Track Segment Model Schema
    track_segment_model = minidom.parse(TRACK_SEGMENT_MODEL).childNodes[0]
    # General Track Model Schema
    output_track_base = minidom.parse(TRACK_MODEL)

    # Parse street segments
    track_segments = []
    with open(input_file, newline='') as track_def:
        reader = csv.reader(track_def, delimiter=' ', quotechar='|')
        # Parse track segments
        [track_segments.append(parse_track_segment(','.join(line))) for line in reader]

    # Add car model
    # TODO: uncomment when model is created in 'models/car.xml'
    # output_track_base.childNodes[1].childNodes[3].appendChild(car_model)

    # Add track segments
    for idx, segment in enumerate(track_segments):
        # Construct segment model
        segment_model = copy.deepcopy(track_segment_model)
        segment_model.attributes['DEF'] = 'Strecke %d' % idx
        # TODO: mirror track model
        segment_model.attributes['scale'] = '%f 1 %f' % (segment['width'], segment['length'])
        segment_model.attributes['rotation'] = '0 1 0 %f' % numpy.radians(segment['angle'])
        segment_model.attributes['translation'] = '%f 0 %f' % (segment['x_coord'], segment['z_coord'])
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
