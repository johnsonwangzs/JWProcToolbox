# -*- coding: UTF-8 -*-
# @file: typora_table_creator.py
# @author: johnsonwangzs
# @time: 2023/7/18 22:48
# @function: 自动生成Typora中的表格(HTML代码), 可合并单元格.

indents = ' ' * 4  # 缩进空格


def check_units_agg(units_agg, cur_row, cur_col):
    """检查当前位置是否出现在units_agg列表中

    :param list units_agg: 一个列表, 列表中每个元素的格式为 [(r1,c1),(r2,c2)],代表单元格合并后的一个大格的左上和右下小单元格的行号和列号
    :param int cur_row: 当前要检查的行号
    :param int cur_col: 当前要检查的列号
    :return: 若当前位置出现在units_agg列表中, 则返回对应的元素 [(r1,c1),(r2,c2)]. 否则返回None.
    """
    for each in units_agg:
        if each[0][0] == cur_row and each[0][1] == cur_col:
            return each
    return None


def create_table_html(n_row, n_col, align_mode, units_agg) -> str:
    """自动生成Typora中的表格(HTML代码), 可合并单元格.

    :param int n_row: 给定表格总行数
    :param int n_col: 给定表格总列数
    :param int align_mode: 表格内容对齐方式(1-左对齐, 2-中间对齐, 3-右对齐)
    :param list units_agg: 一个列表, 列表中每个元素的格式为 [(r1,c1),(r2,c2)],代表单元格合并后的一个大格的左上和右下小单元格的行号和列号
    :return: 生成的代码

    定义
    ========
    单元格
        一个单元格指表格中最小的格子
    大格
        一个大格指对两个或以上单元格合并后得到的格子

    例子
    ========
    输入为::

        n_row = 4
        n_col = 3
        align_mode = 2
        units_agg = [[(1, 1), (2, 1)], [(1, 2), (1, 3)], [(3, 2), (4, 3)]]

    生成代码为::

        <table style="text-align:center;">
            <tr>
                <td rowspan="2"></td>
                <td colspan="2"></td>
            </tr>
            <tr>
                <td></td>
                <td></td>
            </tr>
            <tr>
                <td></td>
                <td colspan="2" rowspan="2"></td>
            </tr>
            <tr>
                <td></td>
            </tr>
        </table>
    """
    align_dict = {1: 'left', 2: 'center', 3: 'right'}
    codes = '<table style=\"text-align:' + align_dict.get(align_mode) + ';\">' + '\n'
    if len(units_agg) == 0:  # 不存在需要合并单元格的情况
        for row in range(1, n_row + 1):
            codes = codes + indents + '<tr>' + '\n'
            for col in range(1, n_col + 1):
                codes = codes + indents * 2 + '<td></td>' + '\n'
            codes = codes + indents + '</tr>' + '\n'
    else:
        units_all = []  # 标记每个格子是否需要输出
        # 初始化
        for row in range(n_row):
            units_all.append([])
            for col in range(n_col):
                units_all[row].append(1)
        # 逐格生成HTML代码
        for row in range(1, n_row + 1):
            codes = codes + indents + '<tr>' + '\n'
            for col in range(1, n_col + 1):
                if units_all[row - 1][col - 1] == 1:
                    agg = check_units_agg(units_agg, row, col)
                    if agg is not None:  # 大格. [(r1,c1),(r2,c2)]
                        r1, c1, r2, c2 = agg[0][0], agg[0][1], agg[1][0], agg[1][1]
                        # 将大格覆盖的位置置0
                        for i in range(r1 - 1, r2):
                            for j in range(c1 - 1, c2):
                                units_all[i][j] = 0
                        if r1 == r2 and c1 != c2:
                            codes = codes + indents * 2 + f'<td colspan=\"{c2 - c1 + 1}\"></td>' + '\n'
                        elif r1 != r2 and c1 == c2:
                            codes = codes + indents * 2 + f'<td rowspan=\"{r2 - r1 + 1}\"></td>' + '\n'
                        elif r1 != r2 and c1 != c2:
                            codes = codes + indents * 2 + f'<td colspan=\"{c2 - c1 + 1}\" ' \
                                                          f'rowspan=\"{r2 - r1 + 1}\"></td>' + '\n'
                        else:
                            raise f'Bad input!'
                    else:  # 普通单元格
                        codes = codes + indents * 2 + f'<td></td>' + '\n'
            codes = codes + indents + '</tr>' + '\n'
    codes += '</table>'
    return codes


if __name__ == '__main__':
    print('指定表格的基本信息: ')
    n_row = eval(input('> 输入表格的总行数: '))
    n_col = eval(input('> 输入表格的总列数: '))
    align_mode = eval(input('> 输入表格对齐方式(用数字表示: 1-左对齐, 2-中间对齐, 3-右对齐): '))

    if align_mode not in [1, 2, 3]:
        raise f'Bad input!'

    print('接下来, 按照 [(r1,c1),(r2,c2)] 的格式, '
          '依次输入表格中每个大格(指单元格合并后形成的格子)的左上角单元格和右下角单元格的行号和列号, '
          '输入-1作为结束符: ')
    cnt = 0
    units_agg = []
    while True:
        cnt += 1
        unit = eval(input(f'> 指定第{cnt}个大格: '))
        if unit == -1:
            break
        units_agg.append(unit)
    print(f'最终输入:{units_agg}')
    codes = create_table_html(n_row, n_col, align_mode, units_agg)
    print(f'代码生成结果:\n\n{codes}')
    print('\nDone.')
