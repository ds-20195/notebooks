# Understanding `figsize`, `aspect`, and `box_aspect` in a GeoDataFrame Plot

This explainer supplements Notebook 3 and clarifies what happens when you modify the `figsize` and
`aspect` parameters passed to `GeoDataFrame.plot()`.

In particular, it should help you predict the differences between these calls:

```python
# A tall canvas
continental_gdf.plot(figsize=(24, 48), column="STATEFP")

# A wide canvas
continental_gdf.plot(figsize=(24, 12), column="STATEFP")

# A wide canvas with explicit aspect values
continental_gdf.plot(figsize=(24, 12), column="STATEFP", aspect="auto")
continental_gdf.plot(figsize=(24, 12), column="STATEFP", aspect="equal")
continental_gdf.plot(figsize=(24, 12), column="STATEFP", aspect=None)
```

> `continental_gdf` is a GeoDataFrame containing the continental United States.

In summary, **`figsize`, `aspect`, and `box_aspect` each answer a different question.**

| Parameter    | Question it answers                                              |
|--------------|------------------------------------------------------------------|
| `figsize`    | How big is the canvas?                                           |
| `box_aspect` | What is the height-to-width ratio of the viewport on that canvas?|
| `aspect`     | Must the data keep equal horizontal and vertical scale, or can it stretch to fill the viewport? |

---

## A painting analogy

Think of producing a painting for display.

* **`figsize`** is the size of the **canvas** you work on.
* **`box_aspect`** is the shape of the **viewport** — the rectangular region on the canvas where the
  painting actually appears. (Any canvas outside this region is excess space.)
* **`aspect`** controls whether the subject in the viewport must keep its true proportions, or
  whether it can be stretched to fill the available shape.

So all three affect the final image, but they control different things: the overall size, the shape
of the drawing area, and whether distortion is allowed.

### Why a bigger `figsize` can make the map look bigger

A larger `figsize` gives more canvas, so the entire plot, including the axes, typically scales up.
But if `aspect` is preserving data proportions, Matplotlib may enlarge the drawing rather than add
empty padding. That is why switching from `figsize=(24, 12)` to `figsize=(24, 48)` often makes the
map itself bigger instead of floating it in a tall empty rectangle.

---

## What GeoPandas is doing under the hood

GeoPandas delegates all plotting to Matplotlib. When you pass `aspect="equal"` to
`GeoDataFrame.plot(...)`, you are ultimately invoking Matplotlib's aspect-handling system.

If you pass no `aspect` argument, GeoPandas defaults to `aspect='auto'`, which behaves as follows:

* **Projected data** $\rightarrow$ equivalent to `"equal"` (1:1 scale on both axes).
* **Unprojected data (lon/lat)** $\rightarrow$ aspect is set to 
  $\frac{1}{\cos\left(\frac{y_{mid}\pi}{180}}`, where $y_{mid}$ is the latitude of the center of 
  the GeoDataFrame's bounding box. This approximates an Equirectangular projection so that a square 
  in lon/lat space looks roughly square on screen at the middle of the plot.
* **`aspect=None`** $\rightarrow$ the axes aspect is left unchanged (Matplotlib's own default applies).
* **`aspect=<float>`** $\rightarrow$ sets the ratio of y-unit to x-unit manually.

Because the final layout depends on Matplotlib's interplay between data aspect, adjustable behavior,
and box aspect, unexpected behaviour in a GeoPandas plot is usually explained in the Matplotlib docs
(linked below).

---

## Official references

* [Matplotlib `Axes.set_aspect`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_aspect.html)
* [Matplotlib `Axes.set_adjustable`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_adjustable.html)
* [Matplotlib `Axes.set_box_aspect`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.set_box_aspect.html)
* [GeoPandas `GeoDataFrame.plot`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.plot.html)
* [Matplotlib example: Axes box aspect](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/axes_box_aspect.html)