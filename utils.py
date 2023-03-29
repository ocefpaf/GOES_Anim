import numpy as np


def _re_projection(ds):
    # https://proj.org/operations/projections/geos.html
    from pyproj import Proj

    sweep_angle_axis = ds["goes_imager_projection"].sweep_angle_axis
    perspective_point_height = perspective_point_height = ds[
        "goes_imager_projection"
    ].perspective_point_height
    longitude_of_projection_origin = ds[
        "goes_imager_projection"
    ].longitude_of_projection_origin

    x = ds["x"] * perspective_point_height
    y = ds["y"] * perspective_point_height

    p = Proj(
        proj="geos",
        h=perspective_point_height,
        lon_0=longitude_of_projection_origin,
        sweep=sweep_angle_axis,
    )

    lons, lats = p(x, y, inverse=True)
    return x, y, lons, lats


def _near(x, x0, n=1):
    """
    Given an 1D array `x` and a scalar `x0`, returns the `n` indices of the
    element of `x` closest to `x0`.

    """
    distance = np.abs(x - x0)
    index = np.argsort(distance)
    return index[:n], distance[index[:n]]


def _indices(lons, lats, min_lon, max_lon, min_lat, max_lat):
    idx0 = _near(lons, min_lon - 2)[0][0]
    idx1 = _near(lons, max_lon + 2)[0][0]

    idy0 = _near(lats, min_lat - 2)[0][0]
    idy1 = _near(lats, max_lat + 2)[0][0]
    return idx0, idx1, idy0, idy1


def smaller_image(ds, min_lon, max_lon, min_lat, max_lat):
    x, y, lons, lats = _re_projection(ds)
    idx0, idx1, idy0, idy1 = _indices(lons, lats, min_lon, max_lon, min_lat, max_lat)
    # The options are NaturalColor and TrueColor, no GeoColor yet.
    rgb = ds.rgb.NaturalColor(night_IR=True)[idy1:idy0, idx0:idx1]
    extent = x[idx0], x[idx1], y[idy0], y[idy1]
    imshow_kw = {"transform": ds.rgb.crs, "extent": extent, "origin": "upper"}
    return rgb, imshow_kw
