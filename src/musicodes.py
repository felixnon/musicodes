import numpy as np
from stl import mesh
import sys, getopt
import os
import reader
import builder
import utils


def make_model(code_values, out_file, split_base=False, preview=False):
    """creates a 3D file of the music code"""
    CODE_OFFSET = 100   # offset between code and left edge
    LOGO_OFFSET = 50    # offset between logo and left edge
    GAP = 12.42         # gap between the individual bars 
    BASE_HEIGHT = 5     # height of the base
    CODE_HEIGHT = 5     # height of the code bars
    SCALING = .25       # scaling factor for complete model. 0.25 results in 10 by 2.5cm

    # build the code out of the individual bars
    code_mesh = mesh.Mesh(np.zeros([0,], dtype=mesh.Mesh.dtype))
    for i, size in enumerate(code_values): 
        bar = builder.get_bar(size, height=CODE_HEIGHT)
        bar.x += CODE_OFFSET + i * GAP

        # append bar to code 
        code_mesh = mesh.Mesh(np.concatenate([
            code_mesh.data.copy(),
            bar.data.copy(),
        ]))
    
    # build the logo and base plate
    logo = builder.get_logo(height=CODE_HEIGHT)
    logo.x += LOGO_OFFSET
    base = builder.get_base(heigt=BASE_HEIGHT)

    # rescale all meshes to get a final size of 10mm x 2.5mm
    code_mesh.vectors *= SCALING
    logo.vectors *= SCALING
    base.vectors *= SCALING

    if split_base:
        output_mesh = mesh.Mesh(np.concatenate([
            code_mesh.data.copy(),
            logo.data.copy()
        ]))
        out_base = out_file.replace(".stl", "_base.stl")
        out_code = out_file.replace(".stl", "_code.stl")
        output_mesh.save(out_code)
        base.save(out_base)
        print("Saved code in:", os.path.abspath(out_code))
        print("Saved base in:", os.path.abspath(out_base))
    else:
        output_mesh = mesh.Mesh(np.concatenate([
            code_mesh.data.copy(),
            logo.data.copy(),
            base.data.copy()
        ]))
        output_mesh.save(out_file)
        print("Saved in:", os.path.abspath(out_file))

    if preview:
        import matplotlib.pyplot as plt
        from mpl_toolkits import mplot3d
        # Create a new plot
        figure = plt.figure()
        axes = mplot3d.Axes3D(figure)
        axes.w_zaxis.line.set_lw(0.)
        axes.set_zticks([])

        # Load the STL files and add the vectors to the plot
        collection = mplot3d.art3d.Poly3DCollection(base.vectors, alpha=.1)
        collection.set_facecolor("black")
        axes.add_collection3d(collection)

        collection2 = mplot3d.art3d.Poly3DCollection(code_mesh.vectors)
        collection2.set_facecolor("blue")
        axes.add_collection3d(collection2)

        collection3 = mplot3d.art3d.Poly3DCollection(logo.vectors)
        collection3.set_facecolor("blue")
        axes.add_collection3d(collection3)

        # Auto scale to the mesh size
        scale = code_mesh.points.flatten('F')
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        plt.show()


def main(uri_in, split=False, preview=False):
    
    uri = reader.parseURI(uri_in)
    if not uri:
        msg = f"Invalid input: {uri_in}\n"
        msg += "Use Web-URL or Spotify-URI"
        print(msg)
        sys.exit(2)
    
    code_values = reader.get_code(uri)
    if not code_values:
        msg = f"Could not fetch Spotify code."
        print(msg)
        sys.exit(2)
    
    out_file = os.path.join("..", "3D_files", "musicode_" + uri.split(":")[2] + ".stl")
    make_model(code_values, out_file=out_file, split_base=split, preview=preview)


if __name__ == "__main__":
    main(*utils.parse_args(sys.argv[1:]))
