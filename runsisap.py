import os
import sys
import tempfile

import datahelper as dh
import genGauss
from programs import vec2msbin, runordel, run
import sysarg
import config
from subprocess import call
from statter import MSStatter
import sprinter

def fullprocess(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):
    gendata(data, overwritedata, overwriteindex)
    process(data, overwriteindex, overwritebench)
    st = MSStatter(data.getFoldedFiles('msbenchfilepath'), data)
    sprinter.printstats(st)
    return st


def gendata(data, overwritedata=False, overwriteindex=False):
    dh.Data.mkdirs(data.benchdir, data.indexdir)
    # vec2(data, overwrite=overwrite)
    if data.cfg.synthetic:
        genGauss.process(data, overwritedata)
        vec2msbin(data, overwritedata, True)

def process(data, overwriteindex=False, overwritebench=False):
    indextype = data.cfg['mstype']
    bprog = "build-%s-vectors"  %indextype #specify the prog to use
    qprog = "query-%s-vectors"  %indextype #specify the query prog to use

    ### annoyingly it seems the build has a filename limit
    ### make a temp file then rename
    data.mkdirs('tempidx')
    __, of = tempfile.mkstemp(
        dir='./tempidx',
        prefix='{}_{}'.format(data.cfg.S, data.cfg.D))
    cmd = [ bprog,
            data.msbinfilepath,
            "0",
            of,
            '3', # bucket size
            "3",
            "6"]

    ran = runordel(
        cmd,
        data.msbuildbenchfilepath,
        outtofile=data.msbuildbenchfilepath,
        overwrite=overwriteindex,
        printcmd=True)
    if ran:
        data.remove(data.msindexfilepath)
        os.rename(of, data.msindexfilepath)

    cmd = [ qprog,
            data.msindexfilepath
          ]
    if not os.path.exists(data.msbenchfilepath) or overwritebench:
        cmdstr = "(time %s %s) < %s 1<&-  2> %s " %(
            qprog,
            data.msindexfilepath,
            data.qmsvecfilepath,
            data.msbenchfilepath)
        print(cmdstr)
        call(cmdstr, shell=True)

        # run(cmd,
        #     stdin=open(data.qmsvecfilepath),
        #     stderr=open(data.msbenchfilepath,'w'),
        #     printcmd=True)


if __name__ == "__main__":
    overwriteindex = True
    overwritedata = True
    overwritebench = True
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)
    args, unknown = ap.parse_known_args()

    runcfg = config.Config(vars(args))
    rundata = dh.Data(runcfg)

    fullprocess(
        rundata,
        overwritedata,
        overwriteindex,
        overwritebench)



