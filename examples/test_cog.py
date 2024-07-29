from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles


def _translate(src_path, dst_path, profile="raw", profile_options={}, **options):
    """Convert image to COG."""
    # Format creation option (see gdalwarp `-co` option)
    output_profile = cog_profiles.get(profile)
    output_profile.update(dict(BIGTIFF="IF_SAFER"))
    output_profile.update(profile_options)

    # Dataset Open option (see gdalwarp `-oo` option)
    config = dict(
        GDAL_NUM_THREADS="ALL_CPUS",
        GDAL_TIFF_INTERNAL_MASK=True,
        GDAL_TIFF_OVR_BLOCKSIZE="256",
    )
    # output_profile = {
    #     "driver": "GTiff",
    #     "interleave": "pixel",
    #     "tiled": True,
    #     "blockxsize": 512,
    #     "blockysize": 512,
    # }

    cog_translate(
        src_path,
        dst_path,
        output_profile,
        config=config,
        in_memory=False,
        quiet=True,
        **options,
    )
    return True


if __name__ == '__main__':
    inPath = r'E:\LaoK\data\LuoJia1-01_LR201809085357_20180907144420_HDR_0021_gec.tif'
    outPath = r'E:\LaoK\data\test.tif'
    _translate(inPath, outPath)
