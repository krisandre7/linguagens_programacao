from io import StringIO
import math
import random
import sys

class Stack:
    # Valida se os operandos são válidos
    def _validate_operands(self):
        if len(self.ls) < 2:
            return False
        
        if not (isinstance(self.ls[-1], (int, float)) and isinstance(self.ls[-2], (int, float))):
            return False
    
    # Empilha em D o resultado da soma
    def sum(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(self.ls.pop() + self.ls.pop())
        return True
    
    # Empilha em D o resultado da subtração
    def subtract(self):
        if self._validate_operands() == False:
            return False
        
        n1 = self.ls.pop()
        n2 = self.ls.pop()
        self.ls.append(n2 - n1)
        return True
    
    # Empilha em D o resultado da multiplicação
    def multiply(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(self.ls.pop() * self.ls.pop())
        return True
    
    # Empilha em D o resultado da divisão
    def divide(self):
        if self._validate_operands() == False or self.ls[-1] == 0:
            return False
        n1 = self.ls.pop()
        n2 = self.ls.pop()
        self.ls.append(n2 / n1)
        return True
    
    # Empilha em D o resultado do módulo
    def mod(self):
        if self._validate_operands() == False:
            return False
        n1 = self.ls.pop()
        n2 = self.ls.pop()
        self.ls.append(n2 % n1)
        return True
    
    # Empilha em D o resultado da raiz quadrada
    def sqrt(self):
        if len(self.ls) < 1 or self.ls[-1] < 0:
            return False
        
        self.ls.append(math.sqrt(self.ls.pop()))
        return True
    
    # Empilha -1 em D
    def true(self):
        self.ls.append(-1)
        return True
    
    # Empilha 0 em D
    def false(self):
        self.ls.append(0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador >
    def gt(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(-1 if self.ls.pop() > self.ls.pop() else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador <
    def lt(self):
        if self._validate_operands() == False:
            return False
        
        el1 = self.ls.pop()
        el2 = self.ls.pop()
        self.ls.append(-1 if el2 < el1 else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador >=
    def gte(self):
        if self._validate_operands() == False:
            return False
        
        el1 = self.ls.pop()
        el2 = self.ls.pop()
        self.ls.append(-1 if el2 >= el1 else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador <=
    def lte(self):
        if self._validate_operands() == False:
            return False
        
        el1 = self.ls.pop()
        el2 = self.ls.pop()
        self.ls.append(-1 if el2 <= el1 else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador ==
    def eq(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(-1 if self.ls.pop() == self.ls.pop() else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador !=
    def neq(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(0 if self.ls.pop() == self.ls.pop() else -1)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador relacional or
    def or_op(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(-1 if self.ls.pop() or self.ls.pop() else 0)
        return True
    
    # Empilha 0 ou -1 em D de acordo com operador relacional and
    def and_op(self):
        if self._validate_operands() == False:
            return False
        self.ls.append(-1 if self.ls.pop() and self.ls.pop() else 0)
        return True
    
    # Desempilha valor no topo da pilha D (a b -- a)
    def drop(self):
        if len(self.ls) < 1:
            return False
        
        self.ls.pop()
        return True
    
    # Troca valores no topo de D (a b -- b a)
    def swap(self):
        if len(self.ls) < 2:
            return False
        
        self.ls[-1], self.ls[-2] = self.ls[-2], self.ls[-1]
        return True
    
    # Duplica valor no topo de D (a -- a )
    def dup(self):
        if len(self.ls) < 1:
            return False
        
        self.ls.append(self.ls[-1])
        return True
    
    # Rotaciona top-3 valores na pilha D (a b c d -- a d b c)
    def rot(self):
        if len(self.ls) < 3:
            return False
        
        self.ls[-1], self.ls[-2], self.ls[-3] = self.ls[-3], self.ls[-1], self.ls[-2]
        return True
    
    # Copia n-esimo valor pro topo de D (2 PICK com a b c -- a b c a)
    def pick(self):
        if len(self.ls) < 2:
            return False
        
        # copy the value at the n-th position to the top of the stack
        n = self.ls.pop()
        
        # n always comes as a float. check if the value is an integer
        if not n.is_integer():
            return False
        else:
            n = int(n)
        
        if n < 0 or n >= len(self.ls):
            return False
        
        self.ls.append(self.ls[-n - 1])
        
    def over(self):
        if len(self.ls) < 2:
            return False
        
        self.ls.append(self.ls[-2])
        return True

    def randn(self):
        self.ls.append(random.random())
        return True

    def __init__(self):
        self.ls = []

    def __len__(self):
        return len(self.ls)

    def __str__(self):
        return str(self.ls)


class ForthVirtualMachine:
    def __init__(self):
        self.d_stack = Stack()
        self.r_stack = Stack()

    def stacks(self):
        return self.d_stack, self.r_stack


class LikeForthInterpreter(object):
    def __init__(self):
        self.fvm = ForthVirtualMachine()
        self.words = dict([
            ('.s', self.dots), ('.d', self.dotd),
            (".", self.pop), ('+', self.fvm.d_stack.sum),
            ('-', self.fvm.d_stack.subtract), ('*', self.fvm.d_stack.multiply),
            ('/', self.fvm.d_stack.divide), ('%', self.fvm.d_stack.mod),
            ('sqrt', self.fvm.d_stack.sqrt), ('true', self.fvm.d_stack.true),
            ('false', self.fvm.d_stack.false), ('>', self.fvm.d_stack.gt),
            ('<', self.fvm.d_stack.lt), ('>=', self.fvm.d_stack.gte),
            ('<=', self.fvm.d_stack.lte), ('eq', self.fvm.d_stack.eq),
            ('neq', self.fvm.d_stack.neq), ('and', self.fvm.d_stack.and_op),
            ('or', self.fvm.d_stack.or_op), ('drop', self.fvm.d_stack.drop),
            ('swap', self.fvm.d_stack.swap), ('dup', self.fvm.d_stack.dup),
            ('rot', self.fvm.d_stack.rot), ('pick', self.fvm.d_stack.pick),
            ('clear', self.clear()), ('cr', self.newline), ('acceptn', self.acceptn),
            ('over', self.fvm.d_stack.over), ('randn', self.fvm.d_stack.randn),
            ('i', self.append_index)
        ])
        self.current_index = -1
        
    def d_stack_to_r_stack(self):
        if len(self.fvm.d_stack.ls) < 1:
            return False
        
        self.fvm.r_stack.ls.append(self.fvm.d_stack.ls.pop())
        return True
    
    def r_stack_to_d_stack(self):
        if len(self.fvm.r_stack.ls) < 1:
            return False
        
        self.fvm.d_stack.ls.append(self.fvm.r_stack.ls.pop())
    
    def copy_r_stack_to_d_stack(self):
        self.fvm.d_stack.ls.append(self.fvm.r_stack.ls[-1])
        
    def clear(self):
        self.fvm.d_stack.ls.clear()
        self.fvm.r_stack.ls.clear()
        return True
        
    def dots(self):
        D, R = self.fvm.stacks()
        print(f"D <{len(D)}> {str(D)} ")
        print(f"R <{len(R)}> {str(R)} ")
        return True

    def dotd(self):
        for w in self.words:
            if not callable(self.words[w]):
                print('%s: %s' % (w, list(self.words[w])))
        return True
    
    def pop(self):
        if len(self.fvm.d_stack) < 1:
            return False
        print(self.fvm.d_stack.ls.pop())
        return True
    
    def newline(self):
        print()
        return True
    
    # Lê um número real do teclado e o insere na pilha D
    def acceptn(self):
        try:
            n = float(input())
            self.fvm.d_stack.ls.append(n)
            return True
        except ValueError:
            return False

    def fcompile(self, tokens):
        'Add keyword to words dictionary'
        keyword = tokens[0]
        try:
            semicolon_pos = tokens.index(';')
        except ValueError:
            return False
        body = tokens[1:semicolon_pos]
        self.words[keyword] = body
        return tokens[semicolon_pos + 1:]
    
    def append_index(self):
        if self.current_index == -1:
            return False
        
        self.fvm.d_stack.ls.append(self.current_index)
        return True

    def interpret(self, tokens):
        if not tokens:
            return True
        
        if tokens[0] == ':':
            rem = self.fcompile(tokens[1:])
            
            if rem == False:
                return False
            else:
                return self.interpret(rem)
            
        if tokens[0] == '.\"':
            tokens = tokens[1:]
            
            try:
                end_quote = tokens.index('\"')
                print(' '.join(tokens[:end_quote]))
                return self.interpret(tokens[end_quote + 1:])
            except ValueError:
                return False

        # Comentário
        if tokens[0] == '(':
            try:            
                return self.interpret(tokens[tokens.index(')') + 1:])
            except ValueError:
                return False
        
        if tokens[0] == 'do':
            try:
                start = int(self.fvm.d_stack.ls.pop())
                end = int(self.fvm.d_stack.ls.pop())
                
                loop_pos = tokens.index('loop')
                
                loop_tokens = tokens[1:loop_pos]
                remaining_tokens = tokens[loop_pos + 1:]
                for i in range(start, end):
                    self.current_index = i
                    self.interpret(loop_tokens)
                self.current_index = -1
                return self.interpret(remaining_tokens)
                
            except ValueError:
                return False
            
        if tokens[0] == 'if':
            try:
                condition = self.fvm.d_stack.ls.pop()
                if condition == -1 and 'else' in tokens:
                    try:
                        else_pos = tokens.index('else')
                        then_pos = tokens.index('then')
                        tokens = tokens[1:else_pos] + tokens[then_pos + 1:]
                        self.interpret(tokens)
                    except ValueError:
                        return False

                if condition == 0 and 'else' in tokens:
                    try:
                        else_pos = tokens.index('else')
                        then_pos = tokens.index('then')
                        tokens = tokens[else_pos + 1:then_pos] + tokens[then_pos + 1:]
                        self.interpret(tokens)
                    except ValueError:
                        return False
                
                if condition == -1 and 'else' not in tokens:
                    try:
                        then_pos = tokens.index('then')
                        tokens = tokens[1:then_pos] + tokens[then_pos + 1:]
                        self.interpret(tokens)
                    except ValueError:
                        return False
                
                return self.interpret(tokens[tokens.index('then') + 1:])
            except ValueError:
                return False
            
        if tokens[0] in self.words:
            fun = self.words[tokens[0]]
            if callable(fun):
                if fun():
                    return self.interpret(tokens[1:])
                else:
                    return False
            else:
                return self.interpret(list(fun) + tokens[1:])
        
        # Insere número na pilha de dados D
        if isinstance(tokens[0], (int, float)):
            self.fvm.d_stack.ls.append(tokens[0])
            return self.interpret(tokens[1:])            
        
        return False

    # Função para quebrar a string em tokens,
    # separando por espaços
    def tokenize(self, s):
        def string_to_num(s):
            try:
                return float(s)
            except ValueError:
                return s
        return [string_to_num(t) for t in s.split()]

    # Função REPL
    def REPL(self):
        input_str = input('?> ')
        if input_str != 'bye':
            ok = self.interpret(self.tokenize(input_str))
            if not ok:
                print('?')
            else:
                print('<ok>')
            self.REPL()

    # Execução principal
    def run(self, txt = None):
        self.__init__()
        if txt is None:
            print('Micro Forth (September 2024)')
            self.REPL()
        else:
            self.interpret(self.tokenize(txt))

forth = LikeForthInterpreter()

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def test():
    def test_stdout(forth_code):
        with Capturing() as output:
            forth.run(forth_code)
        return output
    
    assert test_stdout('4 5 + .') == ['9.0']
    assert test_stdout('4 5 - .') == ['-1.0']
    
    forth.run('1 2 +'); assert forth.fvm.d_stack.ls.pop() == 3
    forth.run('2 1 -'); assert forth.fvm.d_stack.ls.pop() == 1
    forth.run('1 2 *'); assert forth.fvm.d_stack.ls.pop() == 2
    forth.run('2 1 /'); assert forth.fvm.d_stack.ls.pop() == 2
    forth.run('1 2 /'); assert forth.fvm.d_stack.ls.pop() == 0.5
    forth.run('2 0 /')
    forth.run('2 1 %'); assert forth.fvm.d_stack.ls.pop() == 0
    forth.run('4 sqrt'); assert forth.fvm.d_stack.ls.pop() == 2
    forth.run('-1 sqrt')
    forth.run('1 2 eq'); assert forth.fvm.d_stack.ls.pop() == 0
    forth.run('1 2 neq'); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('1 2 >'); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('2 1 <'); assert forth.fvm.d_stack.ls.pop() == 0
    forth.run('2 1 >='); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('2 1 <='); assert forth.fvm.d_stack.ls.pop() == 0
    forth.run('1 2 and'); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('1 2 or'); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('true'); assert forth.fvm.d_stack.ls.pop() == -1
    forth.run('false'); assert forth.fvm.d_stack.ls.pop() == 0
    
    forth.run('1 2 swap'); assert forth.fvm.d_stack.ls.pop() == 1 and forth.fvm.d_stack.ls.pop() == 2
    forth.run('1 drop'); assert len(forth.fvm.d_stack.ls) == 0
    forth.run('1 2 dup'); assert forth.fvm.d_stack.ls.pop() == 2 and forth.fvm.d_stack.ls.pop() == 2
    forth.run('1 2 3 4 rot'); assert forth.fvm.d_stack.ls == [1, 3, 4, 2]
    forth.run('1 2 3 2 pick'); assert forth.fvm.d_stack.ls == [1, 2, 3, 1]; forth.clear()
    
    assert test_stdout("""( ** Quadrado ** )
              : sq dup * ;
              5 sq .
              """) == ['25.0']
    
    assert test_stdout("""( ** Fatorial ** )
                : fat ( n -- n! ) 
                    dup 2 < if
                        drop 1
                    else
                        dup 1 - fat *
                    then
                ;
                5 fat .
                """) == ['120.0']
    
    assert len(test_stdout('4 0 do .\" * \" loop')) == 4
    
if __name__ == '__main__':
    forth = LikeForthInterpreter()
    test()
    
    forth.run()