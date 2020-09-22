#!/usr/bin/env python3
# config: utf-8

import base64
import hashlib
import os
import re
import shutil
import sys
from concurrent.futures import ProcessPoolExecutor, wait

import xmltodict

LEAK_BLK = '0'
SUPP_BLK = '1'
FD_BLK = '2'


def parse_frames(frames):
    _blk = []
    _blkh = []
    ab = 'at'
    for frame in frames:
        _l = '   %s %s: ' % (ab, frame['ip'])
        ab = 'by'
        _fn = frame['fn'] if 'fn' in frame else '???'
        _l += _fn + ' '
        if 'file' in frame and 'line' in frame:
            _l += '(%s:%s)' % (frame['file'], frame['line'])
        elif 'obj' in frame:
            _l += '(in %s)' % frame['obj']
        else:
            continue
        _blk += [_l]
        _blkh += [_fn]
    return _blk, hashlib.sha1('\n'.join(_blkh).encode()).hexdigest()


def parse_val_log(name, val_log, output):
    try:
        with open(val_log, 'rb') as fp:
            jd = xmltodict.parse(fp)['valgrindoutput']
    except:
        jd = None
    if not jd:
        return
    if 'error' not in jd and 'stack' not in jd:
        return
    _suite = os.path.basename(os.path.dirname(val_log))
    _fn = os.path.basename(val_log).replace('.xml', '')
    _plt = _fn.split('_')[-1]
    _of = _suite + '@' + _fn
    ofd = open(os.path.join(output, _of), 'a')
    _hashes = []
    if 'error' in jd:
        if not isinstance(jd['error'], list):
            jd['error'] = [jd['error']]
        for err in jd['error']:
            if 'xwhat' in err:
                _what = err['xwhat']['text']
            else:
                _what = err['what']
            if 'auxwhat' in err:
                if isinstance(err['auxwhat'], list):
                    _auxwhat = ' '.join(err['auxwhat'])
                else:
                    _auxwhat = err['auxwhat']
            else:
                _auxwhat = None
            _stacks = err['stack']
            if not isinstance(_stacks, list):
                _stacks = [_stacks]
            _pstack = []
            for _stack in _stacks:
                _pstack.append(parse_frames(_stack['frame']))
            _blk = '\n'.join(['\n'.join(x[0]) for x in _pstack])
            _hash = hashlib.sha1(
                '\n'.join([x[1] for x in _pstack]).encode()).hexdigest()
            if _hash not in _hashes:
                _hashes.append(_hash)
                _blk = [_what, '\n'.join(_pstack[0][0])]
                if _auxwhat:
                    _blk.append(_auxwhat)
                if len(_pstack) > 1:
                    _blk.append('\n'.join(_pstack[1][0]))
                _blk.append('')
                _blk = base64.b64encode('\n'.join(_blk).encode()).decode()
                ofd.write('|'.join([LEAK_BLK, _suite, _plt,
                                    _hash, _blk]) + '\n')
                ofd.flush()
            if 'suppression' in err and 'rawtext' in err['suppression']:
                _supp = err['suppression']['rawtext'] + '\n'
                _supp = re.sub(r'([\s]+obj:)/tmp/xf-dll/xf-[\w]+.tmp',
                               r'\1*xf-dll*', _supp)
                _supp = _supp.encode()
                _hash = hashlib.sha1(_supp).hexdigest()
                if _hash not in _hashes:
                    _hashes.append(_hash)
                    _supp = base64.b64encode(_supp).decode()
                    ofd.write('|'.join([SUPP_BLK, _suite, _plt,
                                        _hash, _supp]) + '\n')
                    ofd.flush()
    logfile = os.path.splitext(val_log)[0] + '.log'
    if 'stack' in jd and os.path.exists(logfile):
        if not isinstance(jd['stack'], list):
            jd['stack'] = [jd['stack']]
        lines = []
        with open(logfile) as fp:
            lines = fp.readlines()
        if lines:
            fdlist = []
            len_lines = len(lines) - 1
            for idx, line in enumerate(lines):
                if (idx != len_lines and
                        'inherited from parent' in lines[idx + 1]):
                    continue
                m = re.match(r'.*(Open file descriptor [\d]+:[\s\w/\.]*)',
                             line)
                if m:
                    fdlist += [m.group(1)]
                    continue
                m = re.match(r'.*(Open AF_INET socket [\d]+: [<>\w\.:]+ <-> [<>\w\.:]+)',
                             line)
                if m:
                    fdlist += [m.group(1)]
            if fdlist:
                for idx, stack in enumerate(jd['stack']):
                    _blk = [fdlist[idx].strip()]
                    _frs = parse_frames(stack['frame'])
                    _blk.extend(_frs[0])
                    _hash = _frs[1]
                    _blk = '\n'.join(_blk) + '\n\n'
                    _blk = _blk.encode()
                    if _hash not in _hashes:
                        _hashes.append(_hash)
                        _blk = base64.b64encode(_blk).decode()
                        ofd.write('|'.join([FD_BLK, _suite, _plt,
                                            _hash, _blk]) + '\n')
                        ofd.flush()
    if 'suppression' in jd:
        if not isinstance(jd['suppression'], list):
            jd['suppression'] = [jd['suppression']]
        for supp in jd['suppression']:
            _supp = supp['rawtext'] + '\n'
            if '/xf-dll/xf-' in _supp:
                _supp = re.sub(r'([\s]+obj:)/tmp/xf-dll/xf-[\w]+.tmp',
                               r'\1*xf-dll*', _supp)
            _supp = _supp.encode()
            _hash = hashlib.sha1(_supp).hexdigest()
            if _hash not in _hashes:
                _hashes.append(_hash)
                _supp = base64.b64encode(_supp).decode()
                ofd.write('|'.join([SUPP_BLK, _suite, _plt,
                                    _hash, _supp]) + '\n')
                ofd.flush()


def parse_val_log_dir(val_log_dir, output_file):
    files = [
        lf for si in os.scandir(val_log_dir)
        for lf in os.scandir(si.path) if lf.path.endswith('.xml')
    ]
    output = os.path.join(os.path.dirname(base_dir), 'valgrind_results')
    if not os.path.isdir(output):
        os.makedirs(output, 0o755)
    with ProcessPoolExecutor(max_workers=20) as executor:
        threads = []
        for lf in files:
            with open(lf.path, 'rb') as fp:
                if b'\0' in fp.read(512):
                    print(lf.path)
                    continue
            threads.append(
                executor.submit(
                    parse_val_log,
                    lf.name,
                    lf.path,
                    output
                )
            )
        wait(threads)
    if not os.path.isdir(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file), 0o755)
    ofd = open(output_file, 'w+')
    for fn in os.scandir(output):
        with open(fn.path) as fd:
            ofd.write(fd.read())
            ofd.flush()
    ofd.close()
    shutil.rmtree(output, ignore_errors=True)


if __name__ == '__main__':
    base_dir = sys.argv[1]
    output_file = sys.argv[2]
    parse_val_log_dir(base_dir, output_file)
