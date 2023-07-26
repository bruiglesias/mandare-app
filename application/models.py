from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models import Count

# Create your models here.


class UsuarioManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("O e-mail é progratório")

        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(email, password, **extra_fields)


class Profissional(AbstractUser):

    nome = models.CharField('Nome', max_length=100, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True)
    especialidade = models.CharField('Especialidade', max_length=100)
    celular = models.CharField('Celular', max_length=20)
    pais = models.CharField('Pais', max_length=20)
    estado = models.CharField('Estado', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    email = models.EmailField('E-mail', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return f"{self.nome} - {self.email}"

    objects = UsuarioManager()


class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    data_nascimento = models.DateField()
    especialidade = models.CharField(max_length=100)
    data_cadastro = models.DateField(auto_now_add=True)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    diagnostico = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return self.nome


class Programa(models.Model):
    nome = models.CharField(max_length=100)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    numero_sessoes = models.PositiveIntegerField()
    numero_tentativas = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'

    def __str__(self):
        return self.nome


class ProgramaPaciente(models.Model):
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)  # noqa
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Programa-Paciente'
        verbose_name_plural = 'Programas-Paciente'

    def __str__(self):
        return self.programa.nome


class Sessao(models.Model):
    nome = models.CharField(max_length=100)
    programa = models.ForeignKey(ProgramaPaciente, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'

    def __str__(self):
        return self.nome


class Tentativa(models.Model):
    nome = models.CharField(max_length=100)
    SITUACAO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
        ('Suporte', 'Suporte'),
    ]

    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE, related_name='sessão')  # noqa
    situacao = models.CharField(max_length=20, choices=SITUACAO_CHOICES, null=True, blank=True)  # noqa
    criado = models.DateField('Data de criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Tentativa'
        verbose_name_plural = 'Tentativas'

    def __str__(self):
        return self.nome


@receiver(post_save, sender=ProgramaPaciente)
def criar_sessoes(sender, instance: ProgramaPaciente, created, **kwargs):
    if created:

        numero_sessao = 1
        for _ in range(instance.programa.numero_sessoes):

            sessao = Sessao.objects.create(nome=f"Sessão {numero_sessao}", programa=instance)  # noqa

            numero_tentativa = 1
            for _ in range(instance.programa.numero_tentativas):
                Tentativa.objects.create(nome=f"{numero_tentativa}ª tentativa - Sessão {numero_sessao}", sessao=sessao)  # noqa
                numero_tentativa += 1
            numero_sessao += 1
