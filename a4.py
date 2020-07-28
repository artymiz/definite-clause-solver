# returns True if, and only if, string s is a valid variable name
def is_atom(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return False
    return is_letter(s[0]) and all(is_letter(c) or c.isdigit() for c in s[1:])


def is_letter(s):
    return len(s) == 1 and s.lower() in "_abcdefghijklmnopqrstuvwxyz"


class Interpreter:
    def __init__(self):
        self.atoms = []
        self.rules = {}
        self.kb_loaded = False
    

    def tell(self, items):
        """Add a new atom to the knowledge base"""
        if not items:
            print('Error: tell needs at least one atom')
            return
        for item in items:
            if not is_atom(item):
                print('Error: "%s" is not a valid atom' % item)
                return
        for atom in items:
            self.atoms.append(atom)
            print('   atom "%s" added to kb' % atom)


    def load(self, file_name):
        """
        Load a set of definite clause rules from a text file in the
        following format:
            INFERRED_ATOM <-- ATOM_1 & ATOM_2 & ... & ATOM_N
        """
        def print_error():
            print('Error: %s is not a valid knowledge base' % file_name)

        try:
            file = open(file_name)
        except IOError:
            print('Error: could not open file')
            return
        with file:
            count = 0
            rules = {}
            for line in file.readlines():
                sentence = line.strip()
                if sentence == "":
                    continue
                
                split_line = [x.strip() for x in sentence.split('<--')]
                split_line = [x for x in split_line if x]
                if len(split_line) < 2:
                    print_error()
                    return
                
                atoms = [x.strip() for x in split_line[1].split('&')]
                for atom in atoms:
                    if not is_atom(atom) or atom == '':
                        print_error()
                        return
                rules[split_line[0]] = atoms
                count += 1

            # print added rules
            for k,v in rules.items():
                line = '   ' + k + ' <-- '
                for atom in v[:-1]:
                    line += atom + ' & '
                line += v[-1]
                print(line)

            self.rules = rules
            if self.kb_loaded:
                self.atoms = []
            self.kb_loaded = True
            print('\n   %d new rule(s) added' % count)            
            

    def infer_all(self):
        def print_items(items, seperator):
            line = '      '
            if not items:
                line += '<none>'
            else:
                for item in items[:-1]:
                    line += item + seperator
                line += items[-1]
            print(line)

        inferred = []
        while(True):
            inferred_count = 0
            all_atoms = self.atoms + inferred
            for k,v in self.rules.items():
                if k not in all_atoms:
                    if all(item in all_atoms for item in v):
                        inferred.append(k)
                        inferred_count += 1
            if inferred_count == 0:
                break

        print('   Newly inferred atoms:')
        print_items(inferred, ' ')
        print('   Atoms already know to be true:')
        print_items(self.atoms, ', ')
        self.atoms.extend(inferred)


    def run(self):
        """Program loop"""
        while(True):
            line = input('kb> ')
            args = line.strip().split()
            if args:
                if args[0] == 'tell':
                    self.tell(args[1:])
                elif args[0] == 'load':
                    self.load(args[1])
                elif args[0] == 'infer_all':
                    self.infer_all()
                elif args[0] in ['exit', 'quit']:
                    return
                else:
                    print('Error: unknown command "%s"' % args[0])
                print()


if __name__ == "__main__":
    interpreter = Interpreter()
    interpreter.run()
