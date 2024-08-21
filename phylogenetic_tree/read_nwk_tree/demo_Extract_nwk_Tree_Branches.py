# pip install ete3

from ete3 import Tree


# 递归函数
def iteration_children(tree_node,start_leaf_name="C",name_results=set()):
    childens_lst = tree_node.get_children()
    for child in childens_lst:
        # 空name 的则是节点，用于判断单节点# 历遍单枝树所有结点 node.traverse()
        children_name_lst = [x.name for x in child.traverse()]
        node_num = children_name_lst.count('')
        if child.is_leaf():
            # node_num == 0  True
            # 独立节点
            print('leaf',child.name)
            continue
        elif node_num > 1:
            #  当前条件下，第二个节点名children_name_lst[1] 就是这个节点分支的第一个叶节点末端, 完全分支无节点名情况则为""
            print("node_num > 1",children_name_lst)
            if start_leaf_name == children_name_lst[1]:
                # 删除空字符
                child_name_lst = [x for x in children_name_lst if x != '']
                name_results.update(child_name_lst)
                return name_results
            else:
                sub_result = iteration_children(child,start_leaf_name,name_results)
                name_results.update(sub_result)
            '''
            node.get_children()
            [Tree node '' (0x2571022105), Tree node 'C' (0x2571022111),, Tree node 'D' (0x2571022112)]

                /-C
             \-|
                \-D
            '''
        else: # node=1 ,也有节点
            # #  当前条件下，第二个节点名children_name_lst[1] 就是这个节点分支的第一个叶节点末端
            print("node_num == 1",children_name_lst)
            if start_leaf_name == children_name_lst[1]:
                # 删除空字符
                child_name_lst = [x for x in children_name_lst if x != '']
                name_results.update(child_name_lst)
                return name_results
            else:
                sub_result = iteration_children(child,start_leaf_name,name_results)
                name_results.update(sub_result)
    return name_results

def demo():
    tree = Tree( '((H:1,(I:1,J:1):0.5):0.5, A:1, (B:1,((C:1,D:1),(E:1,(F:1,G:1):0.5):0.5):0.5):0.5);' )
    print(tree)
    #                  /-H
    #               /-|
    #              |  |   /-I
    #              |   \-|
    #              |      \-J
    #            --|
    #              |--A
    #              |
    #              |   /-B
    #              |  |
    #               \-|      /-C
    #                 |   /-|
    #                 |  |   \-D
    #                  \-|
    #                    |   /-E
    #                     \-|
    #                       |   /-F
    #                        \-|
    #                           \-G
    leaf_name_set = iteration_children(tree,start_leaf_name="C")
    print(leaf_name_set)
    '''
    node_num > 1 ['', 'H', '', 'I', 'J']
    leaf H
    node_num == 1 ['', 'I', 'J']
    leaf A
    node_num > 1 ['', 'B', '', '', '', 'C', 'D', 'E', '', 'F', 'G']
    leaf B
    node_num > 1 ['', '', '', 'C', 'D', 'E', '', 'F', 'G']
    node_num == 1 ['', 'C', 'D']
    node_num > 1 ['', 'E', '', 'F', 'G']
    leaf E
    node_num == 1 ['', 'F', 'G']

    return:
    {'C', 'D'}

    '''


def main():
    # newick文件 路径
    tree_file = 'tree.nwk'
    # 读取newick文件
    tree = Tree(tree_file)
    # 屏幕输出 树的 tree 的字符形式
    print(tree)

    # 指定起始 start_leaf_name
    start_leaf_name = "varius_01299"
    leaf_name_set = iteration_children(tree,start_leaf_name)
    # leaf_name_set = iteration_children(tree,start_leaf_name="C")
    # leaf_name_set = iteration_children(tree,"C")

    with open('leaf_name.lst',mode='wt',encoding='utf-8') as out:
        for leaf_name in sorted(list(leaf_name_set)):
            #print(leaf_name)
            out.write(leaf_name+'\n')

if __name__ == '__main__':
    main()
