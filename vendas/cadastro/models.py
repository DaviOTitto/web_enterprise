from django.db import models

gender_list = [('M', 'Masculino'), ('F', 'Feminino')]

class TimeStampedModel(models.Model):
    created = models.DateTimeField(
        'criado em', auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(
        'modificado em', auto_now_add=False, auto_now=True)

    class Meta:
        abstract = True

        
class Person(TimeStampedModel):
    """ Person is abstract model """
    gender = models.CharField('Gênero', max_length=1, choices=gender_list)
    cpf = models.CharField('CPF', max_length=11)
    firstname = models.CharField('Nome', max_length=20)
    lastname = models.CharField('Sobrenome', max_length=20)
    email = models.EmailField('E-mail', unique=True)
    phone = models.CharField('Fone', max_length=18)
    birthday = models.DateField('Nascimento')

    class Meta:
        abstract = True
        ordering = ['firstname']

    def __str__(self):
        return self.firstname + " " + self.lastname
    full_name = property(__str__)


class  Cadastro(Person):
    pass
    
    class Meta:
        verbose_name = 'cadastro'
        verbose_name_plural = 'cadastros'

    # clica na pessoa e retorna os detalhes dela
    def get_customer_url(self):
        return f'/ Cadastros/{self.id}'

    # clica em vendas e retorna as vendas da pessoa
    def get_sale_customer_url(self):
        return f'/venda/?Cadastros_sale={self.id}'

    # vendas por pessoa
    def get_sales_count(self):
        return self. Cadastros_sale.count()