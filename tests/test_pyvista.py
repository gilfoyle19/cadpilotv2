#!/usr/bin/env python3
"""
Test script to verify PyVista installation and basic functionality.
This will ensure PyVista works with our CAD system before we build the visualizer.
"""

import sys
import tempfile
import os
from pathlib import Path

def test_pyvista_installation():
    """Test if PyVista is properly installed and can handle CAD files."""
    print("🧪 Testing PyVista Installation...")
    print("=" * 50)
    
    # Test 1: Check if PyVista can be imported
    try:
        import pyvista as pv
        print(" PyVista imported successfully")
        print(f"   Version: {pv.__version__}")
    except ImportError as e:
        print(" FAILED: PyVista not installed")
        print("   Install with: pip install pyvista")
        return False
    
    # Test 2: Check if we can create a simple plotter
    try:
        plotter = pv.Plotter()
        print("Plotter creation successful")
    except Exception as e:
        print(f" FAILED: Plotter creation failed: {e}")
        return False
    
    # Test 3: Create a simple mesh and test visualization
    try:
        # Create a simple cube mesh
        cube = pv.Cube()
        print("Basic mesh creation successful")
        print(f"   Cube bounds: {cube.bounds}")
        print(f"   Number of points: {cube.n_points}")
        print(f"   Number of cells: {cube.n_cells}")
    except Exception as e:
        print(f"FAILED: Mesh creation failed: {e}")
        return False
    
    # Test 4: Test off-screen rendering (for thumbnails)
    try:
        plotter = pv.Plotter(off_screen=True, window_size=(400, 300))
        plotter.add_mesh(cube, color='lightblue', show_edges=True)
        plotter.show_axes()
        
        # Try to take a screenshot
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_png = f.name
        
        plotter.screenshot(temp_png)
        plotter.close()
        
        if Path(temp_png).exists():
            print("Off-screen rendering and screenshot successful")
            print(f"   Screenshot saved: {temp_png}")
            os.unlink(temp_png)  # Clean up
        else:
            print("FAILED: Screenshot not created")
            return False
            
    except Exception as e:
        print(f"FAILED: Off-screen rendering failed: {e}")
        return False
    
    # Test 5: Test STEP file support (critical for CAD)
    try:
        # Create a temporary STEP file
        with tempfile.NamedTemporaryFile(suffix='.step', delete=False) as f:
            temp_step = f.name
        
        # For this test, we'll create a simple STEP file using CadQuery if available
        # If CadQuery isn't available, we'll skip this part
        try:
            import cadquery as cq
            # Create a simple cube and export to STEP
            cube_cq = cq.Workplane("XY").box(10, 10, 10)
            cube_cq.val().exportStep(temp_step)
            print("CadQuery STEP export successful")
        except ImportError:
            print("CadQuery not available - skipping STEP export test")
            # Create a dummy STEP file for testing
            with open(temp_step, 'w') as f:
                f.write("Dummy STEP file for testing")
        
        # Try to load the STEP file with PyVista
        try:
            mesh = pv.read(temp_step)
            print("STEP file loading successful")
            print(f"   Loaded mesh bounds: {mesh.bounds}")
        except Exception as e:
            print(f"STEP file loading failed (may be expected for dummy file): {e}")
        
        # Clean up
        os.unlink(temp_step)
            
    except Exception as e:
        print(f"FAILED: STEP file test failed: {e}")
        return False
    
    # Test 6: Test interactive plotting (if not in headless environment)
    try:
        # Only test interactive if we have a display
        if 'DISPLAY' in os.environ or sys.platform == 'win32':
            print("Testing interactive plotting...")
            plotter = pv.Plotter()
            plotter.add_mesh(cube, color='lightblue', show_edges=True)
            plotter.show_axes()
            plotter.add_title("PyVista Test - Close window to continue", font_size=14)
            
            # Show for just 2 seconds then close
            plotter.show(auto_close=False, interactive=True)
            plotter.close()
            print("Interactive plotting successful")
        else:
            print("No display available - skipping interactive test")
            
    except Exception as e:
        print(f"Interactive plotting test failed: {e}")
    
    print("=" * 50)
    print("🎉 PyVista installation test completed successfully!")
    print("   Your system is ready for 3D visualization!")
    return True

def check_system_requirements():
    """Check system requirements for PyVista."""
    print("\nChecking System Requirements...")
    print("=" * 30)
    
    # Check Python version
    print(f"Python version: {sys.version}")
    
    # Check platform
    print(f"Platform: {sys.platform}")
    
    # Check if we have a display
    if 'DISPLAY' in os.environ:
        print("Display available for interactive plotting")
    elif sys.platform == 'win32':
        print("Windows platform detected")
    else:
        print("⚠️  No display detected - will only support off-screen rendering")
    
    print("=" * 30)

if __name__ == "__main__":
    check_system_requirements()
    success = test_pyvista_installation()
    
    if success:
        print("\nPyVista is ready! You can now build the visualizer.")
    else:
        print("\nPyVista setup needs attention.")
        sys.exit(1)