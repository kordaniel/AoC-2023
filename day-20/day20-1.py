import sys
sys.path.insert(0, '..')

import math
from typing import Dict, List, Tuple

from helpers import filemap


use_test_data = False
inp = filemap('input.txt') if not use_test_data else [
    [
        'broadcaster -> a, b, c',
        '%a -> b',
        '%b -> c',
        '%c -> inv',
        '&inv -> a'
    ], # 32000000
    [
        'broadcaster -> a',
        '%a -> inv, con',
        '&inv -> b',
        '%b -> con',
        '&con -> output'
    ] # 11687500
][1]


class Module:
    '''
    Baseclass for the different modules.
    '''

    def __init__(self, name: str, outputs: List[str]):
        self.__outputs = outputs
        self.__name = name

    @property
    def outputs(self) -> List[str]:
        return self.__outputs

    @property
    def name(self) -> str:
        return self.__name

    @property
    def state(self) -> bool:
        raise NotImplementedError('Baseclass has no state')

    def handle_pulse(self, _source: str, _pulse: bool) -> None:
        raise NotImplementedError('Baseclass does not implement the handle_pulse method')

    def add_input(self, _: str) -> None:
        pass # Relevant subclasses implmeent this method

    def add_output(self, destination: str) -> None:
        self.__outputs.append(destination)

    def remove_output(self, destination: str) -> None:
        while destination in self.__outputs:
            self.__outputs.remove(destination)

    def __str__(self) -> str:
        return f'{self.__name} -> [{",".join(self.__outputs)}]'


class Broadcaster(Module):

    def __init__(self, name: str, outputs: List[str] = []):
        super().__init__(name, outputs)
        self.__state = False

    def handle_pulse(self, _source: str, pulse: bool) -> Tuple[str, bool, List[str]]:
        self.__state = pulse
        return super().name, self.state, super().outputs

    @property
    def state(self) -> bool:
        return self.__state


class FlipFlop(Module):

    def __init__(self, name: str, outputs: List[str] = []):
        super().__init__(name, outputs)
        self.__state = False

    def handle_pulse(self, _source: str, pulse: bool) -> Tuple[str, bool, List[str]]:
        if pulse:
            return super().name, self.state, []

        self.__state = not self.__state
        return super().name, self.state, super().outputs

    @property
    def state(self) -> bool:
        return self.__state


class Conjunction(Module):

    def __init__(self, name: str, outputs: List[str] = []):
        super().__init__(name, outputs)
        self.__inputs: Dict[str, bool] = dict()

    def add_input(self, source: str) -> None:
        if not source in self.__inputs:
            self.__inputs[source] = False

    def handle_pulse(self, source: str, pulse: bool) -> Tuple[str, bool, List[str]]:
        self.__inputs[source] = pulse
        return super().name, self.state, super().outputs

    @property
    def state(self) -> bool:
        return not all(self.__inputs.values())

    def __str__(self) -> str:
        return f'[{",".join(self.__inputs)}] -> {super().__str__()}'


class Output(Module):

    def __init__(self, name: str, outputs: List[str] = []):
        super().__init__(name, outputs)

    def handle_pulse(self, _source: str, _pulse: bool) -> Tuple[str, bool, List[str]]:
        return super().name, self.state, super().outputs

    @property
    def state(self) -> bool:
        return False


def parse_input(inp: List[str]) -> Dict[str, Module]:
    modules = {}

    for line in inp:
        name, destinations = line.strip().split(' -> ')
        if name.startswith('broadcaster'):
            modules[name] = Broadcaster(name, destinations.split(', '))
        elif name[0] == '%':
            modules[name[1:]] = FlipFlop(name[1:], destinations.split(', '))
        elif name[0] == '&':
            modules[name[1:]] = Conjunction(name[1:], destinations.split(', '))
        else:
            assert False

    modules['output'] = Output('output')

    for module in modules.values():
        for output in module.outputs:
            if output in modules:
                modules[output].add_input(module.name)

    return modules


def run(modules: Dict[str, Module]) -> List[int]:
    pulses = [1, 0] # low, high counts. Initially low == 1 (button => broadcaster)
    stack_pulses_inturn = [(0, 'button', False, ['broadcaster'])]
    stack_pulses_emitted = []

    i = 0

    while True:
        i += 1

        if len(stack_pulses_inturn) == 0:
            if len(stack_pulses_emitted) == 0:
                break

            cur_i = stack_pulses_emitted[-1][0]
            while len(stack_pulses_emitted) > 0 and stack_pulses_emitted[-1][0] == cur_i:
                stack_pulses_inturn.append(stack_pulses_emitted.pop())

        _, source, pulse, destinations = stack_pulses_inturn.pop()

        for next_dest in destinations:
            if not next_dest in modules:
                # If a pulse has been emitted to a nonexisting
                # module => ignore, but count the pulse
                continue

            next_source, next_pulse, next_dests = modules[next_dest].handle_pulse(source, pulse)
            stack_pulses_emitted.append((i, next_source, next_pulse, next_dests))
            pulses[1 if next_pulse else 0] += len(next_dests)

    return pulses


modules = parse_input(inp)
total_pulses = [0, 0]
for _ in range(1000):
    low_pulses, high_pulses = run(modules)
    total_pulses[0] += low_pulses
    total_pulses[1] += high_pulses

print('Part 1:', total_pulses, '=>', math.prod(total_pulses))
