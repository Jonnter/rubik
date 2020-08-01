from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from mptt.models import MPTTModel,TreeForeignKey
import uuid

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(password=password,username=username,)
        user.level = 2
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AuthMenu(models.Model):
    """
    菜单
    """
    menu_type = (
        (1, '菜单'),
        (2, '操作'),
    )
    menu_state = (
        (0,'禁用'),
        (1,'启用'),
    )
    name = models.CharField(max_length=32,blank=True,null=True,verbose_name="菜单中文名称")
    url = models.CharField(max_length=255,blank=True, null=True, verbose_name='url')
    parent = models.ForeignKey('self',null=True,blank=True,on_delete=models.CASCADE,verbose_name='父节点')
    only = models.CharField(default="",max_length=64,verbose_name="唯一标识")
    icon = models.CharField(max_length=32, blank=True, null=True, verbose_name="菜单图标")
    wight = models.IntegerField(verbose_name="权重")
    is_state = models.SmallIntegerField(default=1,choices=menu_state,verbose_name='状态，1启用，0禁用')
    type = models.SmallIntegerField(choices=menu_type,default=1,verbose_name='菜单类型  2：操作；1：只作为菜单')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    utime = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"菜单"
        verbose_name_plural = verbose_name

    class MPTTMeta:
        # parent_attr = 'parent_name'
        order_insertion_by = ['name']

class AuthRole(models.Model):
    """
    角色
    """
    role_state = (
        (0, '禁用'),
        (1, '启用'),
    )
    name = models.CharField(max_length=64, unique=True, verbose_name="角色名称")
    pid = models.IntegerField(default=0, verbose_name='父级ID')
    menu = models.ManyToManyField("AuthMenu",verbose_name="菜单ID")
    is_state = models.SmallIntegerField(choices=role_state,default=1, verbose_name='状态，1启用，0禁用')
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    utime = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"角色"
        verbose_name_plural = verbose_name

class UserProfile(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,verbose_name=_("id"))
    name = models.CharField(max_length=32, default=None, blank=True, null=True,verbose_name="名称")
    username = models.CharField(max_length=32,unique=True, verbose_name="用户名")
    mobile = models.CharField(max_length=32, default=None, blank=True, null=True, verbose_name="手机号")
    email = models.EmailField( max_length=255, unique=True,verbose_name="email")
    roles = models.ForeignKey(to="AuthRole", null=True, blank=True,on_delete=models.CASCADE,verbose_name="角色ID")
    avatar = models.ImageField(upload_to="static/images/users/",default="admin.jpeg",verbose_name="头像")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    # is_superuser = models.BooleanField(default=False, verbose_name="用户类型")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    login_date = models.DateTimeField(blank=True, null=True, verbose_name="最后登录时间")
    valid_date = models.DateTimeField(blank=True, null=True, verbose_name="有效日期")
    comment = models.CharField(max_length=128, blank=True, null=True, verbose_name="备注")

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_email(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser

    def set_password(self, raw_password):
        self._set_password = True
        if raw_password:
            return super().set_password(raw_password)

    def reset_password(self, new_password):
        self.set_password(new_password)
        self.save()

    class Meta:
        verbose_name = u"用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

