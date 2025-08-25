def serialize_data(obj):
    if isinstance(obj, list):
        return [serialize_data(item) for item in obj]

    # Agar Row object hai (has _mapping attribute)
    if hasattr(obj, "_mapping"):
        return dict(obj._mapping)

    # ORM model object
    data = obj.__dict__.copy()
    data.pop('_sa_instance_state', None)
    return data

