import numpy as np
import pandas as pd
import xarray as xr
import datetime

# # 一个shape为[4,3]的多维数据组
# data = np.random.rand(4, 3)
# # 两个维度值列表
# locs = ["IA", "IL", "IN"]
# times = pd.date_range("2000-01-01", periods=4)
#
# # dims 为两个维度定义了名字
# # 构造DataArray
# foo = xr.DataArray(data, coords=[times, locs], dims=["time", "space"])
# coords = foo.coords
# foo.attrs = {"test": 1}
# print(foo.attrs)
# print(foo.coords)
# array = xr.DataArray(
#     np.random.randn(2, 3), coords=[("x", ["a", "b"]), ("y", [0, 1, 2])]
# )
# print(array)
# stacked = array.stack(z=("x", "y"))
# print(stacked)

# time = pd.date_range("2000-01-01", freq="6H", periods=365 * 4)
# ds = xr.Dataset({"foo": ("time", np.arange(365 * 4)), "time": time})
# ds2 = ds.groupby("time.hour")
# ds3 = ds.resample(time="6H")
# print(ds2)
#
#
# def testKwargs(**kwargs):
#     return kwargs["a"]
#
# print(testKwargs(a=1))
np.random.seed(0)
temperature = 15 + 8 * np.random.randn(2, 2, 3)
precipitation = 10 * np.random.rand(2, 2, 3)
lon = [[-99.83, -99.32], [-99.79, -99.23]]
lat = [[42.25, 42.21], [42.63, 42.59]]
time = pd.date_range("2014-09-06", periods=3)
reference_time = pd.Timestamp("2014-09-05")
ds = xr.Dataset(
    data_vars=dict(
        temperature=(["x", "y", "time"], temperature),
        precipitation=(["x", "y", "time"], precipitation),
    ),
    coords=dict(
        lon=(["x", "y"], lon),
        lat=(["x", "y"], lat),
        time=time,
        reference_time=reference_time,
    ),
    attrs=dict(description="Weather related data."),
)
print(ds)