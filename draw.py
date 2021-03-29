import matplotlib.pyplot as plt
from pylab import mpl

# 参数配置
# 开关节点字体设置
NODE_FONT_SIZE = 9
NODE_FONT_WEIGHT = 'normal'
# 开关节点绘制设置
NODE_R = 1
NODE_COLOR = '#3398de'
# 开关之间的间隔
NODES_X_INTERVAL = 3
NODES_Y_INTERVAL = 6
# 表箱之间的间隔
CABINETS_X_INTERVAL = 1
CABINETS_Y_INTERVAL = 12
# 线段绘制设置
LINE_IN_CABINET_WIDTH = 0.5
LINE_OUT_CABINET_WIDTH = 0.5
# 超过放大倍率后，显示MAC信息
ZOOM_RATE = 4


def plot_init():
    """ 配置plot """
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    axprops = dict(xticks=[], yticks=[])
    fig = plt.figure(1, figsize=(16, 9), dpi=100, facecolor='white')
    draw_topo.ax = plt.subplot(111, frameon=False, **axprops)
    plt.axis('equal')
    fig.tight_layout()
    pass


def find_topo_root(cabinets):
    """ 找到拓扑结构的根节点所在表箱 """
    root = None
    for cabinet in cabinets:
        if cabinet.parent_cabinet is None:
            root = cabinet
            return root
    return root


def get_axes_size(ax):
    """ 获取画布大小 """
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    width = xlim[1] - xlim[0]
    height = ylim[1] - ylim[0]
    area = width * height
    return width, height, area


def get_cabinet_max_level(root):
    """ 获取表箱的最深层数 """
    deep = 0
    for cabinet in root.linked_next_cabinets:
        deep = max(deep, get_cabinet_max_level(cabinet))
    return deep + 1


def get_cabinet_max_width(cabinets):
    """ 获取表箱的最大宽度 """
    max_width = NODES_X_INTERVAL * 2 + 2 * NODE_R
    for cabinet in cabinets:
        n = len(cabinet.contain_nodes)
        max_width = max(max_width, 2 * (n - 1) * NODE_R + n * NODES_X_INTERVAL)
    return max_width


def get_cabinet_width_height(cabinet):
    """ 计算表箱的宽度和高度 """
    width = NODES_X_INTERVAL * 2 + 2 * NODE_R
    n = len(cabinet.contain_nodes)
    width = max(width, 2 * (n - 1) * NODE_R + n * NODES_X_INTERVAL)
    height = 2 * NODE_R + 2 * NODES_Y_INTERVAL
    if n > 1:
        height = 4 * NODE_R + 3 * NODES_Y_INTERVAL
    return width, height


def get_max_width_in_tree(root):
    """ 获取树中最大宽度 """
    width = 0
    if len(root.linked_next_cabinets) == 0:
        return 1
    for cabinet in root.linked_next_cabinets:
        width += get_max_width_in_tree(cabinet)
    return width


def is_point_visible_in_axes(ax, point):
    """ 判断点是否在当前画布中可见 """
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    if point[0] >= xlim[0] and point[0] <= xlim[1]:
        if point[1] >= ylim[0] and point[1] <= ylim[1]:
            return True
    return False


def ax_update(ax):
    """ 缩放监听 """
    origin_ax_area = draw_topo.ax_area
    _, _, cur_ax_area = get_axes_size(ax)
    # 当放大倍率较小时不显示MAC信息
    if origin_ax_area / cur_ax_area < ZOOM_RATE:
        visible_changed = False
        for ann in draw_topo.node_mac_anns:
            if ann.get_visible() is True:
                ann.set_visible(False)
                visible_changed = True
        if visible_changed:
            plt.draw()
        return
    # 当放大倍率较小时显示当前窗口中的MAC信息
    visible_changed = False
    for ann in draw_topo.node_mac_anns:
        should_be_visible = (is_point_visible_in_axes(ax, ann.xy) is True)
        if should_be_visible is not ann.get_visible():
            ann.set_visible(should_be_visible)
            visible_changed = True
    if visible_changed:
        plt.draw()
    pass


def on_move(event):
    """ 鼠标移动事件触发函数 """
    visible_changed = False
    for cir in draw_topo.nodes_circle.values():
        should_be_visible = (cir.contains(event)[0] is True)
        try:
            node_info = draw_topo.circle_node_info_anns[cir]
        except KeyError:
            print(cir)
            continue
        if should_be_visible != node_info.get_visible():
            visible_changed = True
            node_info.set_visible(should_be_visible)
    if visible_changed:
        plt.draw()
    pass


def on_scroll(event):
    """ 鼠标滚轮事件触发函数 """
    ax = event.inaxes
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()
    zoom_width = (x_max - x_min) / 10
    zoom_height = (y_max - y_min) / 10
    if event.button == 'up':
        # 放大画布
        ax.set_xlim((x_min + zoom_width, x_max - zoom_width))
        ax.set_ylim((y_min + zoom_height, y_max - zoom_height))
    elif event.button == 'down':
        # 缩小画布
        ax.set_xlim((x_min - zoom_width, x_max + zoom_width))
        ax.set_ylim((y_min - zoom_height, y_max + zoom_height))
    plt.draw()
    pass


def plot_cabinet(cabinet, center_x, center_y, width, height):
    """ 使用matplotlib库绘制表箱 """
    lfx = center_x - width / 2
    lfy = center_y - height / 2
    # 绘制表箱位置
    rect = plt.Rectangle((lfx, lfy),
                         width,
                         height,
                         color='b',
                         fill=False,
                         alpha=0.5,
                         linestyle='--')
    draw_topo.ax.add_patch(rect)
    # 标注表箱编号
    cabinet_info = cabinet.id
    plt.text(lfx,
             lfy + height,
             cabinet_info,
             color='r',
             ha='left',
             va='top',
             fontsize=9)
    pass


def plot_line(st_xy, ed_xy, line_width):
    """ 使用matplotlib绘制线段 """
    x = [st_xy[0], ed_xy[0]]
    y = [st_xy[1], ed_xy[1]]
    plt.plot(x, y, color='b', linewidth=line_width)
    pass


def plot_nodes_info(nodes):
    """ 绘制开关详细信息 """
    nodes_posion = draw_topo.nodes_posion
    nodes_circle = draw_topo.nodes_circle
    for node in nodes:
        (x, y) = nodes_posion[node.mac]
        cir = nodes_circle[node.mac]
        annotate = plt.annotate(node.info,
                                xy=(x, y),
                                xycoords=cir,
                                xytext=(x + NODE_R, y),
                                textcoords='data',
                                va='top',
                                ha='left',
                                bbox=dict(boxstyle="round", fc="1"))
        annotate.set_visible(False)
        draw_topo.circle_node_info_anns[cir] = annotate
    pass


def plot_node(node, x, y, r):
    """ 使用matplotlib绘制开关节点 """
    if node.is_virtual:
        # 虚拟节点不进行绘制
        return
    cir = plt.Circle((x, y), 1, color=NODE_COLOR, fill=True)
    draw_topo.ax.add_patch(cir)
    # 开关的mac信息
    ann = plt.annotate(node.mac, (x, y),
                       xycoords=cir,
                       xytext=(x, y - NODE_R),
                       textcoords='data',
                       va='top',
                       ha='center',
                       fontsize=NODE_FONT_SIZE,
                       fontweight=NODE_FONT_WEIGHT)
    ann.set_visible(False)
    draw_topo.node_mac_anns.append(ann)
    draw_topo.nodes_circle[node.mac] = cir
    pass


def draw_nodes(cabinet, center_x, center_y, width, height):
    """ 绘制表箱内节点的逻辑 """
    # 绘制表箱内的总开关
    master_node = cabinet.master_node
    x = center_x
    y = center_y + height / 2 - NODES_Y_INTERVAL - NODE_R
    draw_topo.nodes_posion[master_node.mac] = (x, y)
    plot_node(master_node, x, y, NODE_R)
    if len(cabinet.contain_nodes) > 1:
        if master_node.is_virtual:
            plot_line((x, y + NODE_R), (x, y - NODE_R - NODES_Y_INTERVAL / 2),
                      LINE_IN_CABINET_WIDTH)
        else:
            plot_line((x, y - NODE_R), (x, y - NODE_R - NODES_Y_INTERVAL / 2),
                      LINE_IN_CABINET_WIDTH)
    # 绘制表箱内的其他开关
    y = y - 2 * NODE_R - NODES_Y_INTERVAL
    x = center_x - width / 2 - NODE_R
    for node in cabinet.contain_nodes:
        if node is cabinet.master_node:
            continue
        x += 2 * NODE_R + NODES_X_INTERVAL
        draw_topo.nodes_posion[node.mac] = (x, y)
        plot_node(node, x, y, NODE_R)
        # 绘制表箱内开关间的连线
        plot_line((x, y + NODE_R), (x, y + NODE_R + NODES_Y_INTERVAL / 2),
                  LINE_IN_CABINET_WIDTH)
        positon = draw_topo.nodes_posion[master_node.mac]
        plot_line((x, y + NODE_R + NODES_Y_INTERVAL / 2),
                  (positon[0], y + NODE_R + NODES_Y_INTERVAL / 2),
                  LINE_IN_CABINET_WIDTH)
    pass


def draw_cabinet(cabinet, min_x, max_x, min_y, max_y):
    """ 绘制表箱的逻辑 """
    # 计算表箱的宽度和高度
    width, height = get_cabinet_width_height(cabinet)
    center_x = (max_x + min_x) / 2
    center_y = (max_y + min_y) / 2
    plot_cabinet(cabinet, center_x, center_y, width, height)
    draw_nodes(cabinet, center_x, center_y, width, height)
    # 绘制连接的下一层表箱
    max_width = draw_topo.cabinet_max_width
    max_height = draw_topo.cabinet_max_height
    ty = min_y - CABINETS_Y_INTERVAL
    by = ty - max_height
    rx = min_x - CABINETS_X_INTERVAL
    for next_cabinet in cabinet.linked_next_cabinets:
        lx = rx + CABINETS_X_INTERVAL
        w_nums = get_max_width_in_tree(next_cabinet)
        rx = lx + w_nums * max_width + (w_nums - 1) * CABINETS_X_INTERVAL
        draw_cabinet(next_cabinet, lx, rx, by, ty)
    # 绘制表箱之间的连线
    dealt = 0
    flg = -1
    for node in cabinet.contain_nodes:
        for next_node in node.linked_next_nodes:
            # 连接点是否连向表箱外
            if next_node.belong_to_cabinet_id == cabinet.id:
                continue
            cabinet_distance = cabinet.cabinet_link_distance[
                next_node.belong_to_cabinet_id]
            # print(next_node.belong_to_cabinet_id, cabinet_distance)
            node_posion = draw_topo.nodes_posion[node.mac]
            try:
                next_noed_posion = draw_topo.nodes_posion[next_node.mac]
            except KeyError:
                print(next_node.mac)
                continue
            x, y = node_posion
            nx, ny = next_noed_posion
            # 如果总开关连接下一个表箱，更改出线位置
            if node.mac == cabinet.master_node.mac:
                cy = y
                if nx < x:
                    x -= NODE_R
                if nx > x:
                    x -= NODE_R
                if nx == x:
                    cy -= NODE_R
            else:
                cy = y - NODE_R - NODES_Y_INTERVAL - \
                    CABINETS_Y_INTERVAL / 2 + dealt * flg
                # 变换连线中间线的高度，使其不会共线
                if flg < 0:
                    dealt += 1
                flg = -flg
                # 子开关先向下出线
                plot_line((x, y - NODE_R), (x, cy), LINE_OUT_CABINET_WIDTH)
            plot_line((nx, ny + NODE_R), (nx, cy), LINE_OUT_CABINET_WIDTH)
            plot_line((x, cy), (nx, cy), LINE_OUT_CABINET_WIDTH)
            # 绘制表箱之间的距离
            if cabinet_distance > 0:
                plt.text((x + nx) / 2,
                         cy,
                         str(cabinet_distance) + 'm',
                         ha='center',
                         va='bottom')
    pass


def draw_topo(cabinets, nodes):
    """ 绘制拓扑结构 """
    # plot初始化
    plot_init()
    # 获取最上层表箱
    root_cabinet = find_topo_root(cabinets)
    # 各个节点绘制的位置
    draw_topo.nodes_posion = {}
    # 表示各个开关的圆
    draw_topo.nodes_circle = {}
    # 各个节点对应的详细信息de注释
    draw_topo.circle_node_info_anns = {}
    # 各个节点的MAC信息
    draw_topo.node_mac_anns = []
    # 获取表箱的最大宽度和高度
    width = draw_topo.cabinet_max_width = get_cabinet_max_width(cabinets)
    height = draw_topo.cabinet_max_height = 4 * NODE_R + \
        3 * NODES_Y_INTERVAL
    # 获取拓扑结构树的最大宽度和高度
    w_nums = get_max_width_in_tree(root_cabinet)
    h_nums = get_cabinet_max_level(root_cabinet)
    # 设置画布的宽和高
    ax_width = w_nums * width + (w_nums + 1) * CABINETS_X_INTERVAL
    ax_height = h_nums * height + (h_nums + 1) * CABINETS_Y_INTERVAL
    plt.xlim(0, ax_width)
    plt.ylim(0, ax_height)
    # 绘制表箱
    min_x = 0 + CABINETS_X_INTERVAL
    max_x = ax_width - CABINETS_X_INTERVAL
    max_y = ax_height - CABINETS_Y_INTERVAL
    min_y = max_y - height
    draw_cabinet(root_cabinet, min_x, max_x, min_y, max_y)
    # 绘制开关节点详细信息
    plot_nodes_info(nodes)
    # 记录原始画布大小
    _, _, draw_topo.ax_area = get_axes_size(draw_topo.ax)
    # 添加鼠标监听
    plt.connect('motion_notify_event', on_move)
    plt.connect('scroll_event', on_scroll)
    # 添加缩放监听
    draw_topo.ax.callbacks.connect('xlim_changed', ax_update)
    draw_topo.ax.callbacks.connect('ylim_changed', ax_update)
    # 保存图片
    # plt.savefig('./test.jpg')
    plt.show()
    pass
