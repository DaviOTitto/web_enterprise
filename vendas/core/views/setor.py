from django.views.generic import DetailView, ListView

from ..models import Setor
from ..forms import ProdutoForm, SetorProForm
from ..mixins import CounterMixin, FirstnameSearchMixin

class SetorList(CounterMixin, FirstnameSearchMixin, ListView):
    template_name = 'core/setor/setor_list.html'
    model = Setor
    paginate_by = 8
    # Query responsável pelo filtro de usuários pelo primeiro nome
    def get_queryset(self): 
        p = Setor.objects.all()
        q = self.request.GET.get('search_box')
        # buscar por produto
        if q is not None:
            p = p.filter(Nome_SET__icontains=q)
        return p


class SetorDetail(DetailView):
    template_name = 'core/setor/setor_detail.html'
    model = Setor