import os
import sys
import tempfile

import datahelper as dh
import genGauss
from logger import printl
from programs import vec2msbin, runordel
import sysarg
import config
from subprocess import call
from statter import MSStatter, PMSStatter
import sprinter
from dataenums import MSTypeEnum

def fullprocess(
        data,
        overwritedata=False,
        overwriteindex=False,
        overwritebench=False):
    gendata(data, overwritedata, overwriteindex)
    process(data, overwriteindex, overwritebench)
    if data.cfg['mstype'] == MSTypeEnum.prunedmvp:
        st = PMSStatter(data.getFoldedFiles('msbenchfilepath'), data)
    else:
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
    indextype = MSTypeEnum.prog(indextype)
    print("---------------------------------------", data.cfg['mstype'], indextype)
    bprog = "build-%s-vectors"  %indextype #specify the prog to use
    qprog = "query-%s-vectors"  %indextype #specify the query prog to use

    if overwriteindex or not os.path.exists(data.msindexfilepath):
        ### annoyingly it seems the build has a filename limit
        ### make a temp file then rename
        __, of = tempfile.mkstemp(
            dir=data.datadir,
            prefix='tt{}_{}_'.format(data.cfg.S, data.cfg.D))
        cmd = [ bprog,
                data.msbinfilepath,
                "0",
                of,
                '3', # bucket size
                '3','3']

        runordel(
            cmd,
            data.msbuildbenchfilepath,
            outtofile=data.msbuildbenchfilepath,
            overwrite=overwriteindex,
            printcmd=True)
        printl('renaming idx\n$> mv {} {}'.format(
            of,data.msindexfilepath))
        os.rename(of, data.msindexfilepath)

    cmd = [ qprog,
            data.msindexfilepath
          ]
    if not os.path.exists(data.msbenchfilepath) or overwritebench:
        if data.cfg['mstype'] == MSTypeEnum.prunedmvp:
            cmdstr = "(time %s %s %d %f) < %s 1<&-  2> %s " %(
                qprog,
                data.msindexfilepath,
                data.cfg.D,
                data.cfg['prune_threshold'],
                data.qmsvecfilepath,
                data.msbenchfilepath)
            pst = PMSStatter(data.getFoldedFiles('msbenchfilepath'), data)
            mean = pst.meanofall
            var = pst.varofall
            dev = pst.devofall
            print("FFFF", mean, var, dev)
            cmdstr = "(time %s %s %d %f %f %f %f) < %s 1<&-  2> %s " %(
                qprog,
                data.msindexfilepath,
                data.cfg.D,
                data.cfg['prune_threshold'],
                mean,
                var,
                dev,
                data.qmsvecfilepath,
                data.msbenchfilepath)
        else:
            cmdstr = "(time %s %s) < %s 1<&-  2> %s " %(
                qprog,
                data.msindexfilepath,
                data.qmsvecfilepath,
                data.msbenchfilepath)
        print(cmdstr)
        call(cmdstr, shell=True)


if __name__ == "__main__":
    if len(sys.argv)==1:
        sys.argv = sysarg.args(__file__)
    if '--from-file' in sys.argv:
        fromcl = list(sys.argv)
        sys.argv = sysarg.args(__file__)
        sys.argv.extend(fromcl)
    ap = sysarg.getArgParse(
        sys.argv, needsquerydata=True)
    args, unknown = ap.parse_known_args()
    overwriteindex = '--overwriteindex' in sys.argv
    overwritedata = '--overwritedata' in sys.argv
    overwritebench = '--overwritebench' in sys.argv
    if '--overwriteall' in sys.argv:
        overwriteindex = True
        overwritedata = True
        overwritebench = True

    runcfg = config.Config(vars(args))
    rundata = dh.Data(runcfg)

    fullprocess(
        rundata,
        overwritedata,
        overwriteindex,
        overwritebench)
