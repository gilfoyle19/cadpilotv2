import cadquery as cq
from cadquery import exporters

result = cq.Workplane("XY").box(1, 2, 3)
cq.exporters.export(result, "box.step")