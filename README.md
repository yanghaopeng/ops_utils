####记录python工具包

CLASSES
    builtins.object
        Oracle_util

    class Oracle_util(builtins.object)
     |  Methods defined here:
     |
     |  __del__(self)
     |      # 销毁
     |
     |  __init__(self, db_info={'user': 'xxx', 'pwd': 'xxx', 'dsn': 'xxx'}, arraysize=500)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  callfunc(self, func, ret_type=<class 'cx_Oracle.NUMBER'>, args=())
     |      # 调用函数 函数名，返回类型, 参数('1',2)元祖类型
     |
     |  callproc(self, proc, in_val=())
     |      # 调用过程 过程名，输入参数('1',2)元祖类型
     |
     |  close(self)
     |      # 关闭连接
     |
     |  commit(self)
     |      # 提交
     |
     |  create_params(self, table, args={})
     |      # 根据表自动创建参数字典
     |
     |  deleteByTable(self, table, cond_dict={})
     |      # 删除，参数一：表名，#参数二：用于where条件，如 where 字段3=值3 and 字段4=值4，格式{'字段3':'值3','字段4':'值4'}
     |
     |  execute(self, sql, args={})
     |      # 执行sql
     |
     |  executemany(self, sql, args)
     |      # 批量执行
     |
     |  exportTxt(self, file_name, sql, args={}, col_split='|', col_flg=True)
     |      :param file_name: 文件位置
     |      :param sql:  sql语句 如select module_name,china_name from python_modules where module_name=:module_name
     |      :param args:  参数 如{'module_name':'oracle'}
     |      :param col_split: 列分隔符
     |      :param col_flg: 是否输出列名字段col1|col2
     |      :return:
     |
     |  get_columns(self, table)
     |
     |  get_rows(self, size=None, is_dict=True)
     |      # 提取数据，参数一提取的记录数，参数二，是否以字典方式提取。为true时返回：{'字段1':'值1','字段2':'值2'}
     |
     |  insertMany(self, table, columns=[], values=[])
     |      # 批量插入数据库，参数一：表名，参数二：['字段1','字段2',...],参数二：[('值1','值2',...),('值1','值2',...)]
     |
     |  insertOne(self, table, column_dict)
     |      # oracle的参数名必须使用:代替，如 userid = :userid
     |
     |  nextval(self, seq)
     |      # 获取序列的下一个值，传入sequence的名称
     |
     |  parse(self, sql, args={})
     |      # 解析sql
     |
     |  queryBySql(self, sql, args={})
     |
     |  queryByTable(self, table, column='*', cond_dict={})
     |      # 执行sql，参数一：table，参数二：查询列'col1,col2' 参数三：参数字典{'字段1'：'值1','字段2':'值2'}
     |
     |  query_pages(self, sql, args={}, page=1, page_size=30)
     |      # 分页查询，参数一：sql语句，参数二：参数字典{'字段1'：'值1','字段2':'值2'}，参数三：页码，参数四：分页大小
     |
     |  rollback(self)
     |      # 回滚
     |
     |  updateByTable(self, table, column_dict={}, cond_dict={})
     |      # 更新，参数一：表名，参数二用于set 字段1=值1，字段2=值2...格式：{'字段1':'值1','字段2':'值2'},
     |      # 参数三：用于where条件，如 where 字段3=值3 and 字段4=值4，格式{'字段3':'值3','字段4':'值4'}
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables (if defined)
     |
     |  __weakref__
     |      list of weak references to the object (if defined)

DATA
    BASE_DIR = r'C:\Users\china\PycharmProjects\python_utils'
    modules = {'DBUtils': <module 'DBUtils' from 'C:\\Program Files\\Pytho...

FILE