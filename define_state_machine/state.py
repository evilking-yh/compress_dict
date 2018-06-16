class State(object):
    def __init__(self, value, re = False):
        self.value = value
        self.re = re
        self.num = ()
        self.child_states = {}  # 存普通 state
        self.re_states = {}     # 存 模糊匹配 state
        if self.re:
            temp = value[1:-1].split(',')
            self.num = (int(temp[0]), int(temp[1]))

    def add_state(self, value):
        if value in self.child_states:
            return self.child_states[value]
        elif value in self.re_states:
            return self.re_states[value]
        elif value.startswith('#'):
            self.re_states[value] = State(value, True)
            return self.re_states[value]
        else:
            self.child_states[value] = State(value, False)
            return self.child_states[value]

    def is_empty(self):
        return self.child_states == {}

    def print(self):
        print(self.value, '\t', self.re, '\t', self.child_states)

class StateMachine(object):
    END_PUNC = "$$"
    RE_NUM = 5
    def __init__(self, portray = ''):
        self.init_state = State(portray)
        self.portray = portray

    def build_machine(self, path):
        with open(path, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                self._build_state(line)

    def _build_state(self, line):
        i = 0
        state = self.init_state
        while i < len(line):
            if line[i] == '#':
                temp = line[i:].split('#')[1]
                state = state.add_state('#'+temp+'#')
                i += len(temp) + 2
            else:
                state = state.add_state(line[i])
                i += 1
        state.add_state(self.END_PUNC)

    def extra_pattern(self, line):
        i = 0
        start_idx = i
        state = self.init_state
        stack_states = []
        while i < len(line):
            char = line[i]
            if state.re_states != {}:
                stack_states.append((i, state))
            if line[i] in state.child_states:   # 如果能成功转移，则转移
                state = state.child_states[line[i]]
                i += 1
            elif state.re_states != {}:
                # 取匹配长度最长的一个
                longst = self._extra_re_pattern(i, line, state)
                if longst > 0:
                    return line[start_idx: i + longst]
                else:
                    (t, state) = stack_states.pop()
                    longst = self._extra_re_pattern(t, line, state)
                    if longst > 0:
                        return line[start_idx: t + longst]

                i = start_idx + 1
                start_idx = i
                state = self.init_state
                stack_states.clear()
            elif self.END_PUNC in state.child_states:
                return line[start_idx: i]
            else:
                if stack_states != []:
                    (t, state) = stack_states.pop()
                    longst = self._extra_re_pattern(t, line, state)
                    if longst > 0:
                        return line[start_idx: t + longst]
                i = start_idx + 1
                start_idx = i
                state = self.init_state
                stack_states.clear()

        if self.END_PUNC in state.child_states:
            return line[start_idx: i + 1]
        return None

    def _extra_re_pattern(self, i, line, state):
        longst = 0
        for re_state in state.re_states.values():
            for j in range(re_state.num[0], re_state.num[1] + 1):
                k = self._extra_pattern(line[i + j:], re_state)
                if k is not None and j + k > longst:
                    longst = j + k
        return longst

    def _extra_pattern(self, line, initstate):
        i = 0
        state = initstate
        while i < len(line):
            if line[i] in state.child_states:  # 如果能成功转移，则转移
                state = state.child_states[line[i]]
                i += 1
            else:
                break
        if i > 0 and self.END_PUNC in state.child_states:
            return i
        return None

    def recognition(self, line):
        i = 0
        state = self.init_state
        stack_states = []

        while i < len(line):
            if state.re_states != {}:
                stack_states.append((i, state))
            if line[i] in state.child_states:   # 如果能成功转移，则转移
                state = state.child_states[line[i]]
            elif state.re_states != {}:
                # 考虑模糊转移
                flag = self._recognition_re(i, line, state)
                if flag:
                    return True
                elif stack_states != []:
                    (t, state) = stack_states.pop()
                    flag = self._recognition_re(t, line, state)
                return flag
            else:
                if stack_states != []:
                    (t, state) = stack_states.pop()
                    flag = self._recognition_re(t, line, state)
                    return flag
                return False
            i += 1

        return i == len(line) and self.END_PUNC in state.child_states

    def _recognition_re(self, i, line, state):
        for re_state in state.re_states.values():
            for j in range(re_state.num[0], re_state.num[1] + 1):
                if self._recognition(line[i + j:], re_state):
                    return True
        return False

    def _recognition(self, line, initstate):
        '''给定 state 情况下需要完整转移'''
        i = 0
        state = initstate
        while i < len(line):
            if line[i] in state.child_states:
                state = state.child_states[line[i]]
                i += 1
            else:
                break
        return i == len(line) and self.END_PUNC in state.child_states

if __name__ == '__main__':
    machine = StateMachine('college')
    machine.build_machine('../college_struct.dict')
    if machine.recognition('天津城王府井职业学院'):
        print('OK')
    else:
        print('Fail')

    cont = machine.extra_pattern('我们的天津天王府进商务学院还真没有出过庄园')
    if cont:
        print(cont)
    else:
        print('extra Fail')