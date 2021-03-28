# TODO переписать получше
# TODO улучшить грамматику

class Grammar:

    @staticmethod
    def parse_number(text):
        try:
            return float(text)
        except ValueError:
            return None

    @staticmethod
    def parse_grammar_line(line):
        name, rem = line.split('=')
        name = name.strip()
        rem = rem.strip()
        rules = []
        for item in rem.split('|'):
            item = item.strip()
            parts = [p.replace('\\_', ' ') for p in item.split()]
            rule = []
            for part in parts:
                if part == 'default':
                    rule.append((part, 'default'))
                elif part.isalpha() and part.isupper():
                    rule.append((part, 'non_terminal'))
                else:
                    rule.append((part, 'terminal'))
            rules.append(rule)
        return name, rules

    @staticmethod
    def get_default_function(name):
        if name == 'NUMBER':
            return Grammar.parse_number
        return None

    def __init__(self, file_name):
        self.rules = {}
        self.RESULT = ('RESULT', 'non_terminal')
        self.cache = {}
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line == '':
                    continue
                name, rules = self.parse_grammar_line(line)
                for rule in rules:
                    for i in range(len(rule)):
                        if rule[i][1] == 'default':
                            rule[i] = (self.get_default_function(name), 'default')
                self.rules[name] = rules
        # print(self.RESULT)
        # for key in self.rules:
        #     print(key, self.rules[key])

    def parse_text(self, text, node):
        hash_key = (text, str(node))
        if hash_key in self.cache:
            return self.cache[hash_key]
        result = []
        text = text.strip()
        if node[1] == 'terminal':
            if text == node[0]:
                result.append(text)
        elif node[1] == 'non_terminal':
            name = node[0]
            for rule in self.rules[name]:
                if len(rule) == 1:
                    for item in self.parse_text(text, rule[0]):
                        if rule[0][1] in ['terminal', 'default']:
                            result.append([{rule[0][1] : item}])
                        else:
                            result.append([{rule[0][0] : item}])
                elif len(rule) == 2:
                    for i in range(1, len(text)):
                        if text[i] == ' ':
                            continue
                        left = self.parse_text(text[:i], rule[0])
                        right = self.parse_text(text[i:], rule[1])
                        for item1 in left:
                            for item2 in right:
                                result.append([{rule[0][0] : item1}, {rule[1][0] : item2}])
        elif node[1] == 'default':
            if node[0](text):
                result.append(text)
        self.cache[hash_key] = result
        return result

    def parse(self, text):
        return self.parse_text(text.lower(), self.RESULT)
