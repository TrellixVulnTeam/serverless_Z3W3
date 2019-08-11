# Open3D: www.open3d.org
# The MIT License (MIT)
# See license file or visit www.open3d.org for details

# examples/Python/Basic/clustering.py

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt

np.random.seed(42)


def pointcloud_generator():
    yield 'cube', o3d.geometry.TriangleMesh.create_sphere(
    ).sample_points_uniformly(int(1e4)), 0.4

    mesh = o3d.geometry.TriangleMesh.create_torus().scale(5)
    mesh += o3d.geometry.TriangleMesh.create_torus()
    yield 'torus', mesh.sample_points_uniformly(int(1e4)), 0.75

    d = 4
    mesh = o3d.geometry.TriangleMesh.create_tetrahedron().translate((-d, 0, 0))
    mesh += o3d.geometry.TriangleMesh.create_octahedron().translate((0, 0, 0))
    mesh += o3d.geometry.TriangleMesh.create_icosahedron().translate((d, 0, 0))
    mesh += o3d.geometry.TriangleMesh.create_torus().translate((-d, -d, 0))
    mesh += o3d.geometry.TriangleMesh.create_moebius(twists=1).translate(
        (0, -d, 0))
    mesh += o3d.geometry.TriangleMesh.create_moebius(twists=2).translate(
        (d, -d, 0))
    yield 'shapes', mesh.sample_points_uniformly(int(1e4)), 0.5


if __name__ == "__main__":
    cmap = plt.get_cmap('Set2')
    for pcl_name, pcl, eps in pointcloud_generator():
        labels = np.array(pcl.cluster_dbscan(eps=eps, min_points=10))
        max_label = labels.max()
        print('%s has %d clusters' % (pcl_name, max_label + 1))

        colors = cmap(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        pcl.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([pcl])
