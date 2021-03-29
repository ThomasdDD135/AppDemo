from cabinet import Cabinet
from node import Node
import draw
import json


def load_json_data(data_path):
    data = {}
    # 加载文件
    try:
        with open(data_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        error = '未找到指定文件: ' + data_path
        return None, None, None, error
    # 提取数据
    try:
        # 将nodes的所属表箱按概率排序
        for node in data['nodes']:
            node['cabinets'] = sorted(
                node['cabinets'],
                key=lambda cabinet: cabinet['probability'],
                reverse=True)
        # 将表箱的父表箱按概率排序
        for cabinet in data['cabinets']:
            cabinet['parents'] = sorted(
                cabinet['parents'],
                key=lambda parent: parent['probability'],
                reverse=True)
    except KeyError:
        error = 'Json文件中的数据格式错误'
        return None, None, None, error

    return data['nodes'], data['cabinets'], data['cabinetLinks'], None


def create_cabinets(cabinets_data, cabinet_links_data):
    """ 创建表箱列表及表箱ID与对象的映射 """
    # 创建表箱
    cabinets = []
    id_cabinets_map = {}
    for cabinet_data in cabinets_data:
        cabinet = Cabinet(cabinet_data)
        id_cabinets_map[cabinet_data['id']] = cabinet
        cabinets.append(cabinet)
    # 记录表箱间的距离
    for data in cabinet_links_data:
        start_id = data['start']
        end_id = data['end']
        start_cabinet = id_cabinets_map[start_id]
        start_cabinet.cabinet_link_distance[end_id] = data['distance']
    return cabinets, id_cabinets_map


def create_nodes(nodes_data):
    """ 创建开关节点及开关MAC与对象的映射 """
    nodes = []
    mac_nodes_map = {}
    for node_data in nodes_data:
        node = Node(node_data)
        mac_nodes_map[node_data['mac']] = node
        nodes.append(node)
    return nodes, mac_nodes_map


def finde_cabinets_master_node(cabinets_data, id_cabinets_map, mac_nodes_map):
    """ 找到每个表箱的总开关节点 """
    virtual_node_num = 0
    for cabinet_data in cabinets_data:
        parent_data = cabinet_data['parents'][0]
        if parent_data['inNode'] != "":
            # 实体节点
            node_mac = parent_data['inNode']
            node = mac_nodes_map[node_mac]
        else:
            # 虚拟节点
            virtual_mac = 'virtual node ' + str(virtual_node_num)
            virtual_node_num += 1
            node = Node({}, is_virtual=True, virtual_mac=virtual_mac)
            mac_nodes_map[virtual_mac] = node
        cabinet_id = cabinet_data['id']
        cabinet = id_cabinets_map[cabinet_id]
        cabinet.master_node = node
        if node.is_virtual:
            node.belong_to_cabinet = cabinet
        pass


def find_nodes_link_to_cabinet(cabinets_data, id_cabinets_map, mac_nodes_map):
    """ 找到每个开关外连表箱，没有则为None """
    for cabinet_data in cabinets_data:
        parent_data = cabinet_data['parents'][0]
        if parent_data['probability'] != 0:
            node_mac = parent_data['outNode']
            node = mac_nodes_map[node_mac]
            cabinet_id = cabinet_data['id']
            cabinet = id_cabinets_map[cabinet_id]
            node.add_link_to_cabinet(cabinet)
        pass


def add_nodes_to_cabinet(nodes, cabinets):
    """ 将开关节点添加到对应的表箱 """
    for node in nodes:
        if node.is_virtual:
            continue
        cabinet_id = node.belong_to_cabinet_id
        for cabinet in cabinets:
            if cabinet_id == cabinet.id:
                cabinet.add_node(node)
                break
            pass
        pass


def main():
    """ 主函数 """
    # 加载文件
    data_path = input('输入json文件路径: ')
    # 解析Json数据
    nodes_data, cabinets_data, cabinet_links_data, error = load_json_data(
        data_path)
    if (error is not None):
        print(error)
        exit()
    # 创建开关节点列表
    nodes, mac_nodes_map = create_nodes(nodes_data)
    # 创建表箱列表
    cabinets, id_cabinets_map = create_cabinets(cabinets_data,
                                                cabinet_links_data)
    # 找到每个表箱的总开关节点
    finde_cabinets_master_node(cabinets_data, id_cabinets_map, mac_nodes_map)
    # 找到每个开关外连的表箱
    find_nodes_link_to_cabinet(cabinets_data, id_cabinets_map, mac_nodes_map)
    # 将开关节点列表添加到对应的表箱
    add_nodes_to_cabinet(nodes, cabinets)
    # 绘制拓扑结构
    draw.draw_topo(cabinets, nodes)


if __name__ == "__main__":
    main()
