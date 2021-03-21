class JsonTemplate:

    def __init__(self, file_name):
        self.template = {}
        stack_dict = [(0, self.template)]
        last_dict = None
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                if line.endswith('\n'):
                    line = line[:-1]
                indent, line = self.cut_indent(line)
                key, val = line.split(': ')
                if val not in ['yes', 'no']:
                    raise
                if indent > stack_dict[-1][0]:
                    last_dict['items'] = {}
                    stack_dict.append((indent, last_dict['items']))
                while indent < stack_dict[-1][0]:
                    stack_dict.pop(-1)
                if indent == stack_dict[-1][0]:
                    last_dict = {'need': (val == 'yes')}
                    stack_dict[-1][1][key] = last_dict
                else:
                    raise
        print(self.template)

    @staticmethod
    def cut_indent(line):
        indent = 0
        pos = 0
        while pos < len(line):
            if line[pos] == ' ':
                indent += 1
                pos += 1
            elif line[pos] == '\t':
                indent += 4
                pos += 1
            else:
                break
        return indent, line[pos:]

    def filter_json(self, data):
        def rec(template, json_data):
            res = {}
            for key in template:
                if not template[key]['need']:
                    continue
                if key not in json_data:
                    print(key)
                    print(json_data)
                    continue
                if 'items' in template[key]:
                    res[key] = rec(template[key]['items'], json_data[key])
                else:
                    res[key] = json_data[key]
            return res

        return rec(self.template, data)
