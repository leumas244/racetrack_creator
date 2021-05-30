# racetrack_creator
Simple command line utility to create a simulink track model from a csv track definition

### Usage
`python3 ./racetrack_creator.py <CSV_INPUT_FILE> <XML_OUTPUT_FILE>"`

`CSV_INPUT_FILE` is the track definition in csv format like `example/track_definition.csv`
`XML_OUTPUT_FILE` is the filename as which the newly created track should be saved

### CSV Input Format
Coordinate System
<pre>
  Y
  |
  |______ X
 /
/
Z
</pre>

CSV Input Format  
`x,z,length,e_x,e_y,width`

### Notes
Some non default packages where used, a virtual python environment might be beneficial