TABLE = "oc_customer"

CREATE_COLUMNS = [
    "firstname",
    "lastname",
    "email",
    "telephone",
    "password",
    "status",
    "customer_group_id",
    "store_id",
    "language_id",
]


def create_customer(connection, customer_data):
    cols = CREATE_COLUMNS
    placeholders = ", ".join(["%s"] * len(cols))
    colnames = ", ".join(f"`{c}`" for c in cols)
    sql = f"INSERT INTO `{TABLE}` ({colnames}) VALUES ({placeholders})"
    values = [customer_data[c] for c in cols]

    with connection.cursor() as cur:
        cur.execute(sql, values)
        return int(cur.lastrowid)


def get_customer_by_id(connection, customer_id):
    sql = f"SELECT * FROM `{TABLE}` WHERE `customer_id`=%s"
    with connection.cursor() as cur:
        cur.execute(sql, (customer_id,))
        return cur.fetchone()


def update_customer_basic_fields(
        connection,
        customer_id,
        *,
        firstname=None,
        lastname=None,
        email=None,
        telephone=None,
):
    updates = []
    values = []

    if firstname is not None:
        updates.append("`firstname`=%s");
        values.append(firstname)
    if lastname is not None:
        updates.append("`lastname`=%s");
        values.append(lastname)
    if email is not None:
        updates.append("`email`=%s");
        values.append(email)
    if telephone is not None:
        updates.append("`telephone`=%s");
        values.append(telephone)

    if not updates:
        return 0

    set_clause = ", ".join(updates)
    sql = f"UPDATE `{TABLE}` SET {set_clause} WHERE `customer_id`=%s"
    values.append(customer_id)

    with connection.cursor() as cur:
        cur.execute(sql, values)
        return cur.rowcount


def delete_customer_by_id(connection, customer_id):
    sql = f"DELETE FROM `{TABLE}` WHERE `customer_id`=%s"
    with connection.cursor() as cur:
        cur.execute(sql, (customer_id,))
        return cur.rowcount
