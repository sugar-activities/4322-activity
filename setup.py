#!/usr/bin/env python
try:
    from sugar.activity import bundlebuilder
    bundlebuilder.start()
except ImportError:
    import os
    os.system("find ./ | sed 's,^./,ProducePuzzle.activity/,g' > MANIFEST")
    os.chdir('..')
    os.system('zip -r ProducePuzzle-1.xo ProducePuzzle.activity')
    os.system('mv ProducePuzzle-1.xo ./ProducePuzzle.activity')
    os.chdir('ProducePuzzle.activity')
