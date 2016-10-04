createLSHBenchmark = "CreateLSHBenchmark"
lshbox = "LSHBox"
vec2bin = "vec2bin"
vec2hdf5 = "vec2hdf5"
kdtree = "VarianceTesting"

DATADIRFULL_FORMAT = "{datadir}/{datatype}/{dataname}"
INDEXDIR_FORMAT = "{datadirfull}/indexes"
BENCHMARKDIR_FORMAT = "{datadirfull}/int"
QDIR_FORMAT = "{datadirfull}/query"

VECDATA_NAME = "{name}__d={dimensions}_s={size}"
GAUSSDATA_NAME = "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"

QNAME = "query_{fullname}_qs={Q}.{dataformat}"
TOPK_NAME = "{fullname}_k={K}.topk.txt"
BENCHMARK_NAME = "{fullname}_k={K}.bench.txt"
KD_BENCHMARK_NAME = "{fullname}_k={K}.kd.bench.txt"
LSHRFILE_NAME = "{fullname}_k={K}.rfile.txt"

