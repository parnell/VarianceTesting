createLSHBenchmark = "CreateLSHBenchmark"
lshbox = "LSHBox"
vec2bin = "vec2bin"
vec2vect = "vec2vect"
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


# VECDATA_NAME = "{name}__d={dimensions}_s={size}"
VECDATA_NAME = "{name}"
GAUSSDATA_NAME = \
    "{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}"
GAUSSLSHDATA_NAME = \
    '{name}__d={dimensions}_s={size}_nclus={nclus}_var={var}'\
    '_t={lshtype}_lM={lshM}_lL={lshL}_lS={lshS}_lI={lshI}_lN={lshN}'

QNAME = "query_{fullname}_qs={Q}_f={fold}.{dataformat}"
TOPK_NAME = "{fullname}_k={K}_qs={Q}_f={fold}.topk.txt"
LSH_BENCHMARK_NAME = "{fullname}_t={lshtype}_k={K}_qs={Q}_f={fold}.lsh.bench.txt"
KD_BENCHMARK_NAME = "{fullname}_k={K}_qs={Q}_f={fold}.kd.bench.txt"
LSHRFILE_NAME = "{fullname}_t={lshtype}_k={K}_qs={Q}_f={fold}.rfile.txt"
GAUSSCONF_NAME = "{fullname}.conf.txt"

LOG_NAME = '{fullname}_qs={Q}_f={fold}_k={K}.log'
FINAL_RESULT_NAME = 'results.{fullname}_qs={Q}_f={fold}_k={K}.txt'
