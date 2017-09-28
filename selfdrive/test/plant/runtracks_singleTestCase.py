#!/usr/bin/env python
import sys
import time, json

from selfdrive.test.plant import plant
from selfdrive.config import Conversions as CV, CruiseButtons as CB
from maneuver import *

maneuvers = [
  Maneuver(
    'approaching a 40mph car while cruising at 60mph from 100m away', 
    duration=30., 
    initial_speed = 60. * CV.MPH_TO_MS, 
    lead_relevancy=True, 
    initial_distance_lead=100., 
    speed_lead_values = [40.*CV.MPH_TO_MS, 40.*CV.MPH_TO_MS],
    speed_lead_breakpoints = [0., 100.],
    cruise_button_presses = [(CB.DECEL_SET, 1.2), (0, 1.3)]
  )
]

css_style = """
.maneuver_title {
  font-size: 24px;
  text-align: center;
}
.maneuver_graph {
  width: 100%;
}
"""

def main(output_dir):
  view_html = "<html><head><style>%s</style></head><body><table>" % (css_style,)
  for i, man in enumerate(maneuvers):
    view_html += "<tr><td class='maneuver_title' colspan=5><div>%s</div></td></tr><tr>" % (man.title,)
    for c in ['distance.svg', 'speeds.svg', 'acceleration.svg', 'pedals.svg', 'pid.svg']:
      view_html += "<td><img class='maneuver_graph' src='%s'/></td>" % (os.path.join("maneuver" + str(i+1).zfill(2), c), )
    view_html += "</tr>"

  with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write(view_html)

  for i, man in enumerate(maneuvers):
    score, plot = man.evaluate()
    plot.write_plot(output_dir, "maneuver" + str(i+1).zfill(2))
if __name__ == "__main__":
  if len(sys.argv) <= 1:
    print "Usage:", sys.argv[0], "<output_dir>"
    exit(1)

  main(sys.argv[1])

