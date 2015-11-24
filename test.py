class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.bd_arq, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.criar_bd()

    def tearDown(self):
        os.close(self.bd_arq)
        os.unlink(flaskr.app.config['DATABASE'])

    def teste_bd_vazio(self):
        res = self.app.get('/')
        assert 'nenhuma entrada' in res.data

def teste_nova_entrada(self):
    self.login('admin', 'default')
    rv = self.app.post('/inserir', data=dict(
        titulo='<Olá>',
        texto='<strong>HTML</strong> é permitido aqui'
    ), follow_redirects=True)
    assert rv.status_code == 200
    assert 'nenhuma entrada' not in rv.data
    assert '&lt;Olá&gt;' in rv.data
    assert '<strong>HTML</strong> é permitido aqui' in rv.data
