createLSHBenchmark = "CreateLSHBenchmark"
lshbox = "LSHBox"
vec2bin = "vec2bin"
vec2hdf5 = "vec2hdf5"
kdtree = "VarianceTesting"
gaussoraconf = "gaussoraConf.pl" 
gaussora = "gaussora"

DATADIRFULL_FORMAT = "{datadir}/{datatype}/{dataname}"
RESULTDIRFULL_FORMAT = "{resultdir}/{datatype}/{dataname}"
CONFDIRFULL_FORMAT = "{confdir}/{datatype}/{dataname}"

INDEXDIR_FORMAT = "{datadirfull}/indexes"
QDIR_FORMAT = "{datadirfull}/query"

BENCHMARKDIR_FORMAT = "{resultdirfull}/benchmarks"
CONFDIR_FORMAT = "{confdirfull}/conf"


VECDATA_NAME = "{name}__d={dimensions}_s={size}"
GAUSSDATA_NAME = "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"

QNAME = "query_{fullname}_qs={Q}_f={fold}.{dataformat}"
TOPK_NAME = "{fullname}_k={K}.topk.txt"
BENCHMARK_NAME = "{fullname}_k={K}.bench.txt"
KD_BENCHMARK_NAME = "{fullname}_k={K}.kd.bench.txt"
LSHRFILE_NAME = "{fullname}_k={K}.rfile.txt"
GAUSSCONF_NAME = "{fullname}.conf.txt"

