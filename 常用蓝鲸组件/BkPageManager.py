class BkPageManage(object):
    def __init__(self, func, page=1, start=0, limit=200, no_page=False, **kwargs):
        self.func = func
        self.page = page
        self.start = start
        self.limit = limit
        self.no_page = no_page
        self.kwargs = kwargs
        self.__result = []
        self.__count = 0

    def __call__(self, *args, **kwargs):
        # 不分页
        if self.no_page:
            self.set_kwargs()
            self.__result, self.__count = self.func(**self.kwargs)
            for i in range(self.start, self.__count, self.limit):
                self.add_page()
                self.set_kwargs()
                result, count = self.func(**self.kwargs)
                self.__result.extend(result)
            return self
        # 分页
        for p in range(self.page - 1):
            self.add_page()
        self.set_kwargs()
        self.__result, self.__count = self.func(**self.kwargs)
        return self

    def set_kwargs(self):
        self.kwargs.update({
            'page': {
                'start': int(self.start),
                'limit': int(self.limit)
            }
        })

    def add_page(self):
        self.start += self.limit

    def get_result(self):
        return self.__result, self.__count
