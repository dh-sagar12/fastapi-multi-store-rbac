from sqlalchemy import event
from sqlalchemy.orm import Session, with_loader_criteria


def register_soft_delete_filter():  # noqa: C901
    @event.listens_for(Session, "do_orm_execute")
    def apply_soft_delete_filter(execute_state):  # noqa: C901
        if (
            execute_state.is_select
            and not execute_state.execution_options.get(
                "include_deleted", False
            )
        ):
            try:
                # Handle regular SELECT statements
                if hasattr(execute_state.statement, "column_descriptions"):
                    entities = []
                    for desc in execute_state.statement.column_descriptions:
                        entity = desc.get("entity")
                        if entity and hasattr(entity, "deleted_at"):
                            if entity not in entities:
                                entities.append(entity)

                    if entities:
                        options = []
                        for entity in entities:
                            option = with_loader_criteria(
                                entity, lambda cls: cls.deleted_at.is_(None)
                            )
                            options.append(option)

                        execute_state.statement = (
                            execute_state.statement.options(*options)
                        )

                # Handle UNION and other compound queries
                elif hasattr(execute_state.statement, "selects"):
                    # Apply the filter to each SELECT in the UNION
                    for select_stmt in execute_state.statement.selects:
                        if hasattr(select_stmt, "column_descriptions"):
                            entities = []
                            for desc in select_stmt.column_descriptions:
                                entity = desc.get("entity")
                                if entity and hasattr(entity, "deleted_at"):
                                    if entity not in entities:
                                        entities.append(entity)

                            if entities:
                                options = []
                                for entity in entities:
                                    option = with_loader_criteria(
                                        entity,
                                        lambda cls: cls.deleted_at.is_(None),
                                    )
                                    options.append(option)

                                select_stmt = select_stmt.options(*options)

            except Exception as e:
                # Log the error but don't raise it to prevent query execution from failing
                print(f"Error applying soft delete filter: {str(e)}")
