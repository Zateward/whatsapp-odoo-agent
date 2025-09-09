import xmlrpc.client
from dotenv import load_dotenv
import os

class OdooClient:
    def __init__(self):
        load_dotenv()
        self.url = os.getenv("odoo_url")
        self.db = os.getenv("odoo_db")
        self.username = os.getenv("odoo_username")
        self.password = os.getenv("odoo_password")

        common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        print(f"🔌 Conectado a Odoo como {self.username} (UID: {self.uid})")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")

    def search_read_products(self, domain=None, fields=None):
        domain = domain or []
        fields = fields or ['name', 'list_price']
        products = self.models.execute_kw(
            self.db, self.uid, self.password,
            'product.template', 'search_read',
            [domain], {'fields': fields}
        )
        return products

