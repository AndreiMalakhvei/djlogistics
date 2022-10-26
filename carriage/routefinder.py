from carriage.models import Distance, City, BorderCrossing
from django.db.models import Q


def get_graph():
    graph = {}
    qs = Distance.objects.select_related('from_city', 'to_city', 'coeff')
    for i in qs:
        if i.from_city.name in graph:
            graph[i.from_city.name].update({(i.to_city.name, i.coeff.coeff_type): (i.distance, i.coeff.coeff_value)})
        else:
            graph[i.from_city.name] = {(i.to_city.name, i.coeff.coeff_type): (i.distance, i.coeff.coeff_value)}
        #    создаём обратные направления
        if i.to_city.name in graph:
            graph[i.to_city.name].update({(i.from_city.name, i.coeff.coeff_type): (i.distance, i.coeff.coeff_value)})
        else:
            graph[i.to_city.name] = {(i.from_city.name, i.coeff.coeff_type): (i.distance, i.coeff.coeff_value)}
    return graph


class Vertex:
    vertices = []
    qs = City.objects.select_related('country')
    qs_add = BorderCrossing.objects.all()

    def __init__(self, items_tuple, graph, previous, selection):
        self.name = items_tuple[0][0]
        self.trans_type = items_tuple[0][1]
        self.previous_name = previous.name
        self.destinations = graph[self.name]
        self.visited = False
        self._added_time = 0
        self._added_price = 0
        self.log = []

        if Vertex.qs.get(name=self.name).country.cust_territory != \
                Vertex.qs.get(name=previous.name).country.cust_territory:
            added_value = Vertex.qs_add.get(
                Q(from_cust_territory_id=Vertex.qs.get(name=previous.name).country.cust_territory.cust_territory)
                & Q(to_cust_territory_id=Vertex.qs.get(name=self.name).country.cust_territory.cust_territory))
            self._added_time = added_value.approx_time
            self._added_price = added_value.add_price

        self._distance = items_tuple[1][0]
        self.distance = self._distance + previous.distance
        self.price = round(items_tuple[1][1] * self._distance + previous.price + self._added_price)
        self._worktime = self._distance / 60
        self.time = previous

        if selection == '1':
            self.value = self.time
        else:
            self.value = self.price

        Vertex.vertices.append(self)

    @property
    def time(self):
        return round(self.totaltime + self._worktime)

    @time.setter
    def time(self, previous):
        # считаем, что фура движется 8 ч со скоростью 60 км/час, после чего делает перерыв 10 часов. Через пять рабочих
        # дней (120ч) - пауза 36 ч
        a = self._worktime + previous._worktime
        b = a // 8
        self._worktime = a % 8
        checked_time = previous.totaltime + (a - self._worktime) + b * 10
        self.totaltime = checked_time + (checked_time // 120) * 36 + self._added_time

    class HtmlCity:
        def __init__(self, cityname):
            self.name = cityname
            self.country = Vertex.qs.get(name=cityname).country.name
            self.flag = Vertex.qs.get(name=cityname).country.flag_small


    def get_log(self, start):

        self.start = start.name
        self.log.append(Vertex.HtmlCity(self.name))
        k = self
        while k.name != start.name:
            for i in Vertex.vertices:
                if i.name == k.previous_name:
                    self.log.append(Vertex.HtmlCity(i.name))
                    k = i
        self.log.reverse()


    def get_cleaned_time(self):
        self.days = int(self.totaltime // 24)
        self.hours = int(self.totaltime % 24)


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
        self._worktime = 0
        self.totaltime = 0
        self.previous_name = None
        Vertex.vertices.append(self)


def shortest(start_str, finish_str, selection):
    graph = get_graph()
    # Создаём первый экземпляр класса. Нужно вручную определить значения всех аттрибутов
    start = FirstVertex(start_str, graph)

    # Создаём первые экземпляры с автоматическим высчитванием значений аттрибутов
    for i in start.destinations.items():
        Vertex(i, graph, start, selection)

    while True:
        # Находим ребро с минимальным весом
        mn = min(x.value for x in Vertex.vertices if x.visited is False)
        next_vertex = next(filter(lambda x: x.value == mn and x.visited is False, Vertex.vertices))
        # Отмечаем вершину как пройденную
        next_vertex.visited = True
        # Проверяем, является ли следующая выбранная вершина пунктом назначения
        if next_vertex.name == finish_str:

            next_vertex.get_log(start)
            next_vertex.get_cleaned_time()
            break
        # Добавляем в список вершины, смежные с next_vertex, и пересчитываем для них веса рёбер:
        for i in next_vertex.destinations.items():
            # проверяем, есть ли уже в Vertex.vertices вершины, представляющие собой направления из next_vertex
            somevar = Vertex.get_inst(i[0][0])
            # Если в Vertex.vertices не найдено таких вершин, то создаётся новый экземпляр класса.
            # Значения аттрибутов плюсуются к значениям, которые были у next_vertex
            if not somevar:
                Vertex(i, graph, next_vertex, selection)

            # если же такая вершина уже есть и она ещё не отмечена как посещённая, то сравниваем, какой вес меньше:
            # от старта через next_vertex до неё или прежнее "от старта через иную вершину"
            else:
                if not somevar.visited:
                    alternative_somevar = Vertex(i, graph, next_vertex, selection)
                    if alternative_somevar.value < somevar.value:
                        Vertex.vertices.remove(somevar)
                    else:
                        Vertex.vertices.remove(alternative_somevar)
                        # Vertex(i, graph, next_vertex, selection)

    Vertex.vertices.clear()
    return next_vertex


class WarehouseResult:
    def __init__(self, price_query, data_dict):
        self.coeff = 1
        if data_dict['t1']:
            self.coeff = price_query.customs_coeff

        self._timedelta = data_dict['dep_date'] - data_dict['arr_date']
        self.pll_handling = data_dict['pll_num'] * 2 * price_query.loading * self.coeff
        self.pll_storage = self._timedelta.days * data_dict['pll_num'] * price_query.storage * self.coeff
        self.labelling = data_dict['units_num'] *  price_query.labeling * self.coeff
        self.ex = price_query.ex
        if data_dict['codes_num'] > 5:
            self.ex += (data_dict['codes_num'] - 5) * price_query.codes_add
        self.total = self.pll_handling + self.pll_storage + self.labelling + self.ex

        self.manifest = 0
        if price_query.manifest:
            self.manifest = price_query.manifest
            self.total += self.manifest


    def __setattr__(self, attr, value):
        if type(value).__name__ == 'float':
            value = round(value, 2)
        return object.__setattr__(self, attr, value)




