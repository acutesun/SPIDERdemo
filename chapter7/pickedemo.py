import pickle


class A:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def start():
        print('start')
        raise Exception('raise exception in enter')

    @staticmethod
    def clean_up():
        print('clean and exit')

    def __enter__(self):
        print('enter+self:', self.name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        A.clean_up()
        return True  # 不抛出异常，默认None抛出异常

def b():
    with A('aaa') as a:
        print('in a')
        return a

if __name__ == '__main__':
    f = open('data', 'wb')
    pickle.dump([1, 2, 3], f)
    pickle.dump('hello', f)
    pickle.dump({'hi': 'haha'}, f)
    f.close()

    with open('data', 'rb') as f:
        try:
            while True:
                print(pickle.load(f))
        except EOFError:
            print('加载完毕')

    a = b()
    print(a)