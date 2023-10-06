import re
from ..services.loggingService import LoggingService
from xml.dom import minidom
import re
from ..models.serverAction import ServerAction
from colorama import Fore, Back, Style, init

class Nfa:
    loggingService = LoggingService()
    transitions = []
    startEvents = []
    states = []
    endConditions = []

    def __init__(self):
        path = 'config/ActionDescriptionLaguage.bpmn'
        with open(path, 'r') as myfile:
            data = myfile.read()
            dom_tree = minidom.parseString(data)
            for sequenceFlow in dom_tree.getElementsByTagName('bpmn:sequenceFlow'):
                source = sequenceFlow.getAttribute('sourceRef')
                tartet = sequenceFlow.getAttribute('targetRef')
                name_list = sequenceFlow.getAttribute('name').split(' ')
                regex = name_list[0]
                stack = ''
                if len(name_list) > 1:
                    stack = name_list[1]
                name = sequenceFlow.getElementsByTagName('bpmn:documentation')
                if len(name) > 0:
                    name = name[0].firstChild.nodeValue
                else:
                    name = ''
                transition = Transition(source, regex, tartet, name, stack)
                self.transitions.append(transition)
            start_events = dom_tree.getElementsByTagName('bpmn:startEvent')
            for start_event in start_events:
                start_event_id = start_event.getAttribute('id')
                self.startEvents.append(start_event_id)
            end_conditions = dom_tree.getElementsByTagName('bpmn:intermediateThrowEvent')
            for end_condition in end_conditions:
                end_condition_child = end_condition.getElementsByTagName('bpmn:escalationEventDefinition')
                if len(end_condition_child) > 0:
                    self.endConditions.append(end_condition.getAttribute('id'))

    def get_server_action_by_action_description_string(self, action_string, data_package_configs, action_configs):
        action_parser = ActionParser(self.transitions, self.startEvents, self.endConditions, data_package_configs, action_configs)
        return action_parser.parse_action_string(action_string)

    def parseActionDescription(self, action_string):
        action_parser = ActionParser(self.transitions, self.startEvents, self.endConditions)
        action_parser.parseActionString(action_string)


class TreeNode:
    def __init__(self):
        self.name = ''
        self.value = ''
        self.condition = ''
        self.target_id = ''
        self.stack = ''
        self.children = []
        self.position = ''
        self.length = ''


class ParsedList:
    def __init__(self):
        self.path_list = []
        self.stack = []
        self.length = 0


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class ActionParser:
    loggingService = LoggingService()

    def __init__(self, transitions, start_conditions, end_conditions, data_package_configs, action_configs):
        self.dataPackageConfigs = data_package_configs
        self.actionConfigs = action_configs
        self.transitions = transitions
        self.startConditions = start_conditions
        self.endConditions = end_conditions

    def parse_action_string(self, action_string):
        if action_string is None:
            self.loggingService.error('action_string is None')
            return None
        flat_action_string = action_string.replace("\r", "").replace("\n", "").replace("\t", "").replace("    ", "")
        if flat_action_string == '':
            return []
        actions = []
        for start_condition in self.startConditions:
            for tree in self.parseActionDescription(start_condition, flat_action_string):
                tree = self.clearTree(tree, 1)
                if not tree:
                    self.loggingService.error('can\'t parse action: ' + action_string)
                    break
                path_list = self.getPrioritizedParsedList(tree)
                self.print_action_string(action_string, path_list.path_list)

                group_list = self.get_group_list(path_list.path_list, 0)
                action = self.create_server_action_by_helping_action(self.get_helping_action_by_group_list(group_list))
                actions.append(action)
        return actions

    def get_group_list(self, value_list, counter):
        group_list = []
        start_with_group_start = False
        if value_list[counter].name == 'actionGroup' and value_list[counter].value == '(':
            counter += 1
            start_with_group_start = True
        while counter < len(value_list):
            group_list.append(value_list[counter])
            if value_list[counter].name == 'actionGroup' and value_list[counter].value == '(':
                next_group_list = self.get_group_list(value_list, counter)
                group_list.append(next_group_list)
                counter += self.count_group_list(next_group_list)
            elif value_list[counter].name == 'actionGroup' and value_list[counter].value == ')':
                if start_with_group_start:
                    return group_list
                else:
                    self.loggingService.log('ActionParseError Klammer zu viel geschlossen')
                    return None
            counter += 1
        if start_with_group_start:
            self.loggingService.log('ActionParseError Klammer nicht geschlossen')
        else:
            return group_list
        return None

    def get_helping_action_by_group_list(self, group_list):
        action = ActionHelpingObject()
        next_action = ActionHelpingObject()
        out_action = ActionHelpingObject()
        state = 'first'
        counter = 0
        while counter < len(group_list):
            if isinstance(group_list[counter], list):
                if state == 'next':
                    action.nextActions.append(self.get_helping_action_by_group_list(group_list[counter]))
                    state = ''
                if state == 'out':
                    action.outputActions.append(self.get_helping_action_by_group_list(group_list[counter]))
                    state = ''
            else:
                if group_list[counter].name == 'outputServerAction' or \
                        group_list[counter].name == 'nextAction':
                    if state == 'next':
                        action.nextActions.append(next_action)
                    if state == 'out':
                        action.outputActions.append(out_action)

                if group_list[counter].name == 'outputServerAction':
                    out_action = ActionHelpingObject()
                    state = 'out'
                if group_list[counter].name == 'nextAction':
                    next_action = ActionHelpingObject()
                    state = 'next'

                if state == 'next':
                    next_action.values.append(group_list[counter])
                if state == 'out':
                    out_action.values.append(group_list[counter])
                if state == 'first':
                    action.values.append(group_list[counter])
            counter += 1
        if state == 'next':
            action.nextActions.append(next_action)
        if state == 'out':
            action.outputActions.append(out_action)
        return action

    def count_group_list(self, _list):
        counter = 0
        for i in _list:
            if isinstance(i, list):
                counter += self.count_group_list(i)
            else:
                counter += 1
        return counter

    def create_server_action_by_helping_action(self, action):
        action_input_descriptions = []
        counter = 0
        server_action = ServerAction()
        for value in action.values:
            if value.name == 'condition':
                server_action.Condition = value.value

            if value.name == 'actionName':
                server_action.Type = value.value
                server_action.Name = value.value

            if value.name == 'actionDescription':
                server_action.Type = value.value
                server_action.Name = value.value
                server_action.IsDescription = True
                return server_action

            input_types = ['complexCode', 'inputBinding', 'inputName', 'inputValue', 'inputValueNew']
            if value.name in input_types:
                # self.loggingService.logObject(value)
                action_input_descriptions.append({'valueName': value.name, 'value': value.value})

            if value.name == 'actionPropertyName':
                setattr(server_action, value.value, action.values[counter + 1].value)
            counter += 1

        for output_action in action.outputActions:
            server_action.OutputServerActions.append(self.create_server_action_by_helping_action(output_action))
        for next_action in action.nextActions:
            server_action.NextActions.append(self.create_server_action_by_helping_action(next_action))

        action_input_descriptions = self.combine_bindings(action_input_descriptions)
        self.set_input_value(server_action, action_input_descriptions)
        self.__setActionExecute__(server_action)
        self.__setActionContext__(server_action)
        return server_action

    def __setActionExecute__(self, action):
        for action_config in self.actionConfigs:
            if action_config.type == action.Type:
                action.Execute = action_config.execute
                action.Opening = action_config.opening

    def __getDataPackageByName__(self, name, data_package_configs):
        data_package = {}
        properties = []
        for data_package_config in data_package_configs:
            if data_package_config.name == name:
                properties = data_package_config.properties

        for _property in properties:
            if _property.find(':') != -1:
                data_package[_property.split(':')[0]] = self.getDataPackageByName(_property.split(':')[1])
            else:
                data_package[_property] = ''
        return data_package

    @staticmethod
    def __setActionContext__(action):
        if action.Execute == 'Client':
            action.Context = ''
        else:
            if action.Context == '':
                action.Context = 'Component'

    def combine_bindings(self, action_input_descriptions):
        new_list = []
        binding_list = []
        for index, value in enumerate(action_input_descriptions):
            if value['valueName'] == 'inputBinding' and value['value'] != '.':
                binding_list.append(value['value'])
                if (len(action_input_descriptions) == index + 1 or action_input_descriptions[index + 1]['value'] != '.'):
                    new_list.append({'valueName': 'inputBinding', 'value': '.'.join(binding_list)})
                    binding_list = []
            if value['valueName'] != 'inputBinding':
                new_list.append(value)
        return new_list


    def set_input_value(self, action, action_input_descriptions):

        list_of_expected_inputs = []
        # set default inputs in action
        for action_config in self.actionConfigs:
            if action.Type == action_config.type:
                list_of_expected_inputs = action_config.input
        for _input in list_of_expected_inputs:
            action.Input[_input] = ''

        # set input_values {type, input, name}
        input_values = []
        counter = 0
        for input_description in action_input_descriptions:
            if input_description['valueName'] == 'komplexCode' or input_description['valueName'] == 'inputValue' or input_description['valueName'] == 'inputBinding' or input_description['valueName'] == 'inputValueNew':
                name = ''
                if action_input_descriptions[counter - 1]['valueName'] == 'inputName':
                    name = action_input_descriptions[counter - 1]['value']
                input_values.append({'type': input_description['valueName'], 'input': input_description['value'], 'name': name})
            counter = counter + 1

        # set all inputs_value names
        counter = 0
        for input_value in input_values:
            if input_value['name'] == '':
                input_value['name'] = list_of_expected_inputs[counter]
            else:
                # **check exaption
                if input_value['name'] not in list_of_expected_inputs:
                    self.loggingService.error(input_value['name'] + ' is no Input of ' + action.Type)
                    return {}
                # check exaption**

            counter = counter + 1

        # set values to action input and input bindings
        for input_value in input_values:
            if input_value['type'] == 'inputBinding':
                action.Bindings.append({'name': input_value['name'], 'binding': input_value['input']})
            if input_value['type'] == 'inputValue':
                action.Input[input_value['name']] = input_value['input'].replace('\'', '')
            if input_value['type'] == 'inputValueNew':
                action.Input[input_value['name']] = self.__getDataPackageByName__(input_value['input'], self.dataPackageConfigs)
            if input_value['type'] == 'complexCode':
                action.KomplexCode.append({'name': input_value['name'], 'code': input_value['input']})

    def print_action_string(self, action_string, path_list):
        color_mapping = {
            'white': Fore.WHITE,
            'actionName': Fore.MAGENTA,
            'inputName': Fore.RED,
            'condition': Fore.GREEN,
            'inputValue': Fore.YELLOW,
            'inputBinding': Fore.YELLOW,
            'actionDescription': Fore.CYAN,
            'complexCode': Fore.LIGHTCYAN_EX,
            'inputValueNew': Fore.LIGHTCYAN_EX
        }

        output_string = ''
        path_list_counter = 0
        path_list_value_counter = 0
        for letter in action_string:
            value = path_list[path_list_counter]
            if len(value.value) == path_list_value_counter:
                path_list_value_counter = 0
                path_list_counter += 1
                if path_list_counter == len(path_list):
                    break
                value = path_list[path_list_counter]
            if value.value[path_list_value_counter] == letter:
                if path_list_value_counter == 0:
                    if value.name in color_mapping.keys():
                        output_string += color_mapping[value.name]
                    else:
                        output_string += color_mapping['white']

                path_list_value_counter += 1
            output_string += letter
        print('    ' + output_string+color_mapping['white'])

    def getPrioritizedParsedList(self, tree) -> ParsedList:
        pathes = self.getAllPathesAsList(tree)
        parsed_lists = []
        for path_list in pathes:
            parsed_list = self.getParsedListByTreeList(path_list)
            if parsed_list:
                parsed_lists.append(parsed_list)

        parsed_lists = sorted(parsed_lists, key=lambda k: k.length, reverse=True)
        longest_parsed_lists = []
        if len(parsed_lists) == 0:
            return None

        longest_length = parsed_lists[0].length
        for path_list in parsed_lists:
            if path_list.length == longest_length:
                longest_parsed_lists.append(path_list)
            else:
                break
        parsed_lists = longest_parsed_lists
        pathes_without_stack = [x for x in parsed_lists if len(x.stack) == 0]
        if len(pathes_without_stack) > 0:
            return pathes_without_stack[0]

        return parsed_lists[0]

    def parseActionDescription(self, start_condition, line):
        tree_nodes = []
        transitions = self.getTransitionByCondition(start_condition)
        for transition in transitions:
            p = re.compile(transition.regEx)
            matches = [x for x in p.finditer(line) if x.start() == 0]
            for match in matches:
                tree_node = TreeNode()
                tree_node.name = transition.name
                tree_node.value = match.group()
                tree_node.stack = transition.stack
                tree_node.target_id = transition.targetKnote
                tree_node.children = self.parseActionDescription(tree_node.target_id, line[match.end():])
                tree_nodes.append(tree_node)

        return tree_nodes

    def clearTree(self, tree, position):
        tree.position = position
        tree.length = 0
        remaining_children = []
        for child in tree.children:
            child = self.clearTree(child, position + 1)
            if child:
                length = child.length + 1
                if length > tree.length:
                    tree.length = length
                remaining_children.append(child)
        if len(remaining_children) > 0:
            # longest_children = [sorted(remaining_children, key=lambda k: k.length, reverse=True)[0]]
            tree.children = remaining_children
            return tree
        elif tree.target_id in self.endConditions:
            return tree
        else:
            return None

    def getAllPathesAsList(self, tree):
        pathes_list = []
        if len(tree.children) == 0:
            return [[tree]]
        for child in tree.children:
            for child_list in self.getAllPathesAsList(child):
                pathes_list.append([tree] + child_list)
        return pathes_list

    @staticmethod
    def getParsedListByTreeList(tree_list) -> ParsedList:
        stack = []
        for tree in tree_list:
            if len([x for x in stack if x['name'] == tree.name and x['name'] != '']) == 0:
                stack.append({'name': tree.name, 'count': 0})
            node = [x for x in stack if x['name'] == tree.name][0]
            if tree.stack == '+':
                node['count'] += 1
            if tree.stack == '-':
                node['count'] -= 1
            if node['count'] < 0:
                # self.loggingService.error('Action Parse Error: to stack -1 ' + tree.name)
                return None
        parsed_list = ParsedList()
        parsed_list.path_list = [x for x in tree_list if len(x.value) > 0]
        parsed_list.length = len(tree_list)
        parsed_list.stack = [x for x in stack if x['count'] > 0]
        return parsed_list

    def checkStack(self, tree):
        stack = self.initStack(tree, [])
        if stack is None:
            return False
        positiv_stack = [x for x in stack if x['count'] > 0]
        for x in positiv_stack:
            self.loggingService.error('Action Parse Error: stack positiv ' + x['name'])
        if len(positiv_stack):
            return False
        return True

    def initStack(self, tree, stack):
        if len([x for x in stack if x['name'] == tree.name and x['name'] != '']) == 0:
            stack.append({'name': tree.name, 'count': 0})
        node = [x for x in stack if x['name'] == tree.name][0]
        if tree.stack == '+':
            node['count'] += 1
        if tree.stack == '-':
            node['count'] -= 1
        if node['count'] < 0:
            self.loggingService.error('Action Parse Error: to stack -1 ' + tree.name)
            return None

        if len(tree.children) > 0:
            stack = self.initStack(tree.children[0], stack)
        return stack

    def getTransitionByCondition(self, condition):
        return [x for x in self.transitions if x.firstKnote == condition]

    def getServerActionByTree(self, server_action, tree):
        if tree.name == 'actionName':
            server_action.Name = tree.value

        return server_action

    def printTree(self, tree, deep):
        counter = 0
        string = ''
        while counter < deep:
            string += ' '
            counter += 1
        print(string + tree.value + ' ' + tree.name + ' ' + str(len(tree.children)) + ' ' + str(tree.position) + ' ' + str(tree.length))
        for x in tree.children:
            self.printTree(x, deep + 1)


class Transition:
    def __init__(self, first, reg_ex, target, name, stack):
        self.firstKnote = first
        self.regEx = reg_ex
        self.targetKnote = target
        self.name = name
        self.stack = stack


class ActionHelpingObject:
    def __init__(self):
        self.values = []
        self.nextActions = []
        self.outputActions = []
