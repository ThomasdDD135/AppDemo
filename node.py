class Node(object):
    """
    开关节点
    """
    def __init__(self, node_data, is_virtual=False, virtual_mac=None):
        """ 初始化 """
        self._is_virtual = is_virtual
        if is_virtual:
            self.__crate_virtual_node(virtual_mac)
            return
        # 开关的MAC地址
        self._mac = node_data['mac']
        # 开关的ID
        self._id = node_data['id']
        # 开关IP地址
        self._ip = node_data['ip']
        # 开关所属表箱的ID
        self._belong_to_cabinet_id = self.__get_belong_to_cabinet_id(
            node_data['cabinets'])
        # 开关所属表箱
        self._belong_to_cabinet = None
        # 开关外连表箱
        self._link_to_cabinets = []
        # 连接的下级开关
        self._linked_next_nodes = []
        # 开关的父开关
        self._parent_node = None
        # 开关的其他属性
        self._tei = node_data['tei']
        self.__set_role(node_data['role'])
        self.__set_phase(node_data['phase'])
        self._is_phase_order_correct = node_data['isPhaseOrderCorrect']
        self._device_type = node_data['deviceType']
        self._location = self.__parse_location(node_data['location'])

    def __crate_virtual_node(self, virtual_mac):
        """ 创建虚拟节点 """
        if virtual_mac is None:
            print('virtual_node\'s virtual_mac is None.')
            return
        self._mac = virtual_mac
        # 开关所属表箱
        self._belong_to_cabinet = None
        # 开关外连表箱
        self._link_to_cabinets = []
        # 连接的下级开关
        self._linked_next_nodes = []
        # 开关的父开关
        self._parent_node = None
        pass

    @property
    def belong_to_cabinet(self):
        return self._belong_to_cabinet

    @belong_to_cabinet.setter
    def belong_to_cabinet(self, cabinet):
        self._belong_to_cabinet = cabinet
        self._belong_to_cabinet_id = cabinet.id

    @property
    def belong_to_cabinet_id(self):
        return self._belong_to_cabinet_id

    @property
    def device_type(self):
        return self._device_type

    @property
    def id(self):
        return self._id

    @property
    def ip(self):
        return self._ip

    @property
    def is_phase_order_correct(self):
        return self._is_phase_order_correct

    @property
    def is_virtual(self):
        return self._is_virtual

    @property
    def link_to_cabinets(self):
        return self._link_to_cabinets

    @property
    def linked_next_nodes(self):
        return self._linked_next_nodes

    @property
    def location(self):
        return self._location

    @property
    def mac(self):
        return self._mac

    @property
    def parent_node(self):
        return self._parent_node

    @parent_node.setter
    def parent_node(self, parent_node):
        self._parent_node = parent_node

    @property
    def phase(self):
        return self._phase

    @property
    def role(self):
        return self._role

    @property
    def tei(self):
        return self._tei

    @property
    def info(self):
        """ 开关的详细信息 """
        if self.is_virtual:
            return self.mac
        node_info = ''
        node_info += 'mac: ' + str(self.mac) + '\n'
        node_info += 'id: ' + str(self.id) + '\n'
        node_info += 'ip: ' + str(self.ip) + '\n'
        node_info += 'tei: ' + str(self.tei) + '\n'
        node_info += 'role: ' + str(self.role) + '\n'
        node_info += 'phase: ' + str(self.phase) + '\n'
        node_info += 'isPhaseOrderCorrect: ' + str(
            self.is_phase_order_correct) + '\n'
        node_info += 'deviceType: ' + str(self.device_type) + '\n'
        node_info += 'level: ' + str(self.belong_to_cabinet.level) + '\n'
        node_info += 'location: ' + str(self._location)
        return node_info

    def add_link_to_cabinet(self, cabinet):
        if cabinet not in self._link_to_cabinets:
            self._link_to_cabinets.append(cabinet)
            if cabinet.master_node is not None:
                self.add_linked_next_node(cabinet.master_node)

    def add_linked_next_node(self, node):
        if node not in self._linked_next_nodes:
            self._linked_next_nodes.append(node)
            node.parent_node = self

    def __get_belong_to_cabinet_id(self, cabinets):
        """ 获取节点所在表箱ID """
        cabinet_id = ''
        probability = 0
        for cabinet in cabinets:
            if cabinet['probability'] > probability:
                probability = cabinet['probability']
                cabinet_id = cabinet['id']
        if cabinet_id == "":
            cabinet_id = None
        return cabinet_id

    def __set_role(self, role):
        """ role转义 """
        role_dic = {1: 'CCO', 2: 'STA Proxy', 3: 'STA'}
        try:
            self._role = role_dic[role]
        except KeyError:
            self._role = 'unknown'

    def __set_phase(self, phase):
        """ phase转义 """
        phase_dic = {
            1: 'not started',
            2: 'not supported',
            3: 'identifying',
            4: 'A/B/C',
            5: 'A',
            6: 'B',
            7: 'C',
            8: 'invalid'
        }
        try:
            self._phase = phase_dic[phase]
        except KeyError:
            self._phase = 'unknown'

    def __parse_location(self, location_data):
        """ 解析location，将二进制数组转换为中文，编码为gb2312 """
        byte_datas = []
        for byte in location_data:
            if byte > 0:
                byte_datas.append(byte)
            else:
                break
        res = bytes(byte_datas)
        return res.decode('gb2312')
