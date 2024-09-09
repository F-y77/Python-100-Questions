import random
import tkinter as tk
from tkinter import messagebox, ttk
import time
import json

class 记忆卡片:
    def __init__(self, 问题, 答案, 难度):
        self.问题 = 问题
        self.答案 = 答案
        self.难度 = 难度

class 记忆卡片游戏:
    def __init__(self, root):
        self.root = root
        self.root.title("Python编程问答游戏")
        self.题库 = {"简单": [], "中等": [], "困难": []}
        self.卡片集 = []
        self.当前卡片索引 = 0
        self.分数 = 0
        self.错误卡片 = []
        self.开始时间 = 0
        self.时间限制 = 60  # 每道题60秒

        self.难度选择 = tk.StringVar(value="简单")
        self.题目数量 = tk.IntVar(value=10)

        self.创建GUI()
        self.加载题库()

    def 创建GUI(self):
        # 难度选择
        难度框架 = ttk.Frame(self.root)
        难度框架.pack(pady=10)
        ttk.Label(难度框架, text="选择难度:").pack(side=tk.LEFT)
        for 难度 in ["简单", "中等", "困难"]:
            ttk.Radiobutton(难度框架, text=难度, variable=self.难度选择, value=难度).pack(side=tk.LEFT)

        # 题目数量选择
        数量框架 = ttk.Frame(self.root)
        数量框架.pack(pady=10)
        ttk.Label(数量框架, text="题目数量:").pack(side=tk.LEFT)
        ttk.Spinbox(数量框架, from_=5, to=50, textvariable=self.题目数量, width=5).pack(side=tk.LEFT)

        # 开始按钮
        ttk.Button(self.root, text="开始游戏", command=self.开始游戏).pack(pady=10)

        # 其他GUI组件
        self.问题标签 = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400, justify="center")
        self.答案输入 = tk.Entry(self.root, font=("Arial", 12), width=50)
        self.提交按钮 = tk.Button(self.root, text="提交", command=self.检查答案)
        self.结果标签 = tk.Label(self.root, text="", font=("Arial", 12))
        self.时间标签 = tk.Label(self.root, text="", font=("Arial", 12))

    def 加载题库(self):
        try:
            with open("python_questions.json", "r", encoding="utf-8") as file:
                题库数据 = json.load(file)
                for 难度, 题目列表 in 题库数据.items():
                    for 题目 in 题目列表:
                        self.题库[难度].append(记忆卡片(题目["问题"], 题目["答案"], 难度))
        except FileNotFoundError:
            print("题库文件不存在,使用默认题目")
            self.创建默认题库()
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            self.创建默认题库()

    def 创建默认题库(self):
        默认题目 = {
            "简单": [
                {"问题": "在Python中,如何声明一个空列表?", "答案": "[]"},
                {"问题": "Python中的字典使用什么符号表示?", "答案": "{}"},
                {"问题": "Python中的注释符号是什么?", "答案": "#"},
                {"问题": "如何在Python中定义一个函数?", "答案": "def 函数名():"},
                {"问题": "Python中的条件语句关键字是什么?", "答案": "if"},
                {"问题": "如何在Python中创建一个类?", "答案": "class 类名:"},
                {"问题": "Python中用于循环的两个关键字是什么?", "答案": "for和while"},
                {"问题": "Python中用于输出的函数是什么?", "答案": "print"},
                {"问题": "Python中如何表示布尔值True?", "答案": "True"},
                {"问题": "Python中如何获取列表的长度?", "答案": "len()"},
                {"问题": "Python中的字符串用什么符号表示?", "答案": "单引号或双引号"},
                {"问题": "如何在Python中导入模块?", "答案": "import 模块名"},
                {"问题": "Python中的整数除法运算符是什么?", "答案": "//"},
                {"问题": "如何在Python中创建一个元组?", "答案": "()"},
                {"问题": "Python中的 'and' 运算符的作用是什么?", "答案": "逻辑与"},
                {"问题": "如何在Python中创建一个集合?", "答案": "set()"},
                {"问题": "Python中的 'or' 运算符的作用是什么?", "答案": "逻辑或"},
                {"问题": "如何在Python中获取用户输入?", "答案": "input()"},
                {"问题": "Python中的 'not' 运算符的作用是什么?", "答案": "逻辑非"},
                {"问题": "如何在Python中将字符串转换为整数?", "答案": "int()"},
                {"问题": "如何在Python中创建一个空字典?", "答案": "{}"},
                {"问题": "Python中的range()函数的作用是什么?", "答案": "生成一个数字序列"},
                {"问题": "如何在Python中对列表进行排序?", "答案": "使用sort()方法或sorted()函数"},
                {"问题": "Python中的字符串格式化操作符是什么?", "答案": "%"},
                {"问题": "如何在Python中将整数转换为字符串?", "答案": "str()"},
                {"问题": "Python中的pass语句的作用是什么?", "答案": "作为占位符,不执行任何操作"},
                {"问题": "如何在Python中检查一个值是否在列表中?", "答案": "使用in关键字"},
                {"问题": "Python中的continue语句的作用是什么?", "答案": "跳过当前循环的剩余语句,继续下一次循环"},
                {"问题": "如何在Python中获取当前日期和时间?", "答案": "使用datetime模块"},
                {"问题": "Python中的random模块的作用是什么?", "答案": "生成随机数"}
            ],
            "中等": [
                {"问题": "如何在Python中创建一个生成器函数?", "答案": "使用yield关键字"},
                {"问题": "什么是装饰器(decorator)?", "答案": "一种修改其他函数的函数"},
                {"问题": "如何在Python中使用正则表达式?", "答案": "import re模块"},
                {"问题": "Python中的*args和**kwargs是什么?", "答案": "*args是可变参数,**kwargs是关键字参数"},
                {"问题": "如何在Python中实现多线程?", "答案": "import threading模块"},
                {"问题": "Python中的with语句用于什么?", "答案": "用于资源管理"},
                {"问题": "什么是Python的上下文管理器(context manager)?", "答案": "一种支持with语句的对象"},
                {"问题": "如何在Python中使用枚举类型(enum)?", "答案": "import enum模块"},
                {"问题": "Python中的__init__方法是什么?", "答案": "类的构造函数"},
                {"问题": "如何在Python中实现单例模式?", "答案": "使用__new__方法"},
                {"问题": "什么是Python中的列表推导式?", "答案": "一种简洁创建列表的方式"},
                {"问题": "如何在Python中处理异常?", "答案": "使用try-except语句"},
                {"问题": "什么是Python中的lambda函数?", "答案": "一种匿名函数"},
                {"问题": "如何在Python中读取文件?", "答案": "使用open()函数"},
                {"问题": "什么是Python中的迭代器?", "答案": "一种可以被迭代的对象"},
                {"问题": "如何在Python中创建虚拟环境?", "答案": "使用venv模块"},
                {"问题": "什么是Python中的闭包(closure)?", "答案": "一个函数和其相关的引用环境组合而成的实体"},
                {"问题": "如何在Python中进行单元测试?", "答案": "使用unittest模块"},
                {"问题": "什么是Python中的生成器表达式?", "答案": "类似列表推导式但返回生成器对象"},
                {"问题": "如何在Python中实现函数重载?", "答案": "使用装饰器或默认参数"},
                {"问题": "如何在Python中实现深拷贝?", "答案": "使用copy模块的deepcopy()函数"},
                {"问题": "什么是Python中的property装饰器?", "答案": "用于将方法转换为属性"},
                {"问题": "如何在Python中使用多进程?", "答案": "使用multiprocessing模块"},
                {"问题": "什么是Python中的上下文管理器协议?", "答案": "__enter__和__exit__方法"},
                {"问题": "如何在Python中创建一个自定义异常类?", "答案": "继承Exception类"},
                {"问题": "什么是Python中的functools模块?", "答案": "用于高阶函数和操作可调用对象"},
                {"问题": "如何在Python中实现方法链?", "答案": "在方法中返回self"},
                {"问题": "什么是Python中的反射?", "答案": "在运行时检查和修改对象的能力"},
                {"问题": "如何在Python中使用装饰器工厂?", "答案": "创建返回装饰器的函数"}
            ],
            "困难": [
                {"问题": "解释Python中的GIL(全局解释器锁)是什么?", "答案": "一种防止多线程同时执行Python字节码的机制"},
                {"问题": "什么是元类(metaclass)?", "答案": "用于创建类的类"},
                {"问题": "如何在Python中实现协程?", "答案": "使用asyncio模块"},
                {"问题": "Python中的__slots__是什么?", "答案": "一种节省内存的方式"},
                {"问题": "什么是Python的描述符(descriptor)?", "答案": "一种实现属性访问控制的方式"},
                {"问题": "如何在Python中使用C扩展?", "答案": "使用Cython或CFFI"},
                {"问题": "Python中的__getattr__和__getattribute__有什么区别?", "答案": "__getattr__是后备方法,__getattribute__是主要方法"},
                {"问题": "如何在Python中实现垃圾回收(garbage collection)?", "答案": "import gc模块"},
                {"问题": "什么是Python的内存管理机制?", "答案": "引用计数和垃圾回收"},
                {"问题": "如何在Python中实现多重继承?", "答案": "使用super()函数"},
                {"问题": "什么是Python中的抽象基类(ABC)?", "答案": "定义接口的类,不能被实例化"},
                {"问题": "如何在Python中实现线程安全?", "答案": "使用锁机制或线程安全的数据结构"},
                {"问题": "什么是Python中的弱引用?", "答案": "不会增加对象引用计数的引用"},
                {"问题": "如何在Python中实现函数式编程?", "答案": "使用lambda,map,filter,reduce等"},
                {"问题": "什么是Python中的协程(coroutine)?", "答案": "可以暂停执行的函数"},
                {"问题": "如何在Python中优化代码性能?", "答案": "使用性能分析工具,如cProfile"},
                {"问题": "什么是Python中的元编程?", "答案": "编写操作程序本身的程序"},
                {"问题": "如何在Python中实现并发编程?", "答案": "使用threading,multiprocessing或asyncio"},
                {"问题": "什么是Python中的装饰器类?", "答案": "一种可调用的类,用于装饰其他函数或类"},
                {"问题": "如何在Python中处理大数据?", "答案": "使用pandas,numpy等库"},
                {"问题": "什么是Python中的描述符协议?", "答案": "__get__,__set__,__delete__方法"},
                {"问题": "如何在Python中实现自定义上下文管理器?", "答案": "实现__enter__和__exit__方法"},
                {"问题": "什么是Python中的元类继承?", "答案": "元类可以继承其他元类"},
                {"问题": "如何在Python中实现惰性求值?", "答案": "使用生成器或@property装饰器"},
                {"问题": "什么是Python中的抽象语法树(AST)?", "答案": "源代码的树状表示结构"},
                {"问题": "如何在Python中使用内存视图(memoryview)?", "答案": "创建内存引用而不复制数据"},
                {"问题": "什么是Python中的协程状态机?", "答案": "使用async/await实现的状态转换"},
                {"问题": "如何在Python中实现自定义序列类型?", "答案": "实现__len__,__getitem__等方法"},
                {"问题": "什么是Python中的描述符链?", "答案": "多个描述符按顺序处理属性访问"},
                {"问题": "如何在Python中实现函数式编程的不可变数据结构?", "答案": "使用namedtuple或自定义类"}
            ]
        }
        for 难度, 题目列表 in 默认题目.items():
            for 题目 in 题目列表:
                self.题库[难度].append(记忆卡片(题目["问题"], 题目["答案"], 难度))

    def 开始游戏(self):
        难度 = self.难度选择.get()
        数量 = min(self.题目数量.get(), len(self.题库[难度]))
        self.卡片集 = random.sample(self.题库[难度], 数量)
        random.shuffle(self.卡片集)
        self.当前卡片索引 = 0
        self.分数 = 0
        self.错误卡片 = []

        # 显示游戏组件
        self.问题标签.pack(pady=20)
        self.答案输入.pack(pady=10)
        self.答案输入.bind("<Return>", self.检查答案)
        self.提交按钮.pack(pady=10)
        self.结果标签.pack(pady=10)
        self.时间标签.pack(pady=10)

        self.显示下一张卡片()

    def 显示下一张卡片(self):
        if self.当前卡片索引 < len(self.卡片集):
            卡片 = self.卡片集[self.当前卡片索引]
            self.问题标签.config(text=卡片.问题)
            self.答案输入.delete(0, tk.END)
            self.结果标签.config(text="")
            self.开始时间 = time.time()
            self.更新时间()
        else:
            self.显示结果()

    def 检查答案(self, event=None):
        用户答案 = self.答案输入.get()
        卡片 = self.卡片集[self.当前卡片索引]
        if 用户答案.lower() == 卡片.答案.lower():
            self.结果标签.config(text="正确!", fg="green")
            self.分数 += 1
        else:
            self.结果标签.config(text=f"错误。正确答案是: {卡片.答案}", fg="red")
            self.错误卡片.append(卡片)
        
        self.当前卡片索引 += 1
        self.root.after(1000, self.显示下一张卡片)

    def 更新时间(self):
        剩余时间 = self.时间限制 - int(time.time() - self.开始时间)
        if 剩余时间 > 0:
            self.时间标签.config(text=f"剩余时间: {剩余时间}秒")
            self.root.after(1000, self.更新时间)
        else:
            self.时间标签.config(text="时间到!")
            self.当前卡片索引 += 1
            self.root.after(1000, self.显示下一张卡片)

    def 显示结果(self):
        总数 = len(self.卡片集)
        正确率 = (self.分数 / 总数) * 100
        messagebox.showinfo("游戏结束", f"游戏结束!\n你的得分是: {self.分数}/{总数}\n正确率: {正确率:.2f}%")
        self.复习错误()

    def 复习错误(self):
        if not self.错误卡片:
            messagebox.showinfo("复习", "太棒了!你没有任何错误需要复习。")
        else:
            错误信息 = "让我们复习一下错误的答案:\n\n"
            for 卡片 in self.错误卡片:
                错误信息 += f"问题: {卡片.问题}\n正确答案: {卡片.答案}\n\n"
            messagebox.showinfo("复习错误", 错误信息)
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    游戏 = 记忆卡片游戏(root)
    root.mainloop()