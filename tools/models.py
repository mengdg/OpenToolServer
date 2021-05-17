from django.db import models


# Create your models here.

class BaseModel(models.Model):
    id = models.AutoField(db_index=True, primary_key=True)
    create_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)  # auto_now_add=True:对象第一次被创建时自动设置当前时间
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True)  # auto_now = True:每次保存对象时，自动设置该字段为当前时间

    class Meta:
        abstract = True


class Users(BaseModel):
    """
    用户信息
    """
    uid = models.CharField(max_length=64, unique=True, db_index=True)  # Lark uuid
    name = models.CharField(max_length=64, null=False, db_index=True)  # 用户名
    email = models.CharField(max_length=64, null=True)  # 邮箱
    mobile = models.CharField(max_length=16, null=True)  # 手机号
    avatar = models.CharField(max_length=256, null=False)  # 头像
    identity = models.CharField(max_length=256, default=['viewer'], null=False)  # 身份
    state = models.IntegerField(default=1)  # 状态 1：开启 2：关闭

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Users:%s>' % self.name


class DebugTalk(BaseModel):
    """
    DebugTalk
    """
    debugtalk = models.TextField(default='#debugtalk.py')
    user = models.ForeignKey(to="Users", to_field="uid", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "debugtalk"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<DebugTalk:%s>' % self.id


class BackupDebugTalk(BaseModel):
    """
    记录每次更新DebugTalk
    """
    user = models.ForeignKey(to="Users", to_field="uid", db_index=True, on_delete=models.CASCADE)
    debugtalk = models.ForeignKey(to="DebugTalk", to_field="id", db_index=True, on_delete=models.CASCADE)
    backup_debugtalk = models.TextField(default='#debugtalk.py')

    class Meta:
        verbose_name = "backup_debugtalk"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Update DebugTalk:%s>' % self.debugtalk


class Tools(BaseModel):
    """
    工具信息
    """
    user = models.ForeignKey(to="Users", to_field="uid", on_delete=models.CASCADE, db_index=True)
    image = models.CharField(max_length=2048, null=False, default="https://tse2-mm.cn.bing.net/th/id/OIP.b545z5yupv"
                                                                  "4crcnaiIW6rgHaHa?pid=Api&rs=1")
    card_router = models.CharField(max_length=64, null=False, unique=True)
    name = models.CharField(max_length=64, null=False, db_index=True)
    describe = models.TextField(default='无')
    project = models.ForeignKey(to="Project", to_field="id", on_delete=models.CASCADE)
    state = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)
    params = models.CharField(max_length=2048)
    debugtalk = models.OneToOneField(to="DebugTalk", to_field="id", on_delete=models.CASCADE, null=False)
    function_meta = models.CharField(max_length=2048, null=False)

    class Meta:
        verbose_name = "tools"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Tools:%s>' % self.name


class Project(BaseModel):
    """
    工具分类
    """
    name = models.CharField(max_length=64)  # 英文名
    label = models.CharField(max_length=64)  # 标签名
    state = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)

    class Meta:
        verbose_name = "project"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Project:%s>' % self.name


class ToolVisitor(BaseModel):
    """
    用户浏览信息
    """
    user = models.ForeignKey(to="Users", to_field="uid", on_delete=models.CASCADE)
    tool = models.ForeignKey(to="Tools", to_field="id", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "tool_visitor"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<ToolVisitor:%s>' % self.id


class Wisdom(BaseModel):
    """
    心灵鸡汤
    """
    text = models.TextField()

    class Meta:
        verbose_name = "wisdom"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Wisdom:%s>' % self.id


class Logs(BaseModel):
    """
    日志
    """
    user = models.ForeignKey(to="Users", to_field="uid", on_delete=models.CASCADE, db_index=True)
    event = models.CharField(max_length=128, null=False, db_index=True)
    content = models.TextField()

    class Meta:
        verbose_name = "logs"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Logs:%s>' % self.id


class Navigation(BaseModel):
    """
    导航数据
    """
    name = models.CharField(max_length=128, null=False)
    url = models.CharField(max_length=512)
    img = models.CharField(max_length=512)
    desc = models.CharField(max_length=256)
    kind = models.ForeignKey(to="Kind", to_field="id", on_delete=models.CASCADE)
    recommend = models.IntegerField(default=0)  # 是否推荐0:不推荐 1:推荐
    state = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)

    class Meta:
        verbose_name = "navigation"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Navigation:%s>' % self.id


class Kind(BaseModel):
    """
    导航分类
    """
    name = models.CharField(max_length=128, null=False)
    state = models.IntegerField(default=1)
    sort = models.IntegerField(default=0)

    class Meta:
        verbose_name = "kind"
        verbose_name_plural = verbose_name

    def _unicode_(self):
        return '<Kind:%s>' % self.id
