from carriage.models import Warehouse


def global_navbar(request):
    nav_warehouses = Warehouse.objects.select_related('city__country')
    return {'nav_warehouses': nav_warehouses}
