from sqlalchemy.event import listens_for
from sqlalchemy.orm import Query

@listens_for(Query, 'before_compile', retval=True)
def filter_deleted(query):
    for desc in query.column_descriptions:
        entity = desc['entity']
        if isinstance(entity, type) and hasattr(entity, 'deleted_at'):
            if not query.execution_options.get('include_deleted', False):
                query = query.filter(entity.deleted_at == None)
    return query