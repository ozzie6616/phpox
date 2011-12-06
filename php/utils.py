import random
import sys 
import string
import json
import os
from string import Template

class util_functions(object):
    def __init__(self):
        self.symbol_table = {} 
        self.used_name = [] #initialed in read_json()
        self.jfile = None
        self.gen_utils_functions()

    def clean(self):
        os.unlink('/tmp/php_utils_table_%d' % os.getpid())
        os.unlink('/tmp/php_utils_scripts_%d' % os.getpid())

    def gen_utils_functions(self):
        #xXx it's ULTRA UGLY!!!
        #Because the replacement/xxx.call() is called in very early stage.
        #Those function codes excute when importing apd_function.py
        #Thus I have problem to pass the real symbols into those functions.
        try:
            fd = open('/tmp/php_utils_table_%d' % os.getpid(), 'r')
            j_code = fd.read()
            fd.close()

            obj = json.loads(j_code)
            self.symbol_table = obj['symbol_table']
            self.used_name = obj['used_name']
            fd = open('/tmp/php_utils_scripts_%d' % os.getpid(), 'r')
            ret = fd.read()
            fd.close()
        except:
            ret = ''
            # the order is very important!!!
            ret += self.def_string_parser()
            ret += self.def_multiple_irc()
            obj = {
                'used_name':self.used_name,
                'symbol_table':self.symbol_table,
            }
            fd = open('/tmp/php_utils_table_%d' % os.getpid(), 'w')
            fd.write(json.dumps(obj))
            fd.close()
            fd = open('/tmp/php_utils_scripts_%d' % os.getpid(), 'w')
            fd.write(ret)
            fd.close()
        return ret

    def get_symbol(self, name=None ):
        if( name is None ):
            return self.symbol_table
        else:
            return self.symbol_table[name]
        
    def symbol_append(self, symbol, masq):
        if(symbol in self.symbol_table):
            raise BaseException('Name collaps: %s' % symbol)
        self.symbol_table[symbol] = masq
        self.used_name.append(masq)


    def generate_random_name(self):
        ret = ''
        while True:
            prefix = '' . join(random.choice((string.ascii_uppercase + string.ascii_lowercase)) for x in range(3))
            postfix = '' . join(random.choice(
                (string.ascii_uppercase + string.ascii_lowercase + string.digits))
                for x in range(5))
            if((prefix + postfix) not in self.used_name):
                ret = (prefix + postfix)
                break
        return ret

    def def_string_parser(self):
        ret = ''
        replacement = {
            'simple_code_parser':'',
            }
        replacement['simple_code_parser'] = self.generate_random_name()
        self.symbol_append('simple_code_parser', replacement['simple_code_parser'])
        #self.symbol_table['simple_code_parser'] = replacement['simple_code_parser']
        fd = open("php/string_paser.template")
        line = ''
        for l in fd.readlines():
            line += l
        fd.close()
        t = Template(line)
        ret += t.substitute(replacement)
        return ret;

    def def_multiple_irc(self):
        ret = ''
        replacement = {
            'multiple_irc':'',
            'parsed_strings':'',
            'find_irc_server':'',
            'multiple_irc_return_false':'',
            'simple_code_parser':'', #it's should be generated.
        }
        replacement['multiple_irc'] = self.generate_random_name()
        self.symbol_append('multiple_irc', replacement['multiple_irc'])
        replacement['parsed_strings'] = self.generate_random_name()
        self.symbol_append('parsed_strings', replacement['parsed_strings'])
        replacement['find_irc_server'] = self.generate_random_name()
        self.symbol_append('find_irc_server', replacement['find_irc_server'])
        replacement['multiple_irc_return_false'] = self.generate_random_name()
        self.symbol_append('multiple_irc_return_false', replacement['multiple_irc_return_false'])
        replacement['simple_code_parser'] = self.get_symbol('simple_code_parser')
        fd = open("php/multiple_irc.template")
        line = ''
        for l in fd.readlines():
            line += l
        fd.close()
        t = Template(line)
        ret += t.substitute(replacement)
        return ret
        
#testing program
if __name__ == "__main__":
    utils = util_functions()
    print utils.gen_utils_functions()
    print "%s();" % utils.get_symbol(name='simple_code_parser')
    utils.clean()