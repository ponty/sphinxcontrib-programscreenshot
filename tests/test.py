from easyprocess import EasyProcess
from nose.tools import eq_


def test_dummy():
    p=EasyProcess('ls').call()
    #eq_(p.return_code, 0)