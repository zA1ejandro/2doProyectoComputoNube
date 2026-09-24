# Garantizar soporte y compatibilidad para cliente MariaDB / MySQL
try:
    import MySQLdb  # pragma: no cover
except ImportError:
    try:
        import pymysql  # pragma: no cover
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
