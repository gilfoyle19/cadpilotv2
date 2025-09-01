# CadQuery Error Reference

Use this guide to avoid or troubleshoot common CadQuery modeling errors.

---

## 1. Geometry and Sketch Errors

### Wire Construction Errors
- **Error**: `ValueError: Cannot build a valid wire from provided edges`
- **Cause**: Edges do not connect precisely; the loop is not closed or self-intersecting.
- **Fix**: Ensure each edge ends exactly where the next starts; use `.close()` if applicable.

### Invalid Face Creation
- **Error**: `RuntimeError: Failed to build face`
- **Cause**: The sketch is self-intersecting or forms an invalid loop.
- **Fix**: Avoid overlapping paths; validate the geometry visually or programmatically.

### Extrusion Fails
- **Error**: `RuntimeError: extrude() failed`
- **Cause**: The face is invalid, the extrusion vector is zero, or the sketch is broken.
- **Fix**: Confirm the sketch is a clean, closed loop and that extrusion direction is valid.

---

## 2. Workplane and Selector Errors

### Workplane Has No Faces
- **Error**: `ValueError: Workplane has no faces`
- **Cause**: Selector like `.faces(">Z")` is applied to an object without matching geometry.
- **Fix**: Use `.val()` or `.first()` if needed and validate selector chains.

### Chained Selector Returns None
- **Error**: `AttributeError: 'NoneType' object has no attribute 'faces'`
- **Cause**: A previous operation in the chain returned `None`, likely due to invalid selection.
- **Fix**: Break the chain into steps and inspect each part; validate intermediate objects.

---

## 3. Selector and Boolean Errors

### Multiple Faces Selected
- **Error**: `ValueError: More than one face selected`
- **Cause**: Operations like `.workplane()` or `.hole()` require a single face, but multiple were returned.
- **Fix**: Use `.faces(...).val()` or refine the selector with filters to get a single face.

### Boolean Cut Fails
- **Error**: `RuntimeError: Boolean cut failed`
- **Cause**: Cut object does not intersect the solid or has invalid topology.
- **Fix**: Ensure cut geometry overlaps the solid significantly and is valid.

---

## 4. Method Usage and Type Errors

### Missing Required Arguments
- **Error**: `TypeError: cylinder() missing required arguments`
- **Cause**: Required parameters (e.g., radius, height) are not provided.
- **Fix**: Check method signature and pass all required positional arguments.

### Using None in Chain
- **Error**: `AttributeError: 'NoneType' object has no attribute 'val'`
- **Cause**: One step in the modeling chain returned `None`, often from invalid selector or operation.
- **Fix**: Break the chain and inspect intermediate variables individually.

---

## 5. Units, Scale, and Direction Issues

### Extreme or Invalid Scale
- **Error**: Geometry does not render or fails silently.
- **Cause**: Using extremely small (`1e-12`) or large (`1e+12`) values.
- **Fix**: Keep all dimensions within a realistic range (e.g., 0.1–1000 mm).

### Negative Dimensions
- **Error**: Model may fail to build or produce unexpected geometry.
- **Cause**: Using negative values in operations like `.box()` or `.cylinder()`.
- **Fix**: Use positive values and change orientation via `.mirror()` or workplane direction.

---

# Debugging Tips

- Split long chains into steps to isolate where failures occur.
- Use `.val()` or `.first()` when you need a single face, edge, or vertex.
- Check that all sketches are **closed**, **non-self-intersecting**, and **2D planar** before extrusion.

---
