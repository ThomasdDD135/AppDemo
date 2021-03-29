class Cabinet(object):
    """
    表箱
    """
    def __init__(self, cabinet_data):
        """ 初始化 """
        # 表箱ID
        self._id = cabinet_data['id']
        # 父表箱ID
        self._parent_id = self.__get_parent_cabinet(cabinet_data['parents'])
        # 父表箱
        self._parent_cabinet = None
        # 表箱所在层数
        self._level = cabinet_data['level']
        # 总开关节点
        self._master_node = None
        # 表箱内开关节点
        self._contain_nodes = []
        # 表箱连接的下一层表箱
        self._linked_next_cabinets = []
        # 表箱连接的距离
        self._cabinet_link_distance = {}

    @property
    def cabinet_link_distance(self):
        return self._cabinet_link_distance

    @property
    def contain_nodes(self):
        return self._contain_nodes

    @property
    def id(self):
        return self._id

    @property
    def level(self):
        return self._level

    @property
    def linked_next_cabinets(self):
        return self._linked_next_cabinets

    @property
    def master_node(self):
        return self._master_node

    @master_node.setter
    def master_node(self, master_node):
        self._master_node = master_node
        self.add_node(master_node)

    @property
    def parent_cabinet(self):
        return self._parent_cabinet

    @parent_cabinet.setter
    def parent_cabinet(self, cabinet):
        self._parent_cabinet = cabinet

    @property
    def parent_id(self):
        return self._parent_id

    def add_linked_next_cabinet(self, cabinet):
        if cabinet not in self._linked_next_cabinets:
            self._linked_next_cabinets.append(cabinet)

    def add_node(self, node):
        """ 添加开关节点 """
        if node not in self._contain_nodes:
            self._contain_nodes.append(node)
            node.belong_to_cabinet = self
        for next_cabinet in node.link_to_cabinets:
            self.add_linked_next_cabinet(next_cabinet)

    def __get_parent_cabinet(self, parents):
        """ 获取表箱的父表箱ID """
        probability = 0
        parent_id = ''
        parent = parents[0]
        probability = parent['probability']
        parent_id = parent['id']
        if parent_id == "" or probability == 0:
            parent_id = None
        return parent_id
