# MeshMill algorithm reference

This document describes the algorithms in the current application, the formulas they use, their
implementation sources, and the MeshMill-specific decisions around them. It distinguishes released
reducers from display analysis and research prototypes.

## Production reducers at a glance

| UI name | Implementation | Main objective | Boundary behavior | Typical use |
| --- | --- | --- | --- | --- |
| Depth Adaptive QEM | GPU-adaptive physical probes with `fast-simplification` assembly | Remove supported scan-scale variation while preserving overall form | Preserves open boundaries during QEM assembly | Optional higher-quality reduction on supported GPUs |
| Fast QEM | `fast-simplification` | Reach the target quickly with quadric-error edge collapses | Normal backend behavior | General reduction |
| Density balanced | `fast-simplification` with lower aggressiveness and `preserve_border=True` | Make the Fast QEM pass more conservative around open scan boundaries | Pins boundary vertices | Uneven, open, layered scan geometry |
| Shape preserving | `vtkQuadricDecimation` with volume preservation | Reduce normal-direction and volume error | VTK quadric boundary constraints | Rounded and solid-looking forms |
| Preserve topology | `vtkDecimatePro` with topology preservation, splitting off, and boundary deletion off | Avoid topology-changing operations | Preserves boundaries and topology | Holes, open edges, and connectivity matter more than speed |

All five operate on triangle meshes. Depth Adaptive QEM uses the GPU for regular surface analysis
and native Fast QEM for dependency-heavy topology mutation. The remaining reducers use native CPU
libraries. The GPU also renders the viewport.

The processor split is deliberate. Ray, depth, probe, normal, and residual calculations contain
large amounts of independent, read-mostly work and produced about a 10-times analysis-stage speedup
in the retained benchmark. QEM edge collapse mutates a changing adjacency graph and repeatedly
invalidates neighboring costs and conflict sets. Keeping that graph in VRAM removes transfer cost,
but it does not remove serialization, branch divergence, scattered updates, or synchronization.
The measured execution model, equations, failed GPU reducer results, and design consequences are
documented in [Why GPU depth analysis is fast and GPU QEM is difficult](GPU_QEM_AND_DEPTH_ANALYSIS.md).

## Shared terms and measurements

Let a triangle mesh be


$$
M=(V,F), \qquad V=\{\mathbf v_i\in\mathbb R^3\}, \qquad
F=\{(i,j,k)\}.
$$

`M` is the mesh; `V` is its set of 3D vertices; `F` is its set of triangular
faces; and `(i,j,k)` are the three vertex indices of one face.


For triangle $f=(i,j,k)$, its area is


$$
A_f=\frac{1}{2}\left\| (\mathbf v_j-\mathbf v_i)\times
(\mathbf v_k-\mathbf v_i)\right\|.
$$

`A_f` is triangle area; `v_i`, `v_j`, and `v_k` are its vertices; the cross
product gives twice the oriented area; and the norm removes direction.


MeshMill reports reduction as


$$
R=100\left(1-\frac{|F_{out}|}{|F_{in}|}\right)\%.
$$

`R` is reduction percentage; `|F_in|` is the original triangle count; and
`|F_out|` is the resulting triangle count.


Dimension drift is the component-wise absolute difference between input and output axis-aligned
bounding-box extents. It detects envelope changes, but it does not measure local distortion.

## Quadric error metrics

Fast QEM, Density balanced, and Shape preserving are variants of quadric-error simplification.
They derive from Garland and Heckbert's 1997 surface-simplification method.

For a normalized face plane


$$
p=[a,b,c,d]^T, \qquad ax+by+cz+d=0,
$$

`p` is a normalized plane in homogeneous form; `(a,b,c)` is its unit normal;
`d` is its signed offset; and `(x,y,z)` is a point on the plane.


the plane's fundamental quadric is


$$
K_p=pp^T.
$$

`K_p` is the 4-by-4 plane-error matrix and `p p^T` is the outer product of the
plane vector with itself.


The quadric accumulated at vertex $i$ is


$$
Q_i=\sum_{p\in P(i)}K_p,
$$

`Q_i` is the accumulated quadric at vertex `i`; `P(i)` is the set of incident
face planes; and each `K_p` contributes that plane's squared-distance penalty.


where $P(i)$ is the set of incident face planes. Collapsing edge $(i,j)$ combines its endpoint
quadrics:


$$
Q_{ij}=Q_i+Q_j.
$$

`Q_ij` is the combined error matrix for collapsing edge `(i,j)`; `Q_i` and
`Q_j` are its endpoint quadrics.


For candidate homogeneous position $\bar{\mathbf v}=[x,y,z,1]^T$, the estimated squared plane
error is


$$
\epsilon(\bar{\mathbf v})=\bar{\mathbf v}^{T}Q_{ij}\bar{\mathbf v}.
$$

`v_bar = (x,y,z,1)^T` is a candidate replacement vertex and `epsilon` is its
estimated squared distance from all supporting planes accumulated at the two endpoints.


If the upper-left $3\times3$ part of $Q_{ij}$ is invertible, the minimum is found from


$$
A\mathbf x=-\mathbf b.
$$

`A` is the upper-left 3-by-3 block of the combined quadric; `b` is its linear
term; and `x` is the least-error 3D replacement position when the system is invertible.


Implementations fall back to endpoint or midpoint candidates when that system is singular or when
the optimal placement is not legal. A collapse updates connectivity, removes degenerate faces, and
combines the quadrics for future decisions.

Source: [Garland and Heckbert, Surface Simplification Using Quadric Error Metrics](https://publications.ri.cmu.edu/surface-simplification-using-quadric-error-metrics).

## Fast QEM

### Released implementation

MeshMill calls `fast_simplification.simplify` with the requested reduction and the selected
aggressiveness value. The package wraps the open-source Fast Quadric Mesh Simplification
implementation.

The original QEM formulation commonly uses an ordered structure to choose the least-cost collapse.
The fast implementation avoids maintaining a globally sorted queue. On iteration $t$, it accepts
candidates below a growing threshold:


$$
\tau_t=10^{-9}(t+3)^g,
$$

`tau_t` is the accepted-error threshold on pass `t`; `g` is aggressiveness; and
a larger `g` admits higher-cost collapses earlier.


where $g$ is aggressiveness. A larger $g$ admits costly collapses sooner. A smaller value takes
more passes and tends to be more conservative.

Before committing a collapse, the backend tests adjacent triangles for degeneracy and excessive
normal change. Its implementation rejects a nearly collinear reconstructed triangle when the
absolute edge-direction dot product exceeds `0.999`, and rejects a face when the reconstructed
normal dot the previous normal is below `0.2`.

### Derivation and MeshMill changes

The quadrics and collapse error come from the published QEM method. The threshold scheduler and
flip tests come from Fast Quadric Mesh Simplification. MeshMill supplies the target, exposes the
aggressiveness control, runs the native reducer away from the UI thread, and integrates preview,
comparison, cancellation, selection-only work, and apply history. MeshMill does not claim a new
QEM formula for this option.

Sources:

- [fast-simplification](https://github.com/pyvista/fast-simplification)
- [Fast Quadric Mesh Simplification](https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification)
- [Python API reference](https://pyvista.github.io/fast-simplification/_autosummary/fast_simplification.simplify_mesh.html)

## Density balanced

### What the current option does

Density balanced uses the same Fast QEM backend. It changes two controls:


$$
g_d=\min(5,\max(0,0.70g)),
$$

`g` is the selected Fast QEM aggressiveness and `g_d` is the more conservative
Density balanced value, clamped to the backend's valid 0-to-5 range.


and enables `preserve_border=True`.

The lower effective aggressiveness delays higher-error collapses. Boundary preservation prevents
the reducer from moving or deleting vertices recognized as belonging to open borders. QEM's plane
error tends to collapse redundant coplanar sampling cheaply because such movement adds little
distance-to-plane error. Curved or sharply changing regions accumulate conflicting plane
constraints and are more expensive to collapse.

### What the option does not do

It does not use the colored density field as an optimization weight. It does not assign an explicit
triangle quota per density band. The name describes the intended operating behavior, not a distinct
published density-decimation formula.

### Development finding

An earlier experiment performed voxel averaging before QEM. Moving vertices before calculating
collapse error visibly distorted scan surfaces, so that prepass was removed. The released option is
the conservative configuration above. This removal and the parameter mapping are MeshMill-specific
engineering decisions, not a claim of a new reduction algorithm.

## Shape preserving

MeshMill uses VTK's `vtkQuadricDecimation`, sets the requested target reduction, and enables volume
preservation. VTK repeatedly collapses edges using a priority queue ordered by quadric cost. Its
extended quadric can include terms intended to reduce error in the triangle-normal direction.

The base QEM objective measures displacement from supporting planes. Volume preservation adds a
constraint that discourages accumulated inward or outward motion. Conceptually, the candidate
minimizes a constrained or augmented objective


$$
\epsilon_V(\mathbf x)=\mathbf{\bar x}^TQ\mathbf{\bar x}
+\lambda E_V(\mathbf x),
$$

`epsilon_V` is an augmented collapse objective; `x_bar^T Q x_bar` is ordinary
quadric error; `E_V` measures local volume or normal-direction change; and `lambda` is VTK's
internally managed weight.


where $E_V$ represents the local volume or normal-direction change and $\lambda$ is managed by
VTK. MeshMill uses the VTK implementation rather than reproducing its internal solver.

MeshMill's contribution is the named preset, target integration, asynchronous execution, and
reversible application workflow. The decimator and volume-preservation method are VTK work.

Source: [`vtkQuadricDecimation` documentation](https://vtk.org/doc/nightly/html/classvtkQuadricDecimation.html)
and [VTK source](https://github.com/Kitware/VTK/blob/master/Filters/Core/vtkQuadricDecimation.cxx).

## Preserve topology

MeshMill uses `vtkDecimatePro` with:

- `PreserveTopologyOn()`;
- `SplittingOff()`;
- `BoundaryVertexDeletionOff()`.

This algorithm follows the vertex-removal family described by Schroeder, Zarge, and Lorensen.
Vertices are classified by local topology, assigned an error, and processed by priority. A legal
removal deletes the vertex and its incident triangles, then retriangulates the resulting local hole.
When topology preservation is enabled, operations that split the mesh, close a hole, or otherwise
change topology are rejected. Disabling boundary deletion further protects open edges.

The geometric error is based on the distance of the removed vertex and affected neighborhood from
the replacement local triangulation. In simplified form, for removed point $\mathbf v$ and
replacement patch $T'$, the local error is measured as


$$
E(\mathbf v,T')=\min_{\mathbf x\in T'}\|\mathbf v-\mathbf x\|,
$$

`v` is a removed vertex; `T'` is the replacement triangulated patch; `x` is a
point on that patch; and `E` is the shortest distance from the removed point to the replacement.


with the production implementation maintaining additional topology and accumulated-error state.
Because legal operations are restricted, a topology-preserving pass may be slower, may preserve
more vertices, or may stop before a difficult target on some meshes.

Sources:

- [`vtkDecimatePro` documentation](https://vtk.org/doc/nightly/html/classvtkDecimatePro.html)
- [Schroeder, Zarge, and Lorensen, Decimation of Triangle Meshes](https://www.cs.columbia.edu/~allen/PHOTOPAPERS/Schroeder-etal-sg92.pdf)

## Density display analysis

Density is a display mode, not a fifth reducer. It is calculated per vertex and converted to stable
per-triangle colors.

For vertex $i$, let $n_i$ be its incident-face count and let


$$
S_i=\sum_{f\ni i}A_f.
$$

`S_i` is the total area of all faces incident to vertex `i`; `A_f` is one
incident face's area.


MeshMill's raw local sampling density and log density are


$$
\rho_i=\frac{n_i}{S_i}, \qquad \ell_i=\log(\max(\rho_i,10^{-30})).
$$

`n_i` is incident-face count; `S_i` is represented surface area; `rho_i` is
local samples per unit area; and `ell_i` is its numerically safe logarithm.


Log space keeps extreme scan-density differences visible without allowing the densest region to
consume the full color range. Each incident face contributes its three-vertex mean, producing the
one-ring smoothing used by the implementation:


$$
\tilde\ell_i=
\frac{\ell_i+\sum_{f\ni i}\left(\frac{1}{3}\sum_{j\in f}\ell_j\right)}{1+n_i}.
$$

`ell_tilde_i` is smoothed log density; each incident face contributes the mean
log density of its three vertices; and `1+n_i` normalizes the vertex plus its one-ring faces.


The center and robust scale are


$$
m=\operatorname{median}(\tilde\ell),
$$

`m` is the median smoothed log density over the mesh and supplies a robust center.



$$
\operatorname{MAD}=\operatorname{median}(|\tilde\ell-m|),
$$

`MAD` is the median absolute deviation from `m`, a robust measure of density
spread that resists extreme scan regions.



$$
\sigma_r=\max(1.4826\operatorname{MAD},10^{-12}).
$$

`sigma_r` is a robust standard-deviation estimate; `1.4826` makes MAD comparable
to Gaussian standard deviation; and the floor prevents division by zero.


The robust score is clipped to keep numeric outliers bounded:


$$
z_i=\operatorname{clip}\left(\frac{\tilde\ell_i-m}{\sigma_r},-8,8\right).
$$

`z_i` is standardized density at vertex `i`; clipping to `[-8,8]` keeps extreme
outliers from consuming the color scale.


A logistic approximation supplies bell-curve-like contrast:


$$
B_i=\frac{1}{1+e^{-1.702z_i}}.
$$

`B_i` maps robust score `z_i` to 0-to-1 contrast; `1.702` is the logistic scale
used as a practical normal-CDF approximation.


Multimodal scans can contain several legitimate density populations, so MeshMill also calculates a
percentile contrast between the 0.5th and 99.5th percentiles:


$$
P_i=\operatorname{clip}\left(
\frac{\tilde\ell_i-q_{0.5}}{q_{99.5}-q_{0.5}},0,1\right).
$$

`q_0.5` and `q_99.5` are density percentiles; `P_i` maps the central 99% of
observations to a stable 0-to-1 range.


The final scalar is


$$
C_i=\max(B_i,0.8P_i).
$$

`C_i` is final display intensity; `B_i` preserves statistical contrast and
`0.8 P_i` keeps distinct density populations visible.


It is linearly interpolated through five colors from sparse navy to dense red. Triangle color is the
mean of its three vertex colors.

This particular combination of area-normalized incidence, log scaling, one-ring smoothing, robust
MAD scoring, and percentile contrast is a MeshMill display heuristic. It was developed to make
regional scan density readable without extreme zoom. It has not been presented as a new statistical
method or peer-reviewed mesh metric.

## Automatic target estimate

The automatic target is a MeshMill heuristic. Let $D$ be the input bounding-box diagonal and
$d_q$ the quality divisor:

| Quality | $d_q$ | Maximum fraction of input triangles |
| --- | ---: | ---: |
| Draft | 160 | 15% |
| Balanced | 500 | 50% |
| Fine | 800 | 75% |

The desired edge length and ideal equilateral-triangle area are


$$
e_q=\frac{D}{d_q}, \qquad A_q=\frac{\sqrt 3}{4}e_q^2.
$$

`D` is the bounding-box diagonal; `d_q` is the quality divisor; `e_q` is desired
edge length; and `A_q` is the area of an ideal equilateral triangle at that scale.


For total mesh area $A_M$, the initial estimate is


$$
N_q=\operatorname{round}\left(\frac{A_M}{A_q}\right).
$$

`A_M` is total mesh area; `A_q` is desired area per triangle; and `N_q` is the
initial target before application ceilings and quality caps.


MeshMill clamps that estimate to the quality fraction, a 750,000-triangle application ceiling, and
the valid range for the current mesh. The formula gives objects of different physical sizes a
consistent first target while preventing noisy surface area from making every preset nearly full
density. Manual target entry remains authoritative.

## Research status and claims

Released third-party algorithms retain their original attribution. MeshMill-specific work includes
workflow integration, target selection, display analysis, conservative parameterization, selection
scoping, reversible preview/apply behavior, and benchmark-driven rejection of unsafe approaches.

GPU clustering, complete GPU QEM, tiled reduction, and GPU surface-field work remain prototypes.
Depth-gauge surface sampling is now the production Depth Adaptive QEM analysis stage. Formulas,
results, and rejection reasons are recorded in
[`GPU_GEOMETRY_PROTOTYPE_RESULTS.md`](../benchmarks/GPU_GEOMETRY_PROTOTYPE_RESULTS.md). They are not
listed as application capabilities.

Depth Adaptive QEM originated with the project author's physical depth-gauge
model, not with the GPU simplification papers evaluated during development. Published research
provided the QEM baseline and alternative strategies that were implemented, measured, and rejected.
The complete distinction, mathematical derivation, execution profile, and failure analysis are in
[`DEPTH_GAUGE_REDUCTION.md`](DEPTH_GAUGE_REDUCTION.md).

### Surface-trajectory projection prototype

The completed assembly experiment in `benchmarks/gpu_trajectory_prefilter_qem.py` keeps the source
indexed topology instead of reconstructing disconnected depth sheets. At each spatial scale, the GPU
calculates an area-weighted local plane. For cell $c$,


$$
\mathbf n_c=\frac{\sum_{f\in c}A_f\mathbf n_f}
{\left\|\sum_{f\in c}A_f\mathbf n_f\right\|},
\qquad
\mathbf o_c=\frac{\sum_{f\in c}A_f\mathbf c_f}{\sum_{f\in c}A_f}.
$$

`c` is a spatial cell; `f` is an assigned face; `A_f` is face area; `n_f` and
`c_f` are face normal and center; and `n_c` and `o_c` are the area-weighted cell normal and center.


Normal coherence is


$$
h_c=\frac{\left\|\sum_{f\in c}A_f\mathbf n_f\right\|}{\sum_{f\in c}A_f},
$$

`h_c` is 0-to-1 normal coherence. Values near 1 describe a consistent local
surface direction; lower values indicate curvature, folds, or competing layers.


and a face center's plane residual is


$$
r_f=|\mathbf n_c\cdot(\mathbf c_f-\mathbf o_c)|.
$$

`r_f` is perpendicular face-center distance from the fitted cell plane; the dot
product measures displacement along cell normal `n_c`.


A face is treated as a supported surface outlier when


$$
h_c\ge0.970, \qquad t<r_f\le3t,
$$

`0.970` is the fixed normal-coherence threshold; `t` is analysis tolerance; and
faces between `t` and `3t` are treated as supported surface excursions in this predecessor.


where $t$ is the analysis tolerance. For each incident vertex $\mathbf v$, the plane projection
is


$$
\mathbf v'_{f,c}=\mathbf v-\mathbf n_c
(\mathbf n_c\cdot(\mathbf v-\mathbf o_c)).
$$

`v` is an original vertex; `v'_(f,c)` is its projection onto the plane defined
by `n_c` and `o_c`; only the normal-direction component is removed.


The implementation takes an area-weighted average of those displacement vectors over the selected
faces and scales, then clamps the total displacement:


$$
\Delta\mathbf v_{final}=\Delta\mathbf v
\min\left(1,\frac{d_{max}}{\|\Delta\mathbf v\|}\right).
$$

`Delta v` is the combined proposed displacement; `d_max` is the movement cap;
and the minimum term scales only proposals that exceed that cap.


The best full-scan run used scales 24, 48, and 72, $t=0.10$ mm, and
$d_{max}=0.05$ mm. The original triangle connectivity is passed to boundary-preserving Fast QEM
after projection. This supplies one indexed STL rather than six open sheets.

The contour-gauge interpretation, multiscale supported-outlier rule, and bounded projection pipeline
are MeshMill project work. The plane fit, orthogonal projection, and QEM assembly operations are
established mathematical components. This fixed-scale predecessor remains a prototype; its
physically derived successor is the released Depth Adaptive QEM algorithm.

### Adaptive physical probes

`benchmarks/gpu_adaptive_probe_qem.py` removes the free resolution, tolerance, and displacement
controls from the experiment. It derives physical probe geometry from the mesh and requested target.
The probe body diameter is the median valid source edge length:


$$
d=\operatorname{median}\{\|\mathbf v_i-\mathbf v_j\|:(i,j)\in E\}.
$$

`d` is physical probe diameter; `E` is the edge set; and the median valid edge
length supplies a robust source-sampling scale.


The prototype uses a hemispherical end with radius


$$
r=\frac d2.
$$

`r` is hemispherical tip radius and `d` is probe diameter.


The closest probe pitch comes from the ideal equilateral output triangle edge. For source area
$A_M$ and target triangle count $N$,


$$
p_{min}=\max\left(d,\sqrt{\frac{4A_M}{\sqrt3N}}\right).
$$

`p_min` is finest probe pitch; `d` is source sampling scale; `A_M` is total
surface area; and `N` is the requested output-triangle count.


Candidate pitches are $8p_{min},4p_{min},2p_{min},p_{min}$. Each face starts at the widest spacing.
If that probe population cannot represent the local normal field and plane residual, the face moves
to the next denser level. The maximum allowed normal angle at pitch $p$ is derived from the probe
tip:


$$
\theta_p=\tan^{-1}\left(\frac r{p/2}\right),
\qquad h_c\ge\cos\theta_p.
$$

`theta_p` is allowed normal variation at pitch `p`; `r` is tip radius; and the
coherence test becomes stricter as probe spacing widens.


This makes wide probe spacing strict on long flat surfaces while allowing progressively tighter
curvature at smaller spacing. A supported excursion is projected when


$$
\frac r2<r_f\le\frac{3r}{2},
$$

`r_f` is face residual and `r` is tip radius. Only supported excursions inside
this physical band are corrected; larger deviations remain unresolved.


and total movement is capped at $r/4$. Faces that fail the finest probe remain untouched.

On the full fixture, physical dimensions were derived as follows:

- probe diameter: 0.4513 mm;
- tip radius: 0.2256 mm;
- closest pitch: 2.0553 mm;
- widest pitch: 16.4428 mm.

The hierarchy represented 273,988 source faces with 311 widest-spacing probes. The next levels used
2,258, 14,350, and 51,519 probes. It left 686,197 faces unresolved rather than flattening them. This
demonstrates adaptive probe removal on flat surfaces. Its first output did not improve the fixed-scale
candidate's sampled distance, so it remains an architectural prototype rather than replacing that
candidate.

Retesting the same physical-probe analysis with Fast QEM aggressiveness 8 changed that result. Three
full resident runs took 10.481, 10.112, and 10.156 seconds. The output was deterministic across the
runs: 249,999 triangles, 1.0668 mm RMS, 2.0586 mm P95, 0.0234 mm maximum dimension drift, 0.1241%
surface-area error, 14,215 boundary edges, and 48 non-manifold edges. This measured configuration is
the production Depth Adaptive QEM configuration. Fast QEM remains the application default and does
not initialize the GPU analysis backend.

Two triangle-budget refinements were tested:

1. A continuous per-vertex probe-density attribute was supplied to VTK's attribute-aware QEM. It
   reached the target but took 61.096 seconds of resident compute and produced 1.2591 mm RMS and
   2.4558 mm P95 sampled distance. Attribute QEM preserves changes in a scalar field; it does not
   interpret the scalar magnitude as a local triangle quota.
2. Faces were divided into five probe-density levels, each level received an explicit target, region
   boundaries were pinned during Fast QEM, identical interfaces were welded, and a global
   reconciliation pass reached 250,000 triangles. Pinned interfaces caused every regional pass to
   stop above its quota. The final result took 26.536 seconds of resident compute and produced
   1.7353 mm RMS and 3.4573 mm P95 distance.

Both approaches were rejected. The retained design requirement is to insert the adaptive probe
importance directly into a single global QEM edge cost. For endpoints $i,j$, the next reducer should
rank the ordinary geometric error with an adaptive importance multiplier:


$$
\epsilon'_{ij}=\epsilon_{ij}\,W(i,j),
$$

`epsilon_ij` is ordinary QEM edge cost; `W(i,j)` is a proposed adaptive
importance multiplier; and `epsilon'_ij` would be the weighted cost in a future integrated backend.


where $W$ is low and slowly varying across coarse flat trajectories, increases with required probe
density, and is highest for unresolved geometry. This preserves global connectivity and collapse
ordering without manufacturing region seams. It requires a weighted Fast QEM backend rather than a
wrapper around the current fixed-cost API.
