"""Render reproducible side-by-side algorithm views and metric charts."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
from PIL import Image, ImageDraw, ImageFont
from vtkmodules.util.numpy_support import numpy_to_vtk, vtk_to_numpy
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderer,
    vtkRenderWindow,
    vtkWindowToImageFilter,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "images"
MODELS = []
VIEWS = [
    ("Front structure", (0.0, -1.0, 0.0), (0.0, 0.0, 1.0), (0.50, 0.50, 0.50), 5.2),
    ("Top surface", (0.0, 0.0, 1.0), (0.0, 1.0, 0.0), (0.50, 0.52, 0.50), 5.2),
    ("Side layers", (-1.0, 0.0, 0.0), (0.0, 0.0, 1.0), (0.50, 0.54, 0.48), 5.2),
]
METRICS = {
    "Fast QEM": {"time": 9.827, "rms": 1.1721, "p95": 2.3504, "drift": 0.6987, "area": 0.3993},
    "Density balanced": {"time": 11.439, "rms": 1.2041, "p95": 2.4341, "drift": 0.0030, "area": 0.0405},
    "Shape preserving": {"time": 56.404, "rms": 1.1933, "p95": 2.3323, "drift": 0.0009, "area": 0.0491},
    "Preserve topology": {"time": 35.656, "rms": 3.1672, "p95": 6.8266, "drift": 0.0, "area": 0.0709},
    "Adaptive probes": {"time": 10.156, "rms": 1.0668, "p95": 2.0586, "drift": 0.0234, "area": 0.1241},
}


def font(size, bold=False):
    path = Path("C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf")
    return ImageFont.truetype(str(path), size)


def read_poly(path):
    reader = vtkSTLReader()
    reader.SetFileName(str(path))
    reader.Update()
    return reader.GetOutput()


def face_log_density(poly):
    points = vtk_to_numpy(poly.GetPoints().GetData())
    faces = vtk_to_numpy(poly.GetPolys().GetConnectivityArray()).reshape(-1, 3)
    triangles = points[faces]
    twice_area = np.linalg.norm(
        np.cross(triangles[:, 1] - triangles[:, 0], triangles[:, 2] - triangles[:, 0]), axis=1
    )
    return -0.5 * np.log(np.maximum(twice_area * 0.5, 1e-12))


def density_colors(values, limits):
    low, high = limits
    normalized = np.clip((values - low) / max(high - low, 1e-12), 0.0, 1.0)
    return np.asarray(plt.colormaps["turbo"](normalized)[:, :3] * 255, dtype=np.uint8)


def render(poly, bounds, direction, view_up, focus, zoom, mode, density_limits, width=400, height=280):
    mapper = vtkPolyDataMapper()
    mapper.SetInputData(poly)
    actor = vtkActor()
    actor.SetMapper(mapper)
    if mode == "wireframe":
        actor.GetProperty().SetRepresentationToWireframe()
        actor.GetProperty().SetColor(0.45, 0.66, 0.84)
        actor.GetProperty().SetLineWidth(0.7)
        actor.GetProperty().SetOpacity(0.72)
        actor.GetProperty().LightingOff()
    else:
        colors = numpy_to_vtk(density_colors(face_log_density(poly), density_limits), deep=True)
        colors.SetName("PhysicalDensity")
        colors.SetNumberOfComponents(3)
        poly.GetCellData().SetScalars(colors)
        mapper.SetScalarModeToUseCellData()
        mapper.SetColorModeToDirectScalars()
        mapper.ScalarVisibilityOn()
        actor.GetProperty().LightingOff()
    renderer = vtkRenderer()
    renderer.SetBackground(0.043, 0.106, 0.204)
    renderer.AddActor(actor)
    center = np.asarray(
        tuple(bounds[axis * 2] + focus[axis] * (bounds[axis * 2 + 1] - bounds[axis * 2]) for axis in range(3))
    )
    diagonal = np.linalg.norm(
        (bounds[1] - bounds[0], bounds[3] - bounds[2], bounds[5] - bounds[4])
    )
    vector = np.asarray(direction, dtype=float)
    vector /= np.linalg.norm(vector)
    camera = vtkCamera()
    camera.SetFocalPoint(*center)
    camera.SetPosition(*(center + vector * diagonal * 2.5))
    camera.SetViewUp(*view_up)
    camera.ParallelProjectionOn()
    renderer.SetActiveCamera(camera)
    # Fit the shared source bounds analytically so every algorithm uses the exact same framing.
    view_direction = -vector
    up = np.asarray(view_up, dtype=float)
    right = np.cross(view_direction, up)
    right /= np.linalg.norm(right)
    up = np.cross(right, view_direction)
    corners = np.asarray(
        [
            (x, y, z)
            for x in (bounds[0], bounds[1])
            for y in (bounds[2], bounds[3])
            for z in (bounds[4], bounds[5])
        ]
    ) - center
    horizontal = np.ptp(corners @ right)
    vertical = np.ptp(corners @ up)
    parallel_scale = max(vertical * 0.5, horizontal * 0.5 / (width / height)) * 1.04
    camera.SetParallelScale(parallel_scale / zoom)
    renderer.ResetCameraClippingRange(bounds)
    window = vtkRenderWindow()
    window.SetOffScreenRendering(True)
    window.SetSize(width, height)
    window.SetMultiSamples(4)
    window.AddRenderer(renderer)
    window.Render()
    capture = vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.SetInputBufferTypeToRGB()
    capture.ReadFrontBufferOff()
    capture.Update()
    image = capture.GetOutput()
    dims = image.GetDimensions()
    pixels = vtk_to_numpy(image.GetPointData().GetScalars()).reshape(dims[1], dims[0], 3)
    return Image.fromarray(np.flipud(pixels).copy())


def make_contact_sheet(mode):
    polies = [read_poly(path) for _name, path in MODELS]
    original = polies[0]
    bounds = original.GetBounds()
    simplified_density = np.concatenate([face_log_density(poly) for poly in polies[1:]])
    density_limits = tuple(np.percentile(simplified_density, (1.0, 99.0)))
    tile_width, tile_height = 400, 280
    top = 48
    left = 132
    legend_height = 44 if mode == "density" else 0
    sheet = Image.new(
        "RGB",
        (left + tile_width * len(MODELS), top + tile_height * len(VIEWS) + legend_height),
        "#f7f5f1",
    )
    draw = ImageDraw.Draw(sheet)
    title_font = font(19, True)
    row_font = font(17, True)
    for column, (name, path) in enumerate(MODELS):
        box = draw.textbbox((0, 0), name, font=title_font)
        x = left + column * tile_width + (tile_width - (box[2] - box[0])) / 2
        draw.text((x, 13), name, fill="#0b1b34", font=title_font)
        poly = polies[column]
        for row, (view_name, direction, view_up, focus, zoom) in enumerate(VIEWS):
            tile = render(
                poly, bounds, direction, view_up, focus, zoom, mode, density_limits,
                tile_width, tile_height
            )
            sheet.paste(tile, (left + column * tile_width, top + row * tile_height))
    for row, (view_name, _direction, _view_up, _focus, _zoom) in enumerate(VIEWS):
        box = draw.textbbox((0, 0), view_name, font=row_font)
        y = top + row * tile_height + (tile_height - (box[3] - box[1])) / 2
        draw.text((12, y), view_name, fill="#0b1b34", font=row_font)
    if mode == "density":
        legend_y = top + tile_height * len(VIEWS) + 14
        gradient_x = left + 58
        gradient_width = 340
        for offset in range(gradient_width):
            color = tuple(
                int(channel * 255)
                for channel in plt.colormaps["turbo"](offset / (gradient_width - 1))[:3]
            )
            draw.line((gradient_x + offset, legend_y, gradient_x + offset, legend_y + 14), fill=color)
        label_font = font(14)
        draw.text((gradient_x - 52, legend_y - 1), "Sparse", fill="#0b1b34", font=label_font)
        draw.text((gradient_x + gradient_width + 10, legend_y - 1), "Dense", fill="#0b1b34", font=label_font)
        draw.text(
            (gradient_x + gradient_width + 78, legend_y - 1),
            "Shared physical triangle-density scale for reduced meshes",
            fill="#354052",
            font=label_font,
        )
    path = OUTPUT / f"algorithm-comparison-{mode}.png"
    sheet.save(path, optimize=True)
    return path


def make_chart():
    names = list(METRICS)
    short = ["Fast QEM", "Density", "Shape", "Topology", "Adaptive\nprobes"]
    color = ["#9aa6b5", "#9aa6b5", "#9aa6b5", "#9aa6b5", "#2563ff"]
    panels = [
        ("Resident processing time", "Seconds", "time"),
        ("Sampled surface distance", "Millimetres", "rms"),
        ("95th-percentile distance", "Millimetres", "p95"),
        ("Maximum dimension drift", "Millimetres", "drift"),
        ("Surface-area error", "Percent", "area"),
    ]
    fig, axes = plt.subplots(1, 5, figsize=(18, 4.6), constrained_layout=True)
    fig.patch.set_facecolor("#f7f5f1")
    for axis, (title, ylabel, key) in zip(axes, panels):
        values = [METRICS[name][key] for name in names]
        bars = axis.bar(range(len(names)), values, color=color)
        axis.set_title(title, fontsize=11, fontweight="semibold", color="#0b1b34")
        axis.set_ylabel(ylabel, fontsize=9, color="#354052")
        axis.set_xticks(range(len(names)), short, fontsize=8)
        axis.grid(axis="y", color="#d8dce3", linewidth=0.7)
        axis.set_axisbelow(True)
        axis.set_facecolor("#f7f5f1")
        axis.spines[["top", "right"]].set_visible(False)
        axis.spines[["left", "bottom"]].set_color("#b9c0ca")
        pad = max(values) * 0.02 if max(values) else 0.01
        for bar, value in zip(bars, values):
            label = f"{value:.3f}" if value < 10 else f"{value:.1f}"
            axis.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + pad,
                label,
                ha="center",
                va="bottom",
                fontsize=8,
                color="#0b1b34",
            )
        axis.set_ylim(0, max(values) * 1.16 if max(values) else 1)
    fig.suptitle("MeshMill algorithm comparison at 250,000 triangles", fontsize=15, color="#0b1b34")
    path = OUTPUT / "algorithm-comparison-metrics.png"
    fig.savefig(path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    with Image.open(path) as rendered:
        clean = rendered.convert("RGB")
    clean.save(path, optimize=True)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results", type=Path, help="Directory containing benchmark STL outputs")
    args = parser.parse_args()
    MODELS.extend(
        [
            ("Original", ROOT / "samples" / "original-scan.stl"),
            ("Fast QEM", args.results / "meshmill-current-fast.stl"),
            ("Density balanced", args.results / "meshmill-current-density.stl"),
            ("Shape preserving", args.results / "meshmill-current-shape.stl"),
            ("Preserve topology", args.results / "meshmill-current-topology.stl"),
            ("Depth Adaptive QEM", args.results / "meshmill-depth-adaptive-qem.stl"),
        ]
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    print(make_contact_sheet("wireframe"))
    print(make_contact_sheet("density"))
    print(make_chart())
