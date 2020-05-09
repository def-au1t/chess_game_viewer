from django.db.models import Lookup

class OnlyYearAndMonth(Lookup):
    lookup_name = 'ym'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = [rhs_params[0].year, rhs_params[0].month]
        return 'extract(year FROM %s) = %s AND extract(month FROM %s) = %s' % (lhs, rhs, lhs, rhs), params
