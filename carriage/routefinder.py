from carriage.models import Distance, City


def get_graph():
    graph = {}
    qs = Distance.objects.select_related('from_city', 'to_city', 'coeff')
    for i in qs:
        if i.from_city.name in graph:
            graph[i.from_city.name].update({(i.to_city.name, i.coeff.coeff_type):(i.distance, i.coeff.coeff_value)})
        else:
            graph[i.from_city.name] = {(i.to_city.name, i.coeff.coeff_type):(i.distance, i.coeff.coeff_value)}
        #    создаём обратные направления
        if i.to_city.name in graph:
            graph[i.to_city.name].update({(i.from_city.name, i.coeff.coeff_type):(i.distance, i.coeff.coeff_value)})
        else:
            graph[i.to_city.name] = {(i.from_city.name, i.coeff.coeff_type):(i.distance, i.coeff.coeff_value)}
    return graph

class Vertex:
    vertices = []
    qs = City.objects.select_related('country')
    def __init__(self, items_tuple, graph, previous):
        self.name = items_tuple[0][0]
        self.trans_type = items_tuple[0][1]
        self._distance = items_tuple[1][0]
        self.distance = self._distance + previous.distance
        self._price = items_tuple[1][1] * self._distance
        self.price = self._price + previous.price
        self.previous = previous.name
        self.destinations = graph[self.name]
        self.visited = False

        self._worktime = self._distance / 60
        self._totaltime = 0
        self.time = previous


        self.value = self.distance
        Vertex.vertices.append(self)



    @property
    def time(self):
        return self._totaltime + self._worktime

    @time.setter
    def time(self, previous):
    # считаем, что фура движется 8 ч со скоростью 60 км/час, после чего делает перерыв 10 часов. Через пять рабочих
    # дней (120ч) - пауза 36 ч
        a = self._worktime + previous._worktime
        b = a // 8
        self._worktime = a % 8
        checked_time = previous._totaltime + (a - self._worktime) + b * 10
        if self.crossed_border_check(previous):
            self._totaltime = 36 + checked_time + (checked_time // 120) * 36
        else:
            self._totaltime = checked_time + (checked_time // 120) * 36

    def crossed_border_check(self, previous):
        if Vertex.qs.get(name=self.name).country.cust_territory != Vertex.qs.get(name=previous.name).country.cust_territory:
            return True
        return False

    def get_log(self, start):
        self.start = start.name
        self.log.append(self.name)
        k = self
        while k.name != start.name:
            for i in Vertex.vertices:
                if i.name == k.previous:
                    self.log.append(i.name)
                    k = i
        self.log.reverse()

    @staticmethod
    def get_inst(value):
        for i in Vertex.vertices:
            if i.name == value:
                return i
        return None


class FirstVertex:
    def __init__(self, name, graph):
        self.name = name
        self.visited = True
        self.distance = 0
        self.price = 0
        self.value = self.distance
        self.destinations = graph[self.name]
        self._worktime = 0.00001
        self._totaltime = 0
        self.previous = None
        Vertex.vertices.append(self)



def shortest(start_str, finish_str, selection):
    graph = get_graph()
    # Создаём первый экземпляр класса. Нужно вручную определить значения всех аттрибутов
    start = FirstVertex(start_str, graph)

    # Создаём первые экземпляры с автоматическим высчитванием значений аттрибутов
    for i in start.destinations.items():
        Vertex(i, graph, start)

    while True:
        # Находим ребро с минимальным весом
        mn = min(x.value for x in Vertex.vertices if x.visited == False)
        next_vertex = next(filter(lambda x: x.value == mn and x.visited == False, Vertex.vertices))
        # Отмечаем вершину как пройденную
        next_vertex.visited = True
        # Проверяем, является ли следующая выбранная вершина пунктом назначения
        if next_vertex.name == finish_str:
            next_vertex.log = []
            next_vertex.get_log(start)
            break
        # Добавляем в список вершины, смежные с next_vertex, и пересчитываем для них веса рёбер:
        for i in next_vertex.destinations.items():
            # проверяем, есть ли уже в Vertex.vertices вершины, представляющие собой направления из next_vertex
            somevar = Vertex.get_inst(i[0][0])
            # Если в Vertex.vertices не найдено таких вершин, то создаётся новый экземпляр класса. Значения аттрибутов плюсуются
            # к значениям, которые были у next_vertex
            if not somevar:
                Vertex(i, graph, next_vertex)

             # если же такая вершина уже есть и она ещё не отмечена как посещённая, то сравниваем, какой вес меньше:
            # от старта через next_vertex до неё или прежнее "от старта через иную вершину"
            else:
                if not somevar.visited:
                    if next_vertex.value + i[1][0] < somevar.value:
                        Vertex.vertices.remove(somevar)
                        Vertex(i, graph, next_vertex)


    Vertex.vertices.clear()
    return next_vertex