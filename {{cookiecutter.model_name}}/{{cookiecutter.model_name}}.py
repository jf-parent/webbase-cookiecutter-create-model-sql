
from server.utils import SafeStringField
from server.model.basemodel import BaseModel
from server.settings import config
from server import exceptions
from server.database import Base


class {{cookiecutter.model_name|title}}(Base, BaseModel):

    __tablename__ = '{{cookiecutter.model_name|lower}}'

    safe_string = Column(SafeStringField(250), nullable=False)

    def __repr__(self):
        try:
            _repr = "{{cookiecutter.model_name|title}} <safe_string: {self.safe_string}>"  # noqa
            return _repr.format(
                self=self
                )
        except AttributeError:
            return "{{cookiecutter.model_name|title}} uninitialized"

##############################################################################
# FUNC
##############################################################################

    async def sanitize_data(self, context):
        author = context.get('author')
        data = context.get('data')

        if author:
            if author.role == 'admin':
                return data
            else:
                editable_fields = []
        else:
            editable_fields = []

        return {k: data[k] for k in data if k in editable_fields}

    async def validate_and_save(self, context):
        data = context.get('data')
        db_session = context.get('db_session')

        is_new = await self.is_new()

        # SAFE STRING
        safe_string = data.get('safe_string')
        if safe_string:
            self.safe_string = safe_string
        else:
            raise exceptions.MissingValueExceptions('safe_string')

        db_session.save(self, safe=True)

    async def method_autorized(self, context):
        method = context.get('method')
        author = context.get('author')

        if method in ['create', 'delete']:
            if author.role == 'admin':
                return True
            else:
                return False
        elif method in ['update', 'read']:
            if author == self:
                return True
            elif author.role == 'admin':
                return True
            else:
                return False

    async def serialize(self, context):
        data = {}
        return data
